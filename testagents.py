import unittest
from unittest.mock import patch, AsyncMock
from uagents import Agent, Context, Model
import asyncio

# Define the message model
class Message(Model):
    message: str

# Define the agents
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
    seed='mappingAgent secret phrase'
)
recommendationAgent = Agent(
    name="recommendationAgent",
    seed="recommendationAgent secret phrase"
)

# Dummy function to simulate Cohere query
def query_with_cohere(context, query):
    return " response from Cohere"

# Define agent event handlers
@requestAgent.on_event('startup')
async def send_message(ctx: Context):
    await ctx.send(analysisAgent.address, Message(message="hello there I'm requestAgent"))

@analysisAgent.on_event('startup')
async def say_hello(ctx: Context):
    ctx.logger.info(f'hello, my name is {analysisAgent.name} and and my address is {analysisAgent.address}!')

@analysisAgent.on_message(model=Message)
async def analysisAgent_message_handle(ctx: Context, sender: str, msg: Message):
    query = "Summarize this document into key parts such as rules, types and dates"
    response = query_with_cohere("context_from_llama_index", query)
    await ctx.send(mappingAgent.address, Message(message=response))

@mappingAgent.on_message(model=Message)
async def mappingAgent_message_handler(ctx: Context, sender: str, msg: Message):
    query = "Transform this into JSON format."
    response = query_with_cohere(msg.message, query)
    await ctx.send(recommendationAgent.address, Message(message=response))

# Define unit tests
class TestAgentInteractions(unittest.TestCase):


    #setup 
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.mock_context = AsyncMock(Context)
        self.sender = "test_sender_address"

    # Test Cohere query
    @patch('__main__.query_with_cohere', side_effect=query_with_cohere)
    def test_cohere_query(self, mock_query_with_cohere):
        response = query_with_cohere("context", "query")
        self.assertEqual(response, "Mocked response from Cohere")

    # Test agent can startup or not
    @patch('uagents.Context.send', new_callable=AsyncMock)
    async def test_request_agent_startup(self, mock_send):
        await send_message(self.mock_context)
        mock_send.assert_called_with(
            analysisAgent.address,
            Message(message="hello there I'm requestAgent")
        )

    # test names matching or not using logger
    @patch('uagents.Context.logger')
    async def test_analysis_agent_startup(self, mock_logger):
        await say_hello(self.mock_context)
        mock_logger.info.assert_called_with(
            f'hello, my name is {analysisAgent.name} and and my address is {analysisAgent.address}!'
        )

    def tearDown(self):
        self.loop.close()
        asyncio.set_event_loop(None)

if __name__ == '__main__':
    unittest.main()
