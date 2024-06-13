from uagents import Agent, Bureau, Context, Model, Protocol
from uagents.setup import fund_agent_if_low
import requests
from ai_engine import UAgentResponse, UAgentResponseType
from llama_index.core import VectorStoreIndex
from pathlib import Path
from langchain_cohere import ChatCohere
from langchain_cohere import  CohereEmbeddings
import cohere
from llama_index.readers.file import PDFReader
 
class Message(Model):
    message: str
 
cohere_api_key = '0H1Q7mCc30QBBa5owiQ0Z9BmnlA7FhQmxcwBU7yj'
co = cohere.Client(cohere_api_key)
loader = PDFReader()
documents = loader.load_data(file=Path('DA/IBP.pdf'))
print("Number of documents loaded:", len(documents))
embeddings = CohereEmbeddings(cohere_api_key='0H1Q7mCc30QBBa5owiQ0Z9BmnlA7FhQmxcwBU7yj')
index = VectorStoreIndex.from_documents(documents, embed_model=embeddings)
print(index)

model = "command" 
temperature = 0 
max_tokens = 400
llm = ChatCohere(model=model,temperature=0,cohere_api_key=cohere_api_key,max_tokens=max_tokens)

query_engine = index.as_query_engine(llm=llm)
query_results = query_engine.retrieve("What is in this document?")


# Query with Cohere
def query_with_cohere(context, query):
    prompt = f"Context: {context}\nQuery: {query}\nAnswer:" 
    response = co.generate( 
        model='command-nightly',
        prompt=prompt,
        max_tokens=2000,
        temperature=0.5,
        presence_penalty=0.5,
        num_generations=1,  # Generate multiple responses
        truncate='END',  # Truncate input at the end if it exceeds the maximum token length
        k=1,  # Enable top-k sampling with k=50
        p=0.75)
    return response.generations[0].text

context_from_llama_index = query_results 
#cohere_response = query_with_cohere(context_from_llama_index, "what is this rules in document?")
#print("Cohere's response:", cohere_response)

analysisAgent = Agent(
    name="DocAnalysis",
    seed="DocAnalysis agent phrase"
    
)
requestAgent = Agent(
    name="requestAgent",
    seed="requestAgent secret phrase"

)

mappingAgent = Agent(
    name="mappingAgent",
    seed= 'mappingAgent secret phrase'
)

recommendationAgent = Agent(
    name="recommendationAgent",
    seed="recommendationAgent secret phrase"
)
#RECIPIENT_ADDRESS="agent1qvshnse5680dlthrzygny3y9nvvvvsdl8t7hr6f78jy3d59645j8qateu70"

@requestAgent.on_event('startup')
async def send_message(ctx: Context):
     ctx.logger.info(f'hello, my name is {requestAgent.name} and and my address is {requestAgent.address}!')
     await ctx.send(analysisAgent.address, Message(message="hello there I'm requestAgent"))
     ctx.logger.info("message sent")

@analysisAgent.on_event('startup')
async def say_hello(ctx: Context):
    ctx.logger.info(f'hello, my name is {analysisAgent.name} and and my address is {analysisAgent.address}!')


@mappingAgent.on_event('startup')
async def say_hello(ctx: Context):
    ctx.logger.info(f'hello, my name is {mappingAgent.name} and and my address is {mappingAgent.address}!')

@recommendationAgent.on_event('startup')
async def say_hello(ctx: Context):
    ctx.logger.info(f'hello, my name is {recommendationAgent.name} and and my address is {recommendationAgent.address}!')

@requestAgent.on_message(model=Message)
async def requestAgent_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")

 
@analysisAgent.on_message(model=Message)
async def analysisAgent_message_handle(ctx: Context, sender: str, msg:Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
    query = "Summarize this document into key parts such as rules, types and dates"

    try:
        ctx.logger.info(" Loading the Document..")
        ctx.logger.info(" Document Loaded Succesfully..")
        response = query_with_cohere(context_from_llama_index,query)
        if not response:
            raise Exception("Failed to retrieve Response")
        
        await ctx.send(mappingAgent.address, Message(message=response))
        ctx.logger.info(f"Response: {response}")
    
    except Exception as exc:
        ctx.logger.error(f"An error occured: {exc}")
        await ctx.send(
            sender,
            UAgentResponse(
                message=f"Error: {exc}",
                type=UAgentResponseType.ERROR
            )
        )

@mappingAgent.on_message(model=Message)
async def mappingAgent_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}")
    user_data = """
    User Data:
    Pension Details: Scheme: Example Pension Scheme (EPS) Pension Fund, Contracted Out: Yes, Contracted Out End Date: 30th April 2003, Post 5 April 1997 Basis: Reference Scheme Test, Equalisation Date: 1st November 1993, Retirement Details: Normal Retirement Date (NRD): 60th Birthday, Early Retirement Eligibility: From 55th Birthday, Early Retirement Ill Health Eligibility: Any age if "Incapacity" definition is met, Late Retirement: Pension must commence before age 75, Pension Revaluation in Deferment: Pre 6/4/1988 GMP: Fixed Rate Revaluation, Post 5/4/1988 GMP: As per Pre 6/4/1988 GMP, Non-GMP Benefits: Fixed 7.5%, Pension Increases in Payment: Pre 6/4/1988 GMP: Fixed 7.5%, Post 5/4/1988 GMP: Fixed 7.5%, Pre 6/4/1997 Excess: Fixed 7.5%, 6/4/1997 to 30/4/1999 Benefits: Fixed 7.5%, Post 30/4/1999 Benefits: RPI subject to a minimum increase of 0% and a maximum increase of 5%, Death Benefits: Qualifying Spouse’s Pension: 50% of member’s pre-commutation pension, Lump Sum on Death: None, Children’s Pension: None, Commutation Options: Available: Yes, maximum allowable under post 5 April 2006 legislation, Trivial Commutation Lump Sum Death Benefits: Yes, Guarantee Period: 5 years from the member’s retirement date.
    """
    
    query = "please extract criteria that we need to be able to provide to provide full pension scheme based on the information given, make it into the into json format with consie as possible use the below user data to create a pension scheme" + user_data
  

    try:
        ctx.logger.info(" Mapping Data to Fields..")
        response = query_with_cohere(msg.message,query)
        if not response:
            raise Exception("Failed to retrieve Response")
        
        await ctx.send( recommendationAgent.address, Message(message=response))
        ctx.logger.info(f"Response: {response}")
    
    except Exception as exc:
        ctx.logger.error(f"An error occured: {exc}")

