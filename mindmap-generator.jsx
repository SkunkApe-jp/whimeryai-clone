import { useState, useRef } from "react";

const COLORS = [
  { node: "#C084FC", edge: "#C084FC", leaf: "#E9D5FF", text: "#581C87" },
  { node: "#FDE047", edge: "#FDE047", leaf: "#FEF9C3", text: "#713F12" },
  { node: "#86EFAC", edge: "#86EFAC", leaf: "#DCFCE7", text: "#14532D" },
  { node: "#F9A8D4", edge: "#F9A8D4", leaf: "#FCE7F3", text: "#831843" },
  { node: "#67E8F9", edge: "#67E8F9", leaf: "#CFFAFE", text: "#164E63" },
];

const CENTER_COLOR = { node: "#1E3A8A", text: "#FFFFFF" };

function MindmapSVG({ data }) {
  const W = 700, H = 500;
  const cx = W / 2, cy = H / 2;
  const branchR = 155;
  const leafR = 100;

  const clusters = data.clusters || [];
  const n = clusters.length;
  const clusterAngles = clusters.map((_, i) => (2 * Math.PI * i) / n - Math.PI / 2);

  const nodes = [];
  const edges = [];

  clusters.forEach((cluster, ci) => {
    const angle = clusterAngles[ci];
    const color = COLORS[ci % COLORS.length];
    const bx = cx + branchR * Math.cos(angle);
    const by = cy + branchR * Math.sin(angle);

    edges.push({ x1: cx, y1: cy, x2: bx, y2: by, color: color.edge, key: `e-branch-${ci}` });
    nodes.push({ x: bx, y: by, label: cluster.name, type: "branch", color, key: `branch-${ci}` });

    const leaves = cluster.leaves || [];
    const lCount = leaves.length;
    const spreadAngle = Math.PI * 0.6;
    leaves.forEach((leaf, li) => {
      const offset = lCount > 1 ? -spreadAngle / 2 + (spreadAngle / (lCount - 1)) * li : 0;
      const leafAngle = angle + offset;
      const lx = bx + leafR * Math.cos(leafAngle);
      const ly = by + leafR * Math.sin(leafAngle);

      edges.push({ x1: bx, y1: by, x2: lx, y2: ly, color: color.edge, key: `e-leaf-${ci}-${li}` });
      nodes.push({ x: lx, y: ly, label: leaf, type: "leaf", color, key: `leaf-${ci}-${li}` });
    });
  });

  return (
    <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ overflow: "visible" }}>
      {edges.map(e => (
        <line key={e.key} x1={e.x1} y1={e.y1} x2={e.x2} y2={e.y2}
          stroke={e.color} strokeWidth={6} strokeLinecap="round" opacity={0.85} />
      ))}
      {nodes.filter(n => n.type === "leaf").map(n => {
        const w = Math.max(n.label.length * 9 + 24, 72);
        const h = 36;
        return (
          <g key={n.key}>
            <rect x={n.x - w / 2} y={n.y - h / 2} width={w} height={h} rx={8}
              fill={n.color.leaf} stroke={n.color.node} strokeWidth={2} />
            <rect x={n.x - w / 2} y={n.y + h / 2 - 5} width={w} height={5}
              fill={n.color.node} opacity={0.25} />
            <text x={n.x} y={n.y + 1} textAnchor="middle" dominantBaseline="middle"
              fontSize={14} fontFamily="Georgia, serif" fill={n.color.text} fontWeight="500">
              {n.label}
            </text>
          </g>
        );
      })}
      {nodes.filter(n => n.type === "branch").map(n => (
        <g key={n.key}>
          <circle cx={n.x} cy={n.y} r={38} fill={n.color.node} opacity={0.95} />
          <text x={n.x} y={n.y} textAnchor="middle" dominantBaseline="middle"
            fontSize={13} fontFamily="Georgia, serif" fill="#111" fontWeight="700">
            {n.label}
          </text>
        </g>
      ))}
      <circle cx={cx} cy={cy} r={52} fill={CENTER_COLOR.node} />
      <text x={cx} y={cy} textAnchor="middle" dominantBaseline="middle"
        fontSize={15} fontFamily="Georgia, serif" fill={CENTER_COLOR.text} fontWeight="700">
        {data.center}
      </text>
    </svg>
  );
}

