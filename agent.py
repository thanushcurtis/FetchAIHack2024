from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
agent = Agent(name="alice", seed="secutyfjyret_seed_phrase")

fund_agent_if_low(agent.wallet.address())
 
@agent.on_event("startup")
async def introduce_agent(ctx: Context):
    ctx.logger.info(f"Hello, I'm agent {agent.name} and my address is {agent.address}.")
 
if __name__ == "__main__":
    agent.run()