@recommendationAgent.on_message(model=Message)
async def recommendationAgent_message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}")
    clients = """
    User Profile 1: John Smith
    Name: John Smith
    Gender: Male
    Date of Birth: 1st January 1960
    Age: 64
    Employment Details:
    Company: XYZ Ltd
    Joining Date: 2nd January 1980
    Leaving Date: 31st December 2015
    Years of Service: 35
    Average Salary: £80,000
    Spouse:
    Name: Jane Smith
    Age: 62
    Children: None
    Employment Status: Retired
    Health: Good
    Preferred Retirement Age: 65
    Scheme Enrollment Date: 15th June 1995
    Special Considerations: None
    User Profile 2: Sarah Johnson
    Name: Sarah Johnson
    Gender: Female
    Date of Birth: 10th June 1966
    Age: 58
    Employment Details:
    Company: ABC Corp
    Joining Date: 10th June 1990
    Leaving Date: Present
    Years of Service: 34
    Average Salary: £90,000
    Spouse:
    Name: Mark Johnson
    Age: 60
    Children:
    Child 1: Age 25, Independent
    Child 2: Age 22, Full-time education
    Employment Status: Employed
    Health: Moderate (minor health issues)
    Preferred Retirement Age: 60
    Scheme Enrollment Date: 10th June 1989
    Special Considerations: May need to consider early retirement due to health
    User Profile 3: Michael Brown
    Name: Michael Brown
    Gender: Male
    Date of Birth: 20th November 1953
    Age: 70
    Employment Details:
    Company: DEF Inc
    Joining Date: 20th November 1975
    Leaving Date: 30th November 2010
    Years of Service: 35
    Average Salary: £75,000
    Spouse: Deceased
    Children:
    Child 1: Age 30, Independent
    Employment Status: Retired
    Health: Good
    Preferred Retirement Age: 65
    Scheme Enrollment Date: 20th November 1975
    Special Considerations: None
    User Profile 4: Emily Davis
    Name: Emily Davis
    Gender: Female
    Date of Birth: 5th April 1969
    Age: 55
    Employment Details:
    Company: GHI Ltd
    Joining Date: 5th April 1985
    Leaving Date: Present
    Years of Service: 39
    Average Salary: £68,000
    Spouse:
    Name: Robert Davis
    Age: 55
    Children: None
    Employment Status: Employed
    Health: Good
    Preferred Retirement Age: 63
    Scheme Enrollment Date: 5th April 1985
    Special Considerations: Considering early retirement options
    User Profile 5: Robert Wilson
    Name: Robert Wilson
    Gender: Male
    Date of Birth: 12th July 1964
    Age: 60
    Employment Details:
    Company: JKL Corp
    Joining Date: 12th July 1995
    Leaving Date: Present
    Years of Service: 29
    Average Salary: £50,000
    Spouse:
    Name: Alice Wilson
    Age: 58
    Children:
    Child 1: Age 20, Full-time education
    Employment Status: Employed
    Health: Good
    Preferred Retirement Age: 65
    Scheme Enrollment Date: 12th July 1995
    Special Considerations: None
    User Profile 6: David Miller
    Name: David Miller
    Gender: Male
    Date of Birth: 20th March 1965
    Age: 59
    Employment Details:
    Company: MNO Ltd
    Joining Date: 20th March 1982
    Leaving Date: Present
    Years of Service: 42
    Average Salary: £95,000
    Spouse:
    Name: Laura Miller
    Age: 57
    Children:
    Child 1: Age 24, Independent
    Child 2: Age 18, Full-time education
    Employment Status: Employed
    """

    query_data = "clients data: " + clients + " pension data: " + msg.message

    query = """
    I have a list of client details and some information about pension schemes. Using the client data and pension scheme 
    I have given, list the criteria each person meets based on their details. Then calculate the fixed rate of pension increases and
    any other things you are able to calculate based on the data given. Use this percentage and other client details to calculate 
    a recommendation for the pension amount each client is entitiled to and how often they will be paid based on the pension criteria they meet. 
    It is important to refer to the specific pension scheme I have given and their percentages and details! The recommendation pension amount 
    must be a numerical value every time.
    """

    try:
        ctx.logger.info("Getting recommendations...")
        response = query_with_cohere(query_data,query)
        if not response:
            raise Exception("Failed to retrieve Response")
        
        ctx.logger.info(f"Response: {response}")
    
    except Exception as exc:
        ctx.logger.error(f"An error occured: {exc}")
    



bureau = Bureau()
bureau.add(requestAgent)
bureau.add(analysisAgent)
bureau.add(mappingAgent)
bureau.add(recommendationAgent)
 
if __name__ == "__main__":
    bureau.run()