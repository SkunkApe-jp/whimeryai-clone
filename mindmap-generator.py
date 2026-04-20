import json
import math
import os
import sys
from html import escape
from typing import Dict, List, Any
from pathlib import Path

try:
    import requests
except ImportError:
    print("Please install requests library: pip install requests")
    sys.exit(1)

try:
    from svgwrite import Drawing
    from svgwrite import shapes
except ImportError:
    print("Please install svgwrite library: pip install svgwrite")
    sys.exit(1)

CONFIG_FILE = "config.json"
APP_NAME = "Whimery"
OUTPUT_HTML_FILE = "whimery_output.html"

COLORS = [
    {"node": "#C084FC", "edge": "#C084FC", "leaf": "#E9D5FF", "text": "#581C87"},
    {"node": "#FDE047", "edge": "#FDE047", "leaf": "#FEF9C3", "text": "#713F12"},
    {"node": "#86EFAC", "edge": "#86EFAC", "leaf": "#DCFCE7", "text": "#14532D"},
    {"node": "#F9A8D4", "edge": "#F9A8D4", "leaf": "#FCE7F3", "text": "#831843"},
    {"node": "#67E8F9", "edge": "#67E8F9", "leaf": "#CFFAFE", "text": "#164E63"},
]

CENTER_COLOR = {"node": "#1E3A8A", "text": "#FFFFFF"}

def generate_mindmap_svg(data: Dict[str, Any], output_file: str = "mindmap.svg"):
    W, H = 700, 500
    cx, cy = W / 2, H / 2
    branchR = 155
    leafR = 100
    
    dwg = Drawing(output_file, size=(W, H))
    
    clusters = data.get("clusters", [])
    n = len(clusters)
    cluster_angles = [(2 * math.pi * i) / n - math.pi / 2 for i in range(n)]
    
    nodes = []
    edges = []
    
    for ci, cluster in enumerate(clusters):
        angle = cluster_angles[ci]
        color = COLORS[ci % len(COLORS)]
        bx = cx + branchR * math.cos(angle)
        by = cy + branchR * math.sin(angle)
        
        edges.append({"x1": cx, "y1": cy, "x2": bx, "y2": by, "color": color["edge"], "key": f"e-branch-{ci}"})
        nodes.append({"x": bx, "y": by, "label": cluster["name"], "type": "branch", "color": color, "key": f"branch-{ci}"})
        
        leaves = cluster.get("leaves", [])
        l_count = len(leaves)
        spread_angle = math.pi * 0.6
        
        for li, leaf in enumerate(leaves):
            offset = -spread_angle / 2 + (spread_angle / (l_count - 1)) * li if l_count > 1 else 0
            leaf_angle = angle + offset
            lx = bx + leafR * math.cos(leaf_angle)
            ly = by + leafR * math.sin(leaf_angle)
            
            edges.append({"x1": bx, "y1": by, "x2": lx, "y2": ly, "color": color["edge"], "key": f"e-leaf-{ci}-{li}"})
            nodes.append({"x": lx, "y": ly, "label": leaf, "type": "leaf", "color": color, "key": f"leaf-{ci}-{li}"})
    
    # Draw edges
    for edge in edges:
        dwg.add(dwg.line(
            start=(edge["x1"], edge["y1"]),
            end=(edge["x2"], edge["y2"]),
            stroke=edge["color"],
            stroke_width=6,
            stroke_linecap="round",
            opacity=0.85
        ))
    
    # Draw leaf nodes
    for node in nodes:
        if node["type"] == "leaf":
            w = max(len(node["label"]) * 9 + 24, 72)
            h = 36
            # Main rectangle
            dwg.add(dwg.rect(
                insert=(node["x"] - w / 2, node["y"] - h / 2),
                size=(w, h),
                rx=8,
                fill=node["color"]["leaf"],
                stroke=node["color"]["node"],
                stroke_width=2
            ))
            # Bottom accent
            dwg.add(dwg.rect(
                insert=(node["x"] - w / 2, node["y"] + h / 2 - 5),
                size=(w, 5),
                fill=node["color"]["node"],
                opacity=0.25
            ))
            # Text
            dwg.add(dwg.text(
                node["label"],
                insert=(node["x"], node["y"] + 1),
                text_anchor="middle",
                dominant_baseline="middle",
                font_size=14,
                font_family="Georgia, serif",
                fill=node["color"]["text"],
                font_weight="500"
            ))
    
    # Draw branch nodes
    for node in nodes:
        if node["type"] == "branch":
            dwg.add(dwg.circle(
                center=(node["x"], node["y"]),
                r=38,
                fill=node["color"]["node"],
                opacity=0.95
            ))
            dwg.add(dwg.text(
                node["label"],
                insert=(node["x"], node["y"]),
                text_anchor="middle",
                dominant_baseline="middle",
                font_size=13,
                font_family="Georgia, serif",
                fill="#111",
                font_weight="700"
            ))
    
    # Center node
    dwg.add(dwg.circle(
        center=(cx, cy),
        r=52,
        fill=CENTER_COLOR["node"]
    ))
    dwg.add(dwg.text(
        data.get("center", ""),
        insert=(cx, cy),
        text_anchor="middle",
        dominant_baseline="middle",
        font_size=15,
        font_family="Georgia, serif",
        fill=CENTER_COLOR["text"],
        font_weight="700"
    ))
    
    dwg.save()
    print(f"Mindmap saved as {output_file}")