function VocabularyCard({ vocab }) {
  const POS_COLORS = {
    adj: "#DBEAFE", adv: "#D1FAE5", noun: "#FEF3C7", verb: "#FCE7F3",
  };
  const posKey = (vocab.pos || "").toLowerCase().slice(0, 4);
  const bg = POS_COLORS[posKey] || "#F3F4F6";

  return (
    <div style={{
      background: "#fff",
      borderRadius: 20,
      padding: "32px 28px",
      boxShadow: "0 4px 24px rgba(0,0,0,0.06)",
    }}>
      <div style={{
        fontSize: 58,
        fontFamily: "Georgia, serif",
        fontWeight: 700,
        color: "#1E3A8A",
        lineHeight: 1.1,
        letterSpacing: "-1px",
        marginBottom: 10,
      }}>{vocab.word}</div>

      <div style={{
        fontSize: 17,
        color: "#6B7EAA",
        fontFamily: "monospace",
        marginBottom: 14,
        letterSpacing: "0.5px",
      }}>{vocab.ipa}</div>

      <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 24 }}>
        <span style={{
          background: bg,
          borderRadius: 6,
          padding: "2px 10px",
          fontSize: 13,
          fontWeight: 700,
          fontStyle: "italic",
          color: "#374151",
          fontFamily: "Georgia, serif",
        }}>{vocab.pos}.</span>
        <span style={{ fontSize: 15, color: "#374151", fontFamily: "Georgia, serif" }}>
          {vocab.definition}
        </span>
      </div>

      <div style={{ position: "relative", marginBottom: 24 }}>
        <div style={{
          position: "absolute",
          top: -14,
          left: "50%",
          transform: "translateX(-50%)",
          background: "#FDE68A",
          borderRadius: 20,
          padding: "4px 18px",
          fontSize: 13,
          fontWeight: 700,
          color: "#78350F",
          fontFamily: "Georgia, serif",
          whiteSpace: "nowrap",
          zIndex: 1,
        }}>Fun Fact</div>
        <div style={{
          background: "#EFF6FF",
          borderRadius: 14,
          padding: "22px 18px 16px",
          fontSize: 15,
          color: "#374151",
          fontFamily: "Georgia, serif",
          lineHeight: 1.65,
          textAlign: "center",
        }}>{vocab.funFact}</div>
      </div>

      <div style={{
        fontSize: 15,
        color: "#6B7280",
        fontFamily: "Georgia, serif",
        fontStyle: "italic",
        textAlign: "center",
        borderTop: "1px solid #F3F4F6",
        paddingTop: 16,
      }}>{vocab.example}</div>
    </div>
  );
}

function VisualJourneyCard({ journey }) {
  return (
    <div style={{
      background: "#fff",
      borderRadius: 20,
      padding: "32px 28px",
      boxShadow: "0 4px 24px rgba(0,0,0,0.06)",
    }}>
      <h2 style={{
        fontSize: 22,
        fontWeight: 700,
        fontFamily: "Georgia, serif",
        color: "#1a1a2e",
        marginBottom: 20,
        marginTop: 0,
      }}>Visual Journey</h2>

      <p style={{
        fontSize: 16,
        color: "#374151",
        fontFamily: "Georgia, serif",
        lineHeight: 1.85,
        margin: "0 0 24px",
        textAlign: "justify",
      }}>{journey.narrative}</p>

      <div style={{
        background: "#DBEAFE",
        borderRadius: 10,
        padding: "14px 18px",
        fontSize: 15,
        fontWeight: 600,
        color: "#1E40AF",
        fontFamily: "Georgia, serif",
        lineHeight: 1.55,
      }}>{journey.highlight}</div>
    </div>
  );
}

