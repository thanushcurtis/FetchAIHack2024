from uagents import Agent, Context, Model, Protocol
from uagents.setup import fund_agent_if_low
import requests
from ai_engine import UAgentResponse, UAgentResponseType
from llama_index.core import VectorStoreIndex
from pathlib import Path
from langchain_cohere import ChatCohere
from langchain_cohere import  CohereEmbeddings
import cohere
from llama_index.readers.file import PDFReader

class documentAnalysis(Model):
    query: str

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
    port=8080,
    seed="DocAnalysis agent phrase",
    endpoint=["http://127.0.0.1:8080/"],
)



analysis_protocol = Protocol("Document Summarizer")

@analysisAgent.on_event('startup')
async def say_hello(ctx: Context):
    ctx.logger.info(f'hello, my name is {analysisAgent.name} and and my address is {analysisAgent.address}!')
    # #ctx.logger.info(f"Received the question from the user {sender}.")[]
    # query = "Summarize this document into key parts such as rules, types and dates which as understanble by laymen"

    # try:
    #     ctx.logger.info(" Loading the Document..")
    #     ctx.logger.info(" Document Loaded Succesfully..")
    #     response = query_with_cohere(context_from_llama_index,query)
    #     if not response:
    #         raise Exception("Failed to retrieve Response")
        
        
    #     ctx.logger.info(f"Response: {response}")
    
    # except Exception as exc:
    #     ctx.logger.error(f"An error occured: {exc}")
    
@analysisAgent.on_message(model=documentAnalysis, replies=UAgentResponse)
async def on_message(ctx: Context, sender: str, msg:documentAnalysis):
    ctx.logger.info(f"Received the question from the user {sender}.")
    query = "Summarize this document into key parts such as rules, types and dates"

    try:
        ctx.logger.info(" Loading the Document..")
        ctx.logger.info(" Document Loaded Succesfully..")
        response = query_with_cohere(context_from_llama_index,query)
        if not response:
            raise Exception("Failed to retrieve Response")
        
        await ctx.send(
            sender,
            UAgentResponse(
                message=response,
                type=UAgentResponseType.FINAL
            )
        )
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


analysisAgent.include(analysis_protocol)



if __name__ == "__main__":
    analysisAgent.run()