def create_vocabulary_card_html(vocab: Dict[str, str]) -> str:
    POS_COLORS = {
        "adj": "#DBEAFE", "adv": "#D1FAE5", "noun": "#FEF3C7", "verb": "#FCE7F3",
    }
    pos_key = (vocab.get("pos", "")).lower()[:4]
    bg = POS_COLORS.get(pos_key, "#F3F4F6")
    
    html = f"""
    <div style="background: #fff; border-radius: 20px; padding: 32px 28px; box-shadow: 0 4px 24px rgba(0,0,0,0.06);">
        <div style="font-size: 58px; font-family: Georgia, serif; font-weight: 700; color: #1E3A8A; line-height: 1.1; letter-spacing: -1px; margin-bottom: 10px;">{vocab.get('word', '')}</div>
        
        <div style="font-size: 17px; color: #6B7EAA; font-family: monospace; margin-bottom: 14px; letter-spacing: 0.5px;">{vocab.get('ipa', '')}</div>
        
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 24px;">
            <span style="background: {bg}; border-radius: 6px; padding: 2px 10px; font-size: 13px; font-weight: 700; font-style: italic; color: #374151; font-family: Georgia, serif;">{vocab.get('pos', '')}.</span>
            <span style="font-size: 15px; color: #374151; font-family: Georgia, serif;">{vocab.get('definition', '')}</span>
        </div>
        
        <div style="position: relative; margin-bottom: 24px;">
            <div style="position: absolute; top: -14px; left: 50%; transform: translateX(-50%); background: #FDE68A; border-radius: 20px; padding: 4px 18px; font-size: 13px; font-weight: 700; color: #78350F; font-family: Georgia, serif; white-space: nowrap; z-index: 1;">Fun Fact</div>
            <div style="background: #EFF6FF; border-radius: 14px; padding: 22px 18px 16px; font-size: 15px; color: #374151; font-family: Georgia, serif; line-height: 1.65; text-align: center;">{vocab.get('funFact', '')}</div>
        </div>
        
        <div style="font-size: 15px; color: #6B7280; font-family: Georgia, serif; font-style: italic; text-align: center; border-top: 1px solid #F3F4F6; padding-top: 16px;">{vocab.get('example', '')}</div>
    </div>
    """
    return html

