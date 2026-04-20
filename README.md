# Whimery Python Clone

`Whimery Python Clone` is a small Python version of the JSX page in this repo. The goal is simple: keep the same soft, paper-toned look while generating the result as plain files from a Python script.

- a mindmap in SVG
- a vocabulary card for one strong word
- a short visual journey written by the model

## What It Makes

When you run the script, you get:

- `mindmap.svg` for the visual map
- `whimery_output.html` for the page with the same overall Whimery-style shell, the map, the word card, and the short narrative

## What You Need

- Python 3.7 or newer
- `requests`
- `svgwrite`
- access to an OpenAI-compatible chat endpoint

That endpoint can be OpenAI, Groq, LM Studio, Ollama, or anything else that speaks the same basic API shape.

## Setup

Install the two Python packages:

```powershell
pip install requests svgwrite
```

Copy the example config:

```powershell
Copy-Item example.config.json config.json
```

Then fill in `config.json`:

```json
{
  "api_url": "https://api.openai.com/v1/chat/completions",
  "api_key": "your-api-key-here",
  "model": "gpt-4o"
}
```

## Run It

```powershell
python .\mindmap-generator.py
```

Paste your text into the terminal.

Press `Enter` on a blank line to finish.

The script will call your model, build the map, and write the two output files into the project folder.

## Example Configs

OpenAI:

```json
{
  "api_url": "https://api.openai.com/v1/chat/completions",
  "api_key": "sk-...",
  "model": "gpt-4o"
}
```

Groq:

```json
{
  "api_url": "https://api.groq.com/openai/v1/chat/completions",
  "api_key": "gsk_...",
  "model": "llama-3.1-70b-versatile"
}
```

LM Studio:

```json
{
  "api_url": "http://localhost:1234/v1/chat/completions",
  "api_key": "not-needed",
  "model": "local-model"
}
```

Ollama:

```json
{
  "api_url": "http://localhost:11434/v1/chat/completions",
  "api_key": "not-needed",
  "model": "llama3"
}
```

## How It Works

1. You paste in a paragraph, page, poem, note, or passage.
2. The script sends that text to the configured model with a structured prompt.
3. The model returns JSON for the map, the vocabulary card, and the visual journey.
4. The script writes an SVG file and an HTML page shaped to match the JSX layout as closely as the Python flow allows.

## Project Files

```text
whimeryai-clone/
|-- mindmap-generator.py
|-- mindmap-generator.jsx
|-- example.config.json
|-- config.json
|-- .gitignore
`-- README.md
```

`mindmap-generator.jsx` is kept here as the earlier UI reference. The working tool in this repo is the Python script.

## A Small Note

Keep `config.json` out of version control. It holds your API key, and `.gitignore` is already set up to leave it alone.
