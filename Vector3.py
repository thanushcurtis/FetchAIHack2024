from llama_index.core import VectorStoreIndex
from pathlib import Path
from langchain_cohere import ChatCohere
from langchain_cohere import  CohereEmbeddings
import cohere
from llama_index.readers.file import PDFReader
from llama_index.core import SimpleDirectoryReader

co = cohere.Client('0H1Q7mCc30QBBa5owiQ0Z9BmnlA7FhQmxcwBU7yj')

loader = SimpleDirectoryReader('C:\\Users\\pragb\\Documents\\Hack\\FetchAIHack2024\\Documents\\')
documents = loader.load_data()






# import nest_asyncio
# from llama_parse import LlamaParse
# from pathlib import Path

# nest_asyncio.apply()



# parser = LlamaParse(
#     api_key="llx-eUqQOa1ws1D2bswL0zO1RE5jX1B1daZuYwxCOQF9b732ZbAm",  # replace with your actual API key
#     result_type="markdown",
#     num_workers=4,
#     verbose=True,
#     language="en",
# )

# # sync
# documents = parser.load_data(Path('Documents/IBP.pdf'))


print("Number of documents loaded:", len(documents))

embeddings = CohereEmbeddings(cohere_api_key='0H1Q7mCc30QBBa5owiQ0Z9BmnlA7FhQmxcwBU7yj')

index = VectorStoreIndex.from_documents(documents, embed_model=embeddings)

# print(index)

cohere_api_key = '0H1Q7mCc30QBBa5owiQ0Z9BmnlA7FhQmxcwBU7yj' #keep your api key in the .env file and retrieve it
model = "command" #this is the model name from cohere. Select it that matches with you 
temperature = 0.9 # It can be range from (0-1) as openai
max_tokens = 40
llm = ChatCohere(model=model,temperature=0,cohere_api_key=cohere_api_key,max_tokens=max_tokens)

query_engine = index.as_query_engine(llm=llm)

query_results = query_engine.retrieve("What is in this document?")

#print("Query results:", query_results)

# Query with Cohere
def query_with_cohere(context, query):
    prompt = f"Context:\n{context}\n\nQuery:\n{query}\n\nPlease find the catergories and the each category's criteria. The criteria should have defined conditions"
    response = co.generate(
    model='command',
    prompt=prompt,
    )

    return response.generations[0].text

# Query with Cohere
def query_with_cohere1(context, query, response):
    prompt = f"Context:\n{context}\n\nQuery:\n{query}\n\nCan you provide me with a json response which has the number of people that fall under each category in {response} as the value and the category as the key?"
    response = co.generate(
    model='command',
    prompt=prompt,
    )

    return response.generations[0].text
#Please load the extracted data as a list
# Use query results as context
context_from_llama_index = query_results # Extract context from query_results
cohere_response = query_with_cohere(context_from_llama_index, "What are the scheme details in this document?")
print("Cohere's response:", cohere_response)
final_response = query_with_cohere1(context_from_llama_index, "What are the people's information in the document?", cohere_response)