export default function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function generate() {
    if (!text.trim()) return;
    setLoading(true);
    setError("");
    setResult(null);

    const prompt = `Analyze the following text and return a JSON object with three sections. Return ONLY valid JSON, no markdown, no explanation, no code fences.

{
  "mindmap": {
    "center": "1-2 word core theme",
    "clusters": [
      { "name": "BranchWord", "leaves": ["Word1", "Word2", "Word3"] },
      { "name": "BranchWord", "leaves": ["Word1", "Word2", "Word3"] },
      { "name": "BranchWord", "leaves": ["Word1", "Word2", "Word3"] }
    ]
  },
  "vocabulary": {
    "word": "one interesting or advanced word from the text",
    "ipa": "IPA pronunciation e.g. /ˈwɜːrd/",
    "pos": "adj or noun or verb or adv",
    "definition": "clear concise definition",
    "funFact": "one surprising or memorable fact about this word or its origin, 1-2 sentences",
    "example": "a natural example sentence using the word"
  },
  "visualJourney": {
    "narrative": "A vivid immersive 3-4 sentence narrative drawing the reader into the scene or subject, using sensory second-person language where possible",
    "highlight": "One interesting factual sentence from or related to the text, not repeating the narrative"
  }
}

Rules:
- mindmap: 3 clusters, 2-3 leaves each, evocative mood words not literal descriptors
- vocabulary: pick a non-trivial word, avoid the most common words
- English only, no emojis

Text:
"""
${text}
"""`;

    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1500,
          messages: [{ role: "user", content: prompt }],
        }),
      });

      const data = await res.json();
      const raw = data.content?.map(b => b.text || "").join("") || "";
      const clean = raw.replace(/```json|```/g, "").trim();
      const parsed = JSON.parse(clean);
      setResult(parsed);
    } catch (e) {
      setError("Could not generate. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={{
      minHeight: "100vh",
      background: "#F8F6F1",
      fontFamily: "Georgia, serif",
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      padding: "40px 20px 60px",
    }}>
      <div style={{ textAlign: "center", marginBottom: 32 }}>
        <h1 style={{
          fontSize: 34,
          fontWeight: 700,
          color: "#1a1a2e",
          letterSpacing: "-0.5px",
          margin: 0,
        }}>Whimery</h1>
        <p style={{
          fontSize: 15,
          color: "#6B6B6B",
          marginTop: 6,
          fontStyle: "italic",
        }}>Paste any text — get a mindmap, a word, and a journey</p>
      </div>

      <div style={{
        width: "100%",
        maxWidth: 660,
        background: "#fff",
        borderRadius: 16,
        boxShadow: "0 4px 24px rgba(0,0,0,0.07)",
        padding: "24px",
        marginBottom: 28,
      }}>
        <textarea
          value={text}
          onChange={e => setText(e.target.value)}
          placeholder="Paste a paragraph, quote, poem, or any text..."
          style={{
            width: "100%",
            minHeight: 130,
            border: "1.5px solid #E2DDD8",
            borderRadius: 10,
            padding: "14px 16px",
            fontSize: 15,
            fontFamily: "Georgia, serif",
            color: "#2a2a2a",
            background: "#FDFCFA",
            resize: "vertical",
            outline: "none",
            lineHeight: 1.65,
            boxSizing: "border-box",
          }}
          onFocus={e => e.target.style.borderColor = "#A78BFA"}
          onBlur={e => e.target.style.borderColor = "#E2DDD8"}
        />
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginTop: 14 }}>
          <span style={{ fontSize: 13, color: "#aaa" }}>
            {text.length > 0 ? `${text.split(/\s+/).filter(Boolean).length} words` : ""}
          </span>
          <button
            onClick={generate}
            disabled={loading || !text.trim()}
            style={{
              background: loading || !text.trim() ? "#C4B5FD" : "#1E3A8A",
              color: "#fff",
              border: "none",
              borderRadius: 10,
              padding: "10px 28px",
              fontSize: 15,
              fontFamily: "Georgia, serif",
              fontWeight: 600,
              cursor: loading || !text.trim() ? "not-allowed" : "pointer",
              transition: "background 0.2s",
            }}
          >
            {loading ? "Thinking..." : "Generate"}
          </button>
        </div>
      </div>

      {error && (
        <p style={{ color: "#DC2626", fontSize: 14, marginBottom: 16 }}>{error}</p>
      )}

      {loading && (
        <div style={{
          width: "100%", maxWidth: 660, height: 180,
          background: "#fff", borderRadius: 20,
          boxShadow: "0 4px 24px rgba(0,0,0,0.06)",
          display: "flex", alignItems: "center", justifyContent: "center",
          flexDirection: "column", gap: 12,
        }}>
          <div style={{
            width: 40, height: 40,
            border: "4px solid #E9D5FF",
            borderTop: "4px solid #7C3AED",
            borderRadius: "50%",
            animation: "spin 1s linear infinite",
          }} />
          <p style={{ color: "#9CA3AF", fontSize: 14, fontStyle: "italic", margin: 0 }}>
            Reading between the lines...
          </p>
          <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
        </div>
      )}

      {result && !loading && (
        <div style={{
          width: "100%",
          maxWidth: 660,
          display: "flex",
          flexDirection: "column",
          gap: 24,
          animation: "fadeUp 0.5s ease",
        }}>
          <div style={{
            background: "#fff",
            borderRadius: 20,
            padding: "20px 12px",
            boxShadow: "0 4px 24px rgba(0,0,0,0.06)",
          }}>
            <MindmapSVG data={result.mindmap} />
          </div>

          <VocabularyCard vocab={result.vocabulary} />
          <VisualJourneyCard journey={result.visualJourney} />

          <style>{`
            @keyframes fadeUp {
              from { opacity: 0; transform: translateY(12px); }
              to { opacity: 1; transform: none; }
            }
          `}</style>
        </div>
      )}
    </div>
  );
}
