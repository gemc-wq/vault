# TTS Recommendation: edge-tts
**From:** Athena (via Cem) | **Date:** 2026-04-09

## Summary
For any text-to-speech needs, use **edge-tts** — Microsoft Edge browser's TTS engine as a Python library.

## Why
- **Free** — no API key, no rate limits, no cost
- **High quality** — neural voices, natural sounding
- **Simple** — `pip install edge-tts`, async native
- **Flexible** — dozens of voices and languages

## Voice We Use
`en-GB-SoniaNeural` (British female, rate="+10%")

## Basic Usage
```python
import edge_tts, asyncio

async def speak(text, output_path="output.mp3"):
    comm = edge_tts.Communicate(text, "en-GB-SoniaNeural", rate="+10%")
    await comm.save(output_path)

asyncio.run(speak("Hello world"))
```

## For Telegram Voice (OGG/Opus)
```bash
ffmpeg -y -i output.mp3 -c:a libopus -b:a 64k output.ogg
```

## Use Cases
- Agent voice responses (Telegram, Slack)
- Audio reports and briefs
- Presentation narration
- Alert notifications
