from uagents import Agent, Context
from uagents.setup import fund_agent_if_low

thanush = Agent(name='Thanush', seed="thanush agent phrase")
fund_agent_if_low(thanush.wallet.address())

@thanush.on_event('startup')
async def say_hello(ctx: Context):
    ctx.logger.info(f'hello, my name is {thanush.name}!')

@thanush.on_interval(period=2.0)
async def agent_interval(ctx: Context):
    ctx.logger.info(f'I am Thanush, I am alive! and my address is {thanush.address} and my wallet address is {thanush.wallet.address()}')
 
if __name__ == "__main__":
    thanush.run()