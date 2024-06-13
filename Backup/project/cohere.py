from cohere import CohereClient

# Initialize Cohere client with your API key
cohere = CohereClient(api_key='Yqd4wQBcTH1dYkHYiEqOPY7Ac8rdrvrb2Cst2wLX')


# Sample text
text = "I really enjoy using Cohere's API for natural language processing!"

# # Analyze sentiment using Cohere
# response = cohere.sentiment(text)
# print(response)



response = CohereClient.some_method()