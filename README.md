# Whimery AI Clone

A text analysis tool that generates beautiful mindmaps, vocabulary cards, and visual journey narratives from any text using AI.

![Whimery Demo](screenshot.png)

## Features

✨ **Mindmap Generation** - Creates a visual mindmap with clusters and leaves from your text  
📚 **Vocabulary Card** - Extracts interesting words with definitions, IPA pronunciation, and fun facts  
🎨 **Visual Journey** - Generates an immersive narrative that brings your text to life  

## Tech Stack

- **Python 3.x**
- **svgwrite** - SVG mindmap generation
- **requests** - API communication
- **OpenAI-compatible APIs** - Works with OpenAI, Groq, LM Studio, Ollama, and more

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SkunkApe-jp/whimeryai-clone.git
cd whimeryai-clone
```

2. Install dependencies:
```bash
pip install requests svgwrite
```

3. Create your configuration file:
```bash
cp example.config.json config.json
```

4. Edit `config.json` with your API credentials:
```json
{
  "api_url": "https://api.openai.com/v1/chat/completions",
  "api_key": "your-api-key-here",
  "model": "gpt-4o"
}
```

## Usage

Run the script:
```bash
python mindmap-generator.py
```

1. Enter the text you want to analyze
2. Press Enter twice to finish input
3. Wait for AI analysis
4. View the results in the generated files:
   - `mindmap.svg` - Visual mindmap
   - `whimery_output.html` - Complete HTML report

## Configuration Examples

### OpenAI
```json
{
  "api_url": "https://api.openai.com/v1/chat/completions",
  "api_key": "sk-...",
  "model": "gpt-4o"
}
```

### Groq
```json
{
  "api_url": "https://api.groq.com/openai/v1/chat/completions",
  "api_key": "gsk_...",
  "model": "llama-3.1-70b-versatile"
}
```

### LM Studio (Local)
```json
{
  "api_url": "http://localhost:1234/v1/chat/completions",
  "api_key": "not-needed",
  "model": "local-model"
}
```

### Ollama (Local)
```json
{
  "api_url": "http://localhost:11434/v1/chat/completions",
  "api_key": "not-needed",
  "model": "llama3"
}
```

## Project Structure

```
whimeryai-clone/
├── mindmap-generator.py      # Main Python script
├── config.json               # Your API configuration (gitignored)
├── example.config.json       # Example configuration
├── mindmap-generator.jsx     # Original React version
├── mindmap-generator_1.jsx   # Original React version
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Output Files

After running the script, you'll get:

- **mindmap.svg** - A beautiful SVG mindmap visualization
- **whimery_output.html** - A complete HTML report containing:
  - Mindmap visualization
  - Vocabulary card with word details
  - Visual journey narrative

## How It Works

1. **Input**: Paste any text (paragraph, quote, poem, etc.)
2. **AI Analysis**: The script sends your text to an AI model with a structured prompt
3. **Processing**: AI returns JSON with mindmap data, vocabulary, and narrative
4. **Output Generation**: 
   - SVG mindmap is created using svgwrite
   - HTML report is generated with styled cards
5. **Results**: Open the HTML file in your browser to view everything

## Security Note

⚠️ **Never commit your `config.json` file!** It contains your API keys. The `.gitignore` file is configured to exclude it automatically.

## Requirements

- Python 3.7+
- requests library
- svgwrite library
- Access to an OpenAI-compatible API

## License

MIT License - feel free to use and modify as needed!

## Original Project

This is a Python conversion of the original React/JSX Whimery AI application, converted to work as a standalone command-line tool with flexible API support.
