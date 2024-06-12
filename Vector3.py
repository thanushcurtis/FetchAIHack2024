from llama_index.core import VectorStoreIndex
from pathlib import Path
from langchain_cohere import ChatCohere
from langchain_cohere import  CohereEmbeddings
import cohere
from llama_index.readers.file import PDFReader


co = cohere.Client('0H1Q7mCc30QBBa5owiQ0Z9BmnlA7FhQmxcwBU7yj')

loader = PDFReader()
documents = loader.load_data(file=Path('DA/bayes.pdf'))

print("Number of documents loaded:", len(documents))

embeddings = CohereEmbeddings(cohere_api_key='0H1Q7mCc30QBBa5owiQ0Z9BmnlA7FhQmxcwBU7yj')

index = VectorStoreIndex.from_documents(documents, embed_model=embeddings)

print(index)

cohere_api_key = '0H1Q7mCc30QBBa5owiQ0Z9BmnlA7FhQmxcwBU7yj' #keep your api key in the .env file and retrieve it
model = "command" #this is the model name from cohere. Select it that matches with you 
temperature = 0 # It can be range from (0-1) as openai
max_tokens = 256
llm = ChatCohere(model=model,temperature=0,cohere_api_key=cohere_api_key,max_tokens=max_tokens)

query_engine = index.as_query_engine(llm=llm)

query_results = query_engine.retrieve("What is in this document?")

# Query with Cohere
def query_with_cohere(context, query):
    prompt = f"Context: {context}\nQuery: {query}\nAnswer:" 
    response = co.generate(
    model='command',
    prompt=prompt,
    max_tokens=50
    )

    return response.generations[0].text

# Use query results as context
context_from_llama_index = query_results # Extract context from query_results
cohere_response = query_with_cohere(context_from_llama_index, "What is in this document?")
print("Cohere's response:", cohere_response)