from dotenv import load_dotenv
from livekit import agents
from livekit.agents import Agent, AgentSession, RunContext
from livekit.agents.llm import function_tool
from livekit.plugins import openai, deepgram, silero
from datetime import datetime
from exa_py import Exa
import os

# Load environment variables
load_dotenv(".env")


class JarvisAssistant(Agent):

    def __init__(self):
        super().__init__(
            instructions="""
You are Jarvis, a highly intelligent, polite, and slightly witty AI assistant.

Your personality:
- Friendly, calm, and professional
- Slightly witty like Iron Man’s Jarvis
- Give concise but helpful answers
- Speak naturally as if in a conversation

Tool usage rules:
- Use web_search for current events, news, or unknown facts
- Use get_current_date_and_time when asked about time/date
- If unsure, search instead of guessing

Always prioritize accuracy and clarity.
"""
        )

        # Initialize Exa client
        self.exa = Exa(api_key=os.getenv("EXA_SEARCH_API_KEY"))

    @function_tool
    async def get_current_date_and_time(self, context: RunContext) -> str:
        """Get the current date and time."""
        current_datetime = datetime.now().strftime("%B %d, %Y at %I:%M %p")
        return f"The current date and time is {current_datetime}"

    @function_tool
    async def web_search(self, context: RunContext, query: str) -> str:
        """Search the web for up-to-date information."""
        try:
            print("Searching for:", query)

            await context.session.say("Let me check that for you...")

            results = self.exa.search_and_contents(
                query,
                num_results=3,
                type="auto",
                contents={"highlights": True}
            )

            summaries = []

            for r in results.results:
                text = r.text if hasattr(r, "text") and r.text else ""
                summaries.append(text[:300])

    
            combined = " ".join(summaries)

            return f"""
            Here is a clear summary of the latest information about {query}:{combined}

            Answer the user directly using this information. Do not call the tool again.
            """

        except Exception as e:
            return f"Search error: {str(e)}"


async def entrypoint(ctx: agents.JobContext):
    """Entry point for the agent."""

    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=openai.LLM(
            model=os.getenv("LLM_CHOICE", "gpt-4.1-mini"),
            temperature=0.7  # more natural responses
        ),
        tts=openai.TTS(voice="alloy"),  # safer voice
        vad=silero.VAD.load(),
    )

    # Start session
    await session.start(
        room=ctx.room,
        agent=JarvisAssistant()
    )

    # Initial greeting (Jarvis-style)
    await session.generate_reply(
        instructions="""
Say: Hello Boss, I'm Jarvis. Your personal AI assistant.
How may I assist you today?
"""
    )


if __name__ == "__main__":
    agents.cli.run_app(
        agents.WorkerOptions(entrypoint_fnc=entrypoint)
    )