import asyncio
import sys
import traceback

from beeai_framework.agents.react import ReActAgent, ReActAgentRunOutput
from beeai_framework.backend import ChatModel
from beeai_framework.errors import FrameworkError
from beeai_framework.logger import Logger
from beeai_framework.memory import UnconstrainedMemory


async def main() -> None:
    logger = Logger("app", level="TRACE")

    agent = ReActAgent(llm=ChatModel.from_name("ollama:granite3.3:8b"), tools=[], memory=UnconstrainedMemory())

    output: ReActAgentRunOutput = await agent.run("Hello!").observe(
        lambda emitter: emitter.on(
            "update", lambda data, event: logger.info(f"Event {event.path} triggered by {type(event.creator).__name__}")
        )
    )

    logger.info(f"Agent 🤖 : {output.result.text}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())
