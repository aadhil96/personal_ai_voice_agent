# 🤖 Jarvis — Personal Voice AI Assistant
 
A conversational voice agent built with [LiveKit Agents](https://docs.livekit.io/agents/), powered by OpenAI and Deepgram. Jarvis listens, thinks, and speaks — with real-time web search via Exa.
 
---
 
## Features
 
- 🎙️ **Speech-to-text** — Deepgram Nova-3
- 🧠 **LLM** — OpenAI GPT-4.1-mini (configurable)
- 🔊 **Text-to-speech** — OpenAI TTS (`alloy` voice)
- 🌐 **Web search** — Exa search with content highlights
- 🕒 **Date & time** — live datetime tool
- 🔇 **Voice activity detection** — Silero VAD
 
---

## Configuration
 
Create a `.env` file in the project root:
 
```env
LIVEKIT_URL=wss://your-livekit-server.livekit.cloud
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_api_secret
 
OPENAI_API_KEY=your_openai_api_key
DEEPGRAM_API_KEY=your_deepgram_api_key
EXA_SEARCH_API_KEY=your_exa_api_key
 
# Optional: override the default LLM model
LLM_CHOICE=gpt-4.1-mini
```