def create_visual_journey_card_html(journey: Dict[str, str]) -> str:
    html = f"""
    <div style="background: #fff; border-radius: 20px; padding: 32px 28px; box-shadow: 0 4px 24px rgba(0,0,0,0.06);">
        <h2 style="font-size: 22px; font-weight: 700; font-family: Georgia, serif; color: #1a1a2e; margin-bottom: 20px; margin-top: 0;">Visual Journey</h2>
        
        <p style="font-size: 16px; color: #374151; font-family: Georgia, serif; line-height: 1.85; margin: 0 0 24px; text-align: justify;">{journey.get('narrative', '')}</p>
        
        <div style="background: #DBEAFE; border-radius: 10px; padding: 14px 18px; font-size: 15px; font-weight: 600; color: #1E40AF; font-family: Georgia, serif; line-height: 1.55;">{journey.get('highlight', '')}</div>
    </div>
    """
    return html

def create_full_html_page(result: Dict[str, Any], source_text: str) -> str:
    safe_text = escape(source_text)
    word_count = len(source_text.split())
    mindmap_html = '<div class="card map-card"><img src="mindmap.svg" width="100%" /></div>'
    vocab_html = create_vocabulary_card_html(result.get("vocabulary", {}))
    journey_html = create_visual_journey_card_html(result.get("visualJourney", {}))
    
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{APP_NAME} - Text Analysis</title>
        <style>
            body {{
                min-height: 100vh;
                background: #F8F6F1;
                font-family: Georgia, serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 40px 20px 60px;
                margin: 0;
            }}
            .header {{
                text-align: center;
                margin-bottom: 32px;
            }}
            .header h1 {{
                font-size: 34px;
                font-weight: 700;
                color: #1a1a2e;
                letter-spacing: -0.5px;
                margin: 0;
            }}
            .header p {{
                font-size: 15px;
                color: #6B6B6B;
                margin-top: 6px;
                font-style: italic;
            }}
            .input-card {{
                width: 100%;
                max-width: 660px;
                background: #fff;
                border-radius: 16px;
                box-shadow: 0 4px 24px rgba(0,0,0,0.07);
                padding: 24px;
                margin-bottom: 28px;
                box-sizing: border-box;
            }}
            .source-text {{
                width: 100%;
                min-height: 130px;
                border: 1.5px solid #E2DDD8;
                border-radius: 10px;
                padding: 14px 16px;
                font-size: 15px;
                font-family: Georgia, serif;
                color: #2a2a2a;
                background: #FDFCFA;
                resize: vertical;
                outline: none;
                line-height: 1.65;
                box-sizing: border-box;
            }}
            .source-text[readonly] {{
                cursor: default;
            }}
            .toolbar {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-top: 14px;
            }}
            .word-count {{
                font-size: 13px;
                color: #aaa;
            }}
            .generate-button {{
                background: #1E3A8A;
                color: #fff;
                border: none;
                border-radius: 10px;
                padding: 10px 28px;
                font-size: 15px;
                font-family: Georgia, serif;
                font-weight: 600;
                cursor: default;
            }}
            .results {{
                width: 100%;
                max-width: 660px;
                display: flex;
                flex-direction: column;
                gap: 24px;
                animation: fadeUp 0.5s ease;
            }}
            .card {{
                background: #fff;
                border-radius: 20px;
                box-shadow: 0 4px 24px rgba(0,0,0,0.06);
            }}
            .map-card {{
                padding: 20px 12px;
            }}
            img {{
                display: block;
            }}
            @keyframes fadeUp {{
                from {{
                    opacity: 0;
                    transform: translateY(12px);
                }}
                to {{
                    opacity: 1;
                    transform: none;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>{APP_NAME}</h1>
            <p>Paste any text &mdash; get a mindmap, a word, and a journey</p>
        </div>

        <div class="input-card">
            <textarea class="source-text" readonly>{safe_text}</textarea>
            <div class="toolbar">
                <span class="word-count">{word_count} words</span>
                <button class="generate-button" type="button">Generate</button>
            </div>
        </div>

        <div class="results">
            {mindmap_html}
            {vocab_html}
            {journey_html}
        </div>
    </body>
    </html>
    """
    return full_html

def load_config() -> Dict[str, str]:
    """Load API configuration from config.json"""
    config_path = Path(CONFIG_FILE)
    
    if not config_path.exists():
        print(f"Error: {CONFIG_FILE} not found.")
        print(f"Please create a {CONFIG_FILE} file with your API settings.")
        print(f"See example.config.json for reference.")
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    required_keys = ['api_url', 'api_key', 'model']
    missing = [key for key in required_keys if key not in config]
    
    if missing:
        print(f"Error: Missing required config keys: {', '.join(missing)}")
        sys.exit(1)
    
    return config

def analyze_text(text: str, config: Dict[str, str]) -> Dict[str, Any]:
    if not text.strip():
        raise ValueError("Text cannot be empty")
    
    prompt = f"""Analyze the following text and return a JSON object with three sections. Return ONLY valid JSON, no markdown, no explanation, no code fences.

{{
  "mindmap": {{
    "center": "1-2 word core theme",
    "clusters": [
      {{ "name": "BranchWord", "leaves": ["Word1", "Word2", "Word3"] }},
      {{ "name": "BranchWord", "leaves": ["Word1", "Word2", "Word3"] }},
      {{ "name": "BranchWord", "leaves": ["Word1", "Word2", "Word3"] }}
    ]
  }},
  "vocabulary": {{
    "word": "one interesting or advanced word from the text",
    "ipa": "IPA pronunciation e.g. /ˈwɜːrd/",
    "pos": "adj or noun or verb or adv",
    "definition": "clear concise definition",
    "funFact": "one surprising or memorable fact about this word or its origin, 1-2 sentences",
    "example": "a natural example sentence using the word"
  }},
  "visualJourney": {{
    "narrative": "A vivid immersive 3-4 sentence narrative drawing the reader into the scene or subject, using sensory second-person language where possible",
    "highlight": "One interesting factual sentence from or related to the text, not repeating the narrative"
  }}
}}

Rules:
- mindmap: 3 clusters, 2-3 leaves each, evocative mood words not literal descriptors
- vocabulary: pick a non-trivial word, avoid the most common words
- English only, no emojis

Text:
\"\"\"
{text}
\"\"\""""
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config['api_key']}"
    }
    
    payload = {
        "model": config['model'],
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1500
    }
    
    response = requests.post(
        config['api_url'],
        headers=headers,
        json=payload
    )
    
    if response.status_code != 200:
        raise Exception(f"API request failed with status {response.status_code}: {response.text}")
    
    data = response.json()
    
    # Handle different response formats (OpenAI compatible)
    if 'choices' in data:
        raw = data['choices'][0].get('message', {}).get('content', '')
    elif 'content' in data:
        raw = "".join(block.get("text", "") for block in data.get("content", []))
    else:
        raise Exception("Unexpected API response format")
    
    clean = raw.replace("```json", "").replace("```", "").strip()
    
    return json.loads(clean)

def main():
    print(f"{APP_NAME} - Text Analysis Tool")
    print("=" * 40)
    
    # Load configuration
    config = load_config()
    print(f"Using model: {config['model']}")
    print(f"API endpoint: {config['api_url']}")
    
    # Get text input from user
    print("\nEnter the text you want to analyze (press Enter twice to finish):")
    lines = []
    empty_line_count = 0
    while True:
        try:
            line = input()
            if line == "":
                empty_line_count += 1
                if empty_line_count >= 1 and lines:  # End input after one empty line if we have content
                    break
            else:
                empty_line_count = 0
            lines.append(line)
        except EOFError:
            break
    
    text = "\n".join(lines).strip()
    if not text:
        print("No text provided. Exiting.")
        return
    
    print(f"\nAnalyzing text ({len(text.split())} words)...")
    
    try:
        result = analyze_text(text, config)
        
        # Generate SVG mindmap
        generate_mindmap_svg(result.get("mindmap", {}), "mindmap.svg")
        
        # Create HTML output
        html_content = create_full_html_page(result, text)
        with open(OUTPUT_HTML_FILE, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print("\nAnalysis complete!")
        print("Saved: mindmap.svg")
        print(f"Saved: {OUTPUT_HTML_FILE}")
        print(f"\nOpen {OUTPUT_HTML_FILE} in your browser to view the results.")
        
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        print("Please check your API configuration and try again.")

if __name__ == "__main__":
    main()
