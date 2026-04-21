# Ava - iMac Clawdbot Setup Guide

## Overview

Install a second Clawdbot instance on Cem's iMac with:
- **Primary Model:** GPT 5.2 (via Venice or OpenRouter)
- **Secondary Model:** Kimi K2.5 (via Venice or OpenRouter)
- **Voice:** en-US-JennyNeural (US female)
- **Persona:** Silicon Valley product strategist / devil's advocate

## Prerequisites

- [ ] Venice AI API key OR OpenRouter API key
- [ ] Node.js installed on iMac (already have via clawdbot user)
- [ ] Telegram bot token for Ava (create new bot via @BotFather)

---

## Step 1: Get API Key

### Option A: Venice AI (Recommended)
1. Go to [venice.ai](https://venice.ai)
2. Sign up / Log in
3. Settings → API Keys → Create new key
4. Copy key (format: `vapi_xxxxxxxxxxxx`)

### Option B: OpenRouter
1. Go to [openrouter.ai](https://openrouter.ai)
2. Sign up / Log in
3. Keys → Create Key
4. Copy key (format: `sk-or-v1-xxxxxxxxxxxx`)

---

## Step 2: Create Telegram Bot for Ava

1. Open Telegram, message @BotFather
2. Send `/newbot`
3. Name: `Ava` (or `Ava - Ecell Assistant`)
4. Username: `ecell_ava_bot` (must be unique, end with `bot`)
5. Copy the bot token

---

## Step 3: Install Clawdbot on iMac

Run on the iMac terminal:

```bash
# Create Ava's workspace
mkdir -p ~/ava-workspace
cd ~/ava-workspace

# Initialize clawdbot for Ava
clawdbot init

# Or if clawdbot not in path:
# /usr/local/bin/clawdbot init
```

---

## Step 4: Configure Ava

### Run onboard wizard:

**For Venice:**
```bash
clawdbot onboard --auth-choice venice-api-key
```

**For OpenRouter:**
```bash
clawdbot onboard --auth-choice openrouter
```

### Set default model:

**For Venice:**
```bash
clawdbot models set venice/gpt-5.2
# or for Kimi:
clawdbot models set venice/kimi-k2-thinking
```

**For OpenRouter:**
```bash
clawdbot models set openrouter/openai/gpt-5.2
# or for Kimi:
clawdbot models set openrouter/moonshot/kimi-k2.5
```

---

## Step 5: Configure Telegram

```bash
clawdbot configure
# Select: Channels → Telegram
# Enter bot token from Step 2
# Set DM policy: pairing
# Add Cem's Telegram ID to allowlist: 5587457906
```

Or manually edit `~/.clawdbot/clawdbot.json`:

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "botToken": "YOUR_AVA_BOT_TOKEN",
      "dmPolicy": "pairing"
    }
  }
}
```

---

## Step 6: Configure TTS Voice

Edit `~/.clawdbot/clawdbot.json`:

```json
{
  "messages": {
    "tts": {
      "auto": "off",
      "provider": "edge",
      "edge": {
        "enabled": true,
        "voice": "en-US-JennyNeural",
        "lang": "en-US",
        "rate": "+0%",
        "pitch": "+0%"
      }
    }
  }
}
```

---

## Step 7: Set Up Workspace Files

Copy the workspace files to Ava's directory:

```bash
cd ~/ava-workspace

# Copy SOUL.md (from Harry's prep)
# Copy AGENTS.md, USER.md etc.
```

Or Harry can sync them via Google Drive:
- Location: `Clawdbot Shared Folder/ava-setup/`

---

## Step 8: Start Ava

```bash
cd ~/ava-workspace
clawdbot gateway start
```

Or install as service:
```bash
clawdbot gateway install
clawdbot gateway start
```

---

## Step 9: Pair with Cem

1. Open Telegram
2. Find Ava's bot (the one you created)
3. Send `/start`
4. Ava will prompt for pairing approval

---

## Communication Between Harry & Ava

### Option A: Shared Workspace (Google Drive)
Both agents read/write to `Clawdbot Shared Folder/collaboration/`

### Option B: Direct Sessions
Configure cross-gateway sessions (advanced)

### Option C: Telegram Group
Create a group with both bots + Cem for three-way collaboration

---

## Quick Reference

| Setting | Value |
|---------|-------|
| Workspace | `~/ava-workspace` |
| Primary Model | GPT 5.2 (Venice/OpenRouter) |
| Secondary Model | Kimi K2.5 |
| Voice | en-US-JennyNeural |
| Persona | Devil's advocate, data-driven |
| Telegram Bot | @ecell_ava_bot (or your chosen name) |

---

*Setup guide prepared by Harry - 2026-02-01*
