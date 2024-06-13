from uagents import Agent, Context, Model

 
class Message(Model):
    message: str
 
RECIPIENT_ADDRESS="agent1qvshnse5680dlthrzygny3y9nvvvvsdl8t7hr6f78jy3d59645j8qateu70"
 
requestAgent = Agent(
    name="requestAgent",
    port=8000,
    seed="requestAgent secret phrase",
    endpoint=["http://127.0.0.1:8000/submit"],
)
 

 
@requestAgent.on_event('startup')
async def send_message(ctx: Context):
     ctx.logger.info(f'hello, my name is {requestAgent.name} and and my address is {requestAgent.address}!')

@requestAgent.on_interval(period=10.0)
async def send_message(ctx: Context):
    ctx.logger.info("hi")
    await ctx.send(RECIPIENT_ADDRESS, Message(message="hello there I'm requestAgent"))
    ctx.logger.info("message sent")
 
@requestAgent.on_message(model=Message)
async def message_handler(ctx: Context, sender: str, msg: Message):
    ctx.logger.info(f"Received message from {sender}: {msg.message}")
 
if __name__ == "__main__":
    requestAgent.run()