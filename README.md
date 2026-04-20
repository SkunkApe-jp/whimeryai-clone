# Ars Verborum

Paste any text and generate three learning outputs in the browser: a mindmap, a vocabulary card, and a short visual journey.

## What It Makes

- A colorful **mindmap** in SVG with clustered branches and leaves
- A **vocabulary card** highlighting one interesting word (with IPA, definition, fun fact, and example)
- A **visual journey** — a vivid narrative and a factual highlight

## How to Use

1. Open `index.html` in any modern browser.
2. Click the **gear icon** (top-right) to open AI settings.
3. Choose a provider and enter your **API URL**, **API key**, and **model**, then click Save. Settings are stored in browser `localStorage`.
4. Paste text into the input and click **Generate**.

## Providers

Two provider modes are supported:

- **Anthropic** — uses the Messages API with `x-api-key` + `anthropic-version` headers.
  - Default URL: `https://api.anthropic.com/v1/messages`
  - Default model: `claude-sonnet-4-20250514`
- **OpenAI-compatible** — uses `Authorization: Bearer <key>` with the Chat Completions schema. Works with OpenAI, and any compatible endpoint (Together, Groq, OpenRouter, local servers like Ollama or LM Studio, etc.).
  - Default URL: `https://api.openai.com/v1/chat/completions`
  - Default model: `gpt-4o-mini`

Switching provider in the modal auto-fills the matching defaults; you can still override the URL and model by hand.

## Project Files

```text
project-root/
|-- index.html
`-- README.md
```

The working tool is `index.html`.
