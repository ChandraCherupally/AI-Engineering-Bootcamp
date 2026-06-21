"""
Deep Agents Conversational Chatbot — Streamlit App
Showcases all features from the 05_deepagentsdemo notebooks:
  1. Planning (write_todos)
  2. File System (ls, read_file, write_file, edit_file)
  3. Subagents (task tool with Tavily web search)
  4. Context Engineering (AGENTS.md + Skills)
  5. Multiple Backends (State / Filesystem / Store)
"""

import os
import uuid
import json
import html as html_lib
from pathlib import Path
from typing import Literal, Optional

import streamlit as st
from dotenv import load_dotenv

# ─── Load env ────────────────────────────────────────────────────────────────
load_dotenv()
for key in ("OPENAI_API_KEY", "GROQ_API_KEY", "GOOGLE_API_KEY", "TAVILY_API_KEY"):
    raw = os.getenv(key) or os.getenv(key.replace("OPENAI_API_KEY", "OPEN_API_KEY"))
    if raw:
        os.environ[key] = raw

# Also set OPEN_API_KEY alias used in notebooks
if os.getenv("OPEN_API_KEY"):
    os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", os.getenv("OPEN_API_KEY", ""))

# ─── Streamlit page config ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Deep Agents Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

  html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
  }

  /* Dark glassmorphism background */
  .stApp {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%);
    min-height: 100vh;
  }

  /* Sidebar styling */
  [data-testid="stSidebar"] {
    background: rgba(22, 27, 34, 0.95) !important;
    border-right: 1px solid rgba(99, 102, 241, 0.2);
  }

  /* Card styling */
  .agent-card {
    background: rgba(30, 37, 49, 0.8);
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
    backdrop-filter: blur(10px);
  }

  /* Chat message styling */
  .msg-user {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.15));
    border: 1px solid rgba(99, 102, 241, 0.4);
    border-radius: 16px 16px 4px 16px;
    padding: 14px 18px;
    margin: 8px 0 8px 40px;
    color: #e2e8f0;
    font-size: 0.95rem;
    line-height: 1.6;
    position: relative;
  }

  .msg-ai {
    background: rgba(30, 37, 49, 0.9);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 16px 16px 16px 4px;
    padding: 14px 18px;
    margin: 8px 40px 8px 0;
    color: #cbd5e1;
    font-size: 0.95rem;
    line-height: 1.7;
  }

  .msg-tool {
    background: rgba(16, 24, 36, 0.8);
    border: 1px solid rgba(34, 197, 94, 0.3);
    border-radius: 10px;
    padding: 10px 14px;
    margin: 4px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #86efac;
  }

  /* Role badge */
  .role-badge {
    display: inline-block;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    padding: 2px 8px;
    border-radius: 20px;
    margin-bottom: 6px;
    text-transform: uppercase;
  }
  .badge-user   { background: rgba(99,102,241,0.3); color: #a5b4fc; }
  .badge-ai     { background: rgba(56,189,248,0.2); color: #7dd3fc; }
  .badge-tool   { background: rgba(34,197,94,0.2);  color: #86efac; }

  /* TODO item styling */
  .todo-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 10px;
    border-radius: 8px;
    margin: 4px 0;
    font-size: 0.88rem;
    background: rgba(22, 27, 34, 0.5);
    border: 1px solid rgba(255,255,255,0.06);
    color: #94a3b8;
  }
  .todo-pending   { border-left: 3px solid #6366f1; }
  .todo-progress  { border-left: 3px solid #f59e0b; color: #fcd34d; background: rgba(245,158,11,0.08); }
  .todo-done      { border-left: 3px solid #22c55e; color: #86efac; background: rgba(34,197,94,0.06); text-decoration: line-through; }

  /* File item */
  .file-item {
    padding: 6px 10px;
    border-radius: 8px;
    margin: 3px 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    color: #94a3b8;
    background: rgba(22,27,34,0.4);
    border: 1px solid rgba(255,255,255,0.05);
    cursor: pointer;
    transition: all 0.2s;
  }
  .file-item:hover { border-color: rgba(99,102,241,0.4); color: #c7d2fe; }

  /* Header gradient */
  .app-header {
    background: linear-gradient(135deg, #6366f1, #8b5cf6, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
  }

  /* Feature badge */
  .feature-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 500;
    margin: 2px;
  }
  .fb-planning  { background: rgba(99,102,241,0.2); color:#a5b4fc; border:1px solid rgba(99,102,241,0.3); }
  .fb-fs        { background: rgba(34,197,94,0.15); color:#86efac; border:1px solid rgba(34,197,94,0.3); }
  .fb-sub       { background: rgba(251,146,60,0.15); color:#fdba74; border:1px solid rgba(251,146,60,0.3); }
  .fb-ctx       { background: rgba(56,189,248,0.15); color:#7dd3fc; border:1px solid rgba(56,189,248,0.3); }
  .fb-backend   { background: rgba(167,139,250,0.15); color:#c4b5fd; border:1px solid rgba(167,139,250,0.3); }

  /* Streamlit override fixes */
  .stButton>button {
    border-radius: 10px;
    font-weight: 500;
    transition: all 0.2s;
  }
  .stTextArea textarea, .stTextInput input {
    background: rgba(22, 27, 34, 0.8) !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
  }
  .stSelectbox > div > div {
    background: rgba(22, 27, 34, 0.8) !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
  }

  /* Scrollable chat area */
  .chat-scroll {
    max-height: calc(100vh - 280px);
    overflow-y: auto;
    padding-right: 6px;
  }

  /* Pulsing dot for thinking */
  @keyframes pulse {
    0%,100%{opacity:1;transform:scale(1);}
    50%{opacity:0.5;transform:scale(0.8);}
  }
  .thinking-dot {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: #6366f1;
    margin: 0 2px;
    animation: pulse 1.2s ease infinite;
  }
  .thinking-dot:nth-child(2){animation-delay:0.2s;}
  .thinking-dot:nth-child(3){animation-delay:0.4s;}

  /* Divider */
  hr { border-color: rgba(99,102,241,0.2) !important; }
</style>
""", unsafe_allow_html=True)


# ─── Import deepagents (with graceful error) ──────────────────────────────────
@st.cache_resource
def _import_deepagents():
    try:
        from deepagents import create_deep_agent
        from deepagents.backends import StateBackend, FilesystemBackend, StoreBackend
        from langgraph.checkpoint.memory import MemorySaver
        from langgraph.store.memory import InMemoryStore
        return create_deep_agent, StateBackend, FilesystemBackend, StoreBackend, MemorySaver, InMemoryStore, None
    except ImportError as e:
        return None, None, None, None, None, None, str(e)


create_deep_agent, StateBackend, FilesystemBackend, StoreBackend, MemorySaver, InMemoryStore, import_error = _import_deepagents()


# ─── Helpers ─────────────────────────────────────────────────────────────────
AGENTS_MD_PATH = Path(__file__).parent / "projects" / "AGENTS.md"
SKILLS_DIR = Path(__file__).parent / "skills"

def load_agents_md() -> str:
    if AGENTS_MD_PATH.exists():
        return AGENTS_MD_PATH.read_text(encoding="utf-8")
    return ""


def load_skill_files(skill_name: str) -> dict:
    """Return a dict of virtual path → content for the chosen skill."""
    skill_dir = SKILLS_DIR / skill_name
    files = {}
    if skill_dir.exists():
        for f in skill_dir.iterdir():
            if f.is_file():
                files[f"/skills/{skill_name}/{f.name}"] = {
                    "content": f.read_text(encoding="utf-8"),
                    "encoding": "utf-8",
                }
    return files


def get_tavily_tool():
    """Return a Tavily internet_search tool, or None if key missing."""
    api_key = os.getenv("TAVILY_API_KEY", "")
    if not api_key:
        return None
    try:
        from tavily import TavilyClient

        client = TavilyClient(api_key=api_key)

        def internet_search(
            query: str,
            max_results: int = 5,
            topic: Literal["general", "news", "finance"] = "general",
            include_raw_content: bool = False,
        ):
            """Run a web search and return results."""
            return client.search(
                query,
                max_results=max_results,
                include_raw_content=include_raw_content,
                topic=topic,
            )

        return internet_search
    except Exception:
        return None


def extract_todos_from_messages(messages) -> list[dict]:
    """Parse write_todos ToolMessages to build a todo list."""
    todos = []
    for msg in messages:
        cls_name = type(msg).__name__
        if cls_name == "AIMessage":
            for tc in getattr(msg, "tool_calls", []):
                if tc.get("name") == "write_todos":
                    args = tc.get("args", {})
                    raw = args.get("todos", [])
                    if isinstance(raw, list):
                        todos = raw  # last write_todos wins
    return todos


def extract_files_from_result(result: dict) -> dict:
    """Get files dict from agent result (StateBackend approach)."""
    return result.get("files", {}) if result else {}


def _extract_text(content) -> str:
    """Safely convert a message content to a plain string.

    Some models (e.g. Claude) return a list of content blocks like
    [{'type': 'text', 'text': '...'}, ...] instead of a plain string.
    We flatten those into a single string.
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                parts.append(block.get("text", str(block)))
            else:
                parts.append(str(block))
        return "\n".join(parts)
    return str(content) if content else ""


def parse_messages_for_display(messages) -> list[dict]:
    """Convert LangGraph messages into displayable dicts."""
    display = []
    for msg in messages:
        cls_name = type(msg).__name__
        if cls_name == "HumanMessage":
            display.append({"role": "user", "content": _extract_text(getattr(msg, "content", ""))})
        elif cls_name == "AIMessage":
            content = _extract_text(getattr(msg, "content", ""))
            tool_calls = getattr(msg, "tool_calls", [])
            if content:
                display.append({"role": "ai", "content": content, "tool_calls": tool_calls})
            elif tool_calls:
                # Tool-only message (agent is calling a tool but not yet speaking)
                display.append({"role": "ai", "content": "", "tool_calls": tool_calls})
        elif cls_name == "ToolMessage":
            name = getattr(msg, "name", "tool")
            content = _extract_text(getattr(msg, "content", ""))
            display.append({"role": "tool", "name": name, "content": content})
    return display


def render_todo_list(todos: list[dict]):
    """Render a styled todo list."""
    if not todos:
        st.markdown("<p style='color:#64748b;font-size:0.85rem;'>No todos yet. Ask the agent to plan something!</p>", unsafe_allow_html=True)
        return
    for item in todos:
        if isinstance(item, dict):
            status = item.get("status", "pending")
            task = item.get("task", str(item))
        else:
            status = "pending"
            task = str(item)

        icon = {"pending": "○", "in_progress": "◐", "completed": "✓"}.get(status, "○")
        css_cls = {"pending": "todo-pending", "in_progress": "todo-progress", "completed": "todo-done"}.get(status, "todo-pending")
        st.markdown(
            f'<div class="todo-item {css_cls}">'
            f'<span style="font-size:1rem">{icon}</span> {task}'
            f'<span style="margin-left:auto;font-size:0.7rem;opacity:0.6">{status}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )


def render_file_browser(files: dict):
    """Render virtual filesystem browser."""
    if not files:
        st.markdown("<p style='color:#64748b;font-size:0.85rem;'>No files yet. Ask the agent to write a file!</p>", unsafe_allow_html=True)
        return
    for path, meta in sorted(files.items()):
        content = meta.get("content", "") if isinstance(meta, dict) else str(meta)
        with st.expander(f"📄 {path}", expanded=False):
            st.code(content, language="text")


def build_agent(model_str: str, backend_choice: str, system_prompt: str,
                subagent_enabled: bool, subagent_model_str: str | None = None):
    """Create (or recreate) the deep agent.

    subagent_model_str:
        None  → subagent inherits the main model (always works)
        str   → explicit model; wrapped in try/except so a bad/unavailable
                model string falls back to inheriting the main model instead
                of crashing the whole agent.
    """
    if create_deep_agent is None:
        return None

    tavily_tool = get_tavily_tool()
    custom_tools = [tavily_tool] if tavily_tool else []

    subagents = []
    if subagent_enabled and tavily_tool:
        research_subagent = {
            "name": "research-agent",
            "description": "Used to research in-depth questions using web search",
            "system_prompt": (
                "You are a great researcher. Search the web thoroughly and "
                "provide detailed, well-cited answers."
            ),
            "tools": [tavily_tool],
        }
        # Only add 'model' key when an explicit model was chosen.
        # Omitting it makes the subagent inherit the main agent's model,
        # which is always a safe fallback.
        if subagent_model_str:
            research_subagent["model"] = subagent_model_str
        subagents.append(research_subagent)

    try:
        checkpointer = MemorySaver()

        if backend_choice == "StateBackend (In-Memory)":
            backend = StateBackend()
        elif backend_choice == "FilesystemBackend (Local Disk)":
            root = Path(__file__).parent
            backend = FilesystemBackend(root_dir=str(root), virtual_mode=True)
        else:  # StoreBackend
            store = InMemoryStore()
            st.session_state["langgraph_store"] = store
            backend = StoreBackend(namespace=lambda rt: ("demo-user",))

        kwargs = dict(
            model=model_str,
            tools=custom_tools,
            system_prompt=system_prompt,
            subagents=subagents,
            backend=backend,
            checkpointer=checkpointer,
        )
        if backend_choice == "StoreBackend (Cross-Thread)":
            kwargs["store"] = st.session_state.get("langgraph_store")

        return create_deep_agent(**kwargs)
    except Exception as e:
        st.error(f"Failed to create agent: {e}")
        return None


# ─── Session state init ───────────────────────────────────────────────────────
def init_session():
    defaults = {
        "messages": [],            # raw LangGraph message objects
        "display_msgs": [],        # parsed for UI rendering
        "thread_id": str(uuid.uuid4()),
        "agent": None,
        "agent_config": {},        # last-used config to detect changes
        "todos": [],
        "files": {},
        "thinking": False,
        "last_result": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_session()


# ─── SIDEBAR ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Agent Configuration")
    st.markdown("---")

    # Model selection
    st.markdown("**🧠 Model**")
    model_choice = st.selectbox(
        "Model",
        [
            "google_genai:gemini-2.5-flash-lite",
            "groq:qwen/qwen3-32b",
            "groq:llama-3.1-8b-instant",
        ],
        label_visibility="collapsed",
        key="model_choice",
    )

    # Backend selection
    st.markdown("**🗄️ Storage Backend**")
    backend_choice = st.selectbox(
        "Backend",
        [
            "StateBackend (In-Memory)",
            "FilesystemBackend (Local Disk)",
            "StoreBackend (Cross-Thread)",
        ],
        label_visibility="collapsed",
        key="backend_choice",
    )

    # Backend info
    backend_info = {
        "StateBackend (In-Memory)": "📦 Files live in LangGraph state. Ephemeral — lost when conversation ends.",
        "FilesystemBackend (Local Disk)": "💾 Files written to actual disk. Persistent across restarts.",
        "StoreBackend (Cross-Thread)": "🔄 Files shared across threads using InMemoryStore. Cross-conversation.",
    }
    st.info(backend_info.get(backend_choice, ""))

    st.markdown("---")

    # Subagent toggle + model selector
    st.markdown("**🤖 Subagents**")
    subagent_enabled = st.toggle(
        "Enable Research Subagent",
        value=True,
        help="Enables a specialized research subagent that uses Tavily web search",
        key="subagent_enabled",
    )
    if subagent_enabled:
        subagent_model = st.selectbox(
            "Subagent model",
            [
                "Same as main model (safe default)",
                "groq:qwen/qwen3-32b",
                "groq:llama-3.1-8b-instant",
                "google_genai:gemini-2.5-flash-lite",
            ],
            index=0,
            key="subagent_model",
            help="Model the research subagent uses. 'Same as main model' is always safe — it inherits whatever the main agent uses.",
        )
        # Resolve to None (inherit) or an explicit model string
        _resolved = None if subagent_model.startswith("Same") else subagent_model
        _label = subagent_model if not subagent_model.startswith("Same") else model_choice
        st.markdown(
            f'<span class="feature-badge fb-sub">🔍 research-agent · {_label} + Tavily</span>',
            unsafe_allow_html=True,
        )
        if _resolved and "groq" in _resolved:
            st.caption("⚠️ Groq models require a valid GROQ\_API\_KEY. If the call fails the main model is used as fallback.")
    else:
        subagent_model = "Same as main model (safe default)"

    st.markdown("---")

    # Skills loader
    st.markdown("**📚 Skills (Context Engineering)**")
    available_skills = [d.name for d in SKILLS_DIR.iterdir() if d.is_dir()] if SKILLS_DIR.exists() else []
    selected_skills = st.multiselect(
        "Load skills into agent context:",
        available_skills,
        default=[],
        key="selected_skills",
        help="Skills are loaded as files into the agent's virtual filesystem",
    )

    # AGENTS.md toggle
    load_agents_md_ctx = st.toggle(
        "Load AGENTS.md context",
        value=True,
        key="load_agents_md",
        help="Pre-loads the project AGENTS.md as context engineering for the agent",
    )

    st.markdown("---")

    # System prompt
    st.markdown("**📝 System Prompt**")
    default_prompt = "You are a powerful deep agent. Plan tasks before executing, use files to store intermediate work, and delegate research to subagents when needed."
    system_prompt = st.text_area(
        "System prompt",
        value=default_prompt,
        height=120,
        label_visibility="collapsed",
        key="system_prompt",
    )

    st.markdown("---")

    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 Apply Config", use_container_width=True, type="primary"):
            st.session_state["agent"] = None  # force rebuild
            st.session_state["messages"] = []
            st.session_state["display_msgs"] = []
            st.session_state["todos"] = []
            st.session_state["files"] = {}
            st.session_state["thread_id"] = str(uuid.uuid4())
            st.rerun()
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state["messages"] = []
            st.session_state["display_msgs"] = []
            st.session_state["todos"] = []
            st.session_state["files"] = {}
            st.session_state["thread_id"] = str(uuid.uuid4())
            st.rerun()

    st.markdown("---")

    # Virtual Filesystem Browser
    st.markdown("### 📁 Virtual Filesystem")
    render_file_browser(st.session_state.get("files", {}))


# ─── MAIN AREA ────────────────────────────────────────────────────────────────
# Header
st.markdown(
    '<h1 class="app-header">🤖 Deep Agents Chat</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    """
    <p style="color:#64748b;margin:-8px 0 12px 0;font-size:0.9rem">
      Conversational chatbot powered by the <strong style="color:#a5b4fc">deepagents</strong> library —
      featuring planning, virtual filesystem, subagents & context engineering.
    </p>
    """,
    unsafe_allow_html=True,
)

# Feature badges
st.markdown(
    """
    <div>
      <span class="feature-badge fb-planning">📋 Planning (write_todos)</span>
      <span class="feature-badge fb-fs">📂 Virtual Filesystem</span>
      <span class="feature-badge fb-sub">🤖 Subagents</span>
      <span class="feature-badge fb-ctx">📄 Context Engineering</span>
      <span class="feature-badge fb-backend">🗄️ Multiple Backends</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown("---")

# ── Two-column layout: chat + activity panel ─────────────────────────────────
chat_col, panel_col = st.columns([3, 1])

with panel_col:
    st.markdown("### 📋 Agent Todos")
    render_todo_list(st.session_state.get("todos", []))

    st.markdown("---")
    st.markdown("### 🔧 Agent Info")
    cfg = {
        "Model": model_choice,
        "Backend": backend_choice.split(" ")[0],
        "Thread": st.session_state["thread_id"][:8] + "...",
        "Subagents": "✅ On" if subagent_enabled else "❌ Off",
        "AGENTS.md": "✅ Loaded" if load_agents_md_ctx else "❌ Off",
        "Skills": ", ".join(selected_skills) if selected_skills else "None",
    }
    for k, v in cfg.items():
        st.markdown(
            f'<div style="display:flex;justify-content:space-between;'
            f'padding:4px 0;font-size:0.82rem;color:#94a3b8;border-bottom:1px solid rgba(255,255,255,0.04)">'
            f'<span style="color:#64748b">{k}</span><span style="color:#c7d2fe">{v}</span></div>',
            unsafe_allow_html=True,
        )

    if import_error:
        st.error(f"⚠️ deepagents import failed:\n{import_error}")


with chat_col:
    # Display existing messages
    for dmsg in st.session_state.get("display_msgs", []):
        role = dmsg.get("role")
        content = dmsg.get("content", "")
        tool_calls = dmsg.get("tool_calls", [])

        if role == "user":
            # HTML-escape user text so special chars don't break the markup
            safe_user = html_lib.escape(content).replace("\n", "<br>")
            st.markdown(
                f'<div class="msg-user">'
                f'<div class="role-badge badge-user">You</div><br>'
                f'{safe_user}'
                f'</div>',
                unsafe_allow_html=True,
            )
        elif role == "ai":
            tc_html = ""
            for tc in tool_calls:
                tc_name = tc.get("name", "tool")
                args_safe = html_lib.escape(json.dumps(tc.get("args", {}), indent=2))
                tc_html += (
                    f'<div class="msg-tool">🔧 <b>{tc_name}</b><br>'
                    f'<pre style="margin:4px 0;white-space:pre-wrap;font-size:0.75rem">{args_safe}</pre></div>'
                )

            if content or tc_html:
                # HTML-escape AI text; convert newlines → <br> for readability
                safe_ai = html_lib.escape(content).replace("\n", "<br>") if content else ""
                st.markdown(
                    f'<div class="msg-ai">'
                    f'<div class="role-badge badge-ai">Agent</div><br>'
                    f'{safe_ai}'
                    f'{tc_html}'
                    f'</div>',
                    unsafe_allow_html=True,
                )
        elif role == "tool":
            name = dmsg.get("name", "tool")
            # Show a reasonable preview; full content in the code block
            preview = content[:800] + ("\n…[truncated]" if len(content) > 800 else "")
            lang = "json" if (content.lstrip().startswith("{") or content.lstrip().startswith("[")) else "text"
            with st.expander(f"🔧 Tool result: `{name}`", expanded=True):
                st.code(preview, language=lang)

    # Thinking indicator
    if st.session_state.get("thinking", False):
        st.markdown(
            '<div class="msg-ai" style="padding:10px 18px">'
            '<div class="role-badge badge-ai">Agent</div><br>'
            '<span class="thinking-dot"></span>'
            '<span class="thinking-dot"></span>'
            '<span class="thinking-dot"></span>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ── Input area ────────────────────────────────────────────────────────────
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_area(
            "Message",
            placeholder="Ask the agent anything… e.g. 'Plan how to build a REST API', 'Search for recent news about AI', 'Write a Python script for binary search'",
            height=100,
            label_visibility="collapsed",
            key="user_input",
        )
        submit_btn = st.form_submit_button("Send ➤", use_container_width=True, type="primary")

    # Quick prompts
    st.markdown("**Quick prompts:**")
    qcols = st.columns(3)
    quick_prompts = [
        ("📋 Plan a task", "Plan how you would research and write a comprehensive report on quantum computing. Create a todo list."),
        ("📂 Write a file", "Create a file at /notes/research.md with a summary of what deep agents are."),
        ("🔍 Web search", "Search the web for the latest news about LangChain and summarize the top 3 results."),
        ("🤖 Use subagent", "Delegate to the research subagent: find me 3 recent papers on AI agents and summarize them."),
        ("💡 Show filesystem", "List all files in the virtual filesystem and tell me what you see."),
        ("🐍 Code task", "Write a Python function that implements a binary search algorithm with type hints and docstrings."),
    ]
    for i, (label, prompt) in enumerate(quick_prompts):
        if qcols[i % 3].button(label, key=f"qp_{i}", use_container_width=True):
            st.session_state["_quick_prompt"] = prompt
            st.rerun()


# ─── Process message send ─────────────────────────────────────────────────────
def send_message(user_text: str):
    """Queue a message for processing — build agent if needed, then trigger do_invoke."""
    if not user_text.strip():
        return

    # ── Build agent if needed (synchronously before showing thinking) ──
    _raw_subagent_model = st.session_state.get("subagent_model", "Same as main model (safe default)")
    _subagent_model_str = None if _raw_subagent_model.startswith("Same") else _raw_subagent_model

    current_config = {
        "model": model_choice,
        "backend": backend_choice,
        "system_prompt": system_prompt,
        "subagent": subagent_enabled,
        "subagent_model": _subagent_model_str,
    }
    if st.session_state.get("agent") is None or st.session_state.get("agent_config") != current_config:
        st.session_state["agent"] = build_agent(
            model_choice, backend_choice, system_prompt, subagent_enabled,
            subagent_model_str=_subagent_model_str,
        )
        st.session_state["agent_config"] = current_config

    if st.session_state.get("agent") is None:
        st.error("Agent could not be created. Check API keys and configuration.")
        return

    # ── Store pending user text and trigger thinking state ──
    st.session_state["_pending_user_text"] = user_text
    st.session_state["display_msgs"].append({"role": "user", "content": user_text})
    st.session_state["thinking"] = True
    st.rerun()


def do_invoke():
    """Actually run the agent invocation (called when thinking=True)."""
    agent = st.session_state.get("agent")
    if agent is None:
        st.session_state["thinking"] = False
        return

    user_text = st.session_state.pop("_pending_user_text", None)
    if not user_text:
        st.session_state["thinking"] = False
        return

    thread_config = {"configurable": {"thread_id": st.session_state["thread_id"]}}

    # Build files state (context engineering)
    files_state = {}
    if st.session_state.get("load_agents_md", True):
        md_content = load_agents_md()
        if md_content:
            files_state["/projects/AGENTS.md"] = {"content": md_content, "encoding": "utf-8"}
    for skill in st.session_state.get("selected_skills", []):
        files_state.update(load_skill_files(skill))
    # Merge existing virtual files (for StateBackend continuity across turns)
    files_state.update(st.session_state.get("files", {}))

    # Build previous LangGraph messages + new human message
    prev_lc_msgs = st.session_state.get("messages") or []
    invoke_input = {
        "messages": prev_lc_msgs + [{"role": "user", "content": user_text}],
    }
    if files_state:
        invoke_input["files"] = files_state

    try:
        result = agent.invoke(invoke_input, config=thread_config)
        st.session_state["last_result"] = result

        # Update raw LangGraph messages
        all_msgs = result.get("messages", [])
        st.session_state["messages"] = all_msgs

        # Update virtual files (StateBackend returns them in result)
        updated_files = result.get("files", {})
        if updated_files:
            st.session_state["files"] = updated_files

        # Parse for UI display
        display = parse_messages_for_display(all_msgs)
        st.session_state["display_msgs"] = display

        # Extract todos from planning tool calls
        todos = extract_todos_from_messages(all_msgs)
        if todos:
            st.session_state["todos"] = todos

    except Exception as e:
        st.session_state["display_msgs"].append({
            "role": "ai",
            "content": f"⚠️ **Error:** {e}\n\nPlease check your API keys and configuration.",
            "tool_calls": [],
        })
    finally:
        st.session_state["thinking"] = False


# ─── Handle submit / quick prompt ─────────────────────────────────────────────
_quick = st.session_state.pop("_quick_prompt", None)

if st.session_state.get("thinking"):
    do_invoke()
    st.rerun()

if submit_btn and user_input and user_input.strip():
    send_message(user_input)

elif _quick:
    send_message(_quick)


# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    """
    <div style="text-align:center;color:#334155;font-size:0.75rem;padding:8px 0">
      Built with <strong style="color:#6366f1">deepagents</strong> · LangGraph · Streamlit &nbsp;|&nbsp;
      Features: Planning · Filesystem · Subagents · Context Engineering · Backends
    </div>
    """,
    unsafe_allow_html=True,
)
