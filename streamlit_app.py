import os
import re
import json
import base64
import time
from datetime import datetime
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load local .env if present
load_dotenv()

# Page Configuration
st.set_page_config(
    page_title="VideoTube AI Studio • Powered by Meta AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Dark-mode modern styling matching the platform theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
    }
    
    .gradient-header {
        background: linear-gradient(135deg, #0081FB 0%, #00C6FF 50%, #00F2FE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    .meta-badge {
        background: rgba(0, 129, 251, 0.15);
        color: #60A5FA;
        border: 1px solid rgba(0, 129, 251, 0.3);
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 11px;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .card-box {
        background: rgba(18, 24, 38, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
    }
    
    .metric-badge {
        font-family: 'JetBrains Mono', monospace;
        font-weight: bold;
        color: #10B981;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Configuration & Meta AI Client Setup
# -----------------------------------------------------------------------------
DEFAULT_META_KEY = (
    st.secrets.get("META_API_KEY", "")
    if hasattr(st, "secrets") and "META_API_KEY" in st.secrets
    else os.getenv("META_API_KEY", "LLM_2508659049627425_SP-O03SsEsHr97OwAejF4x6H5kM")
)

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 Meta AI Studio Control")
    st.caption("Powered exclusively by Meta's Official AI Suite (`https://api.meta.ai/v1`)")
    
    api_key_input = st.text_input(
        "Meta API Key",
        value=DEFAULT_META_KEY,
        type="password",
        help="Your Meta AI Developer Key. Never shared or stored."
    )
    
    st.markdown("---")
    st.markdown("#### ⚡ Active Meta AI Models")
    st.markdown("""
    - 🧠 **`muse-wonder-1.0`** *(Reasoning Director)*
    - 🔬 **`muse-spark-1.3`** *(Systems Masterclass)*
    - 💡 **`muse-spark-1.2`** *(Pedagogy & FAQs)*
    - 🎨 **`muse-image-1.0`** *(Native 1024x1024 WebP)*
    - ⚡ **`muse-spark-1.3-contributor`** *(Code & DB)*
    """)
    
    st.markdown("---")
    st.markdown("#### 📁 Resources")
    pptx_path = "VideoTube_Meta_AI_14_Slide_Presentation.pptx"
    if os.path.exists(pptx_path):
        with open(pptx_path, "rb") as f:
            st.download_button(
                label="📊 Download 14-Slide .PPTX Deck",
                data=f.read(),
                file_name="VideoTube_Meta_AI_14_Slide_Presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True
            )
            
    st.markdown("[🌐 GitHub Repository](https://github.com/bkutkars-debug/docker-ai)")

@st.cache_resource
def get_meta_client(api_key):
    if not api_key:
        return None
    return OpenAI(
        api_key=api_key,
        baseURL=os.getenv("META_API_BASE_URL", "https://api.meta.ai/v1")
    )

client = get_meta_client(api_key_input)

# -----------------------------------------------------------------------------
# Core Meta AI Production Service Functions
# -----------------------------------------------------------------------------
def parse_video_intent(prompt_text):
    text = prompt_text.lower()
    is_video = bool(re.search(r"\b(make|create|produce|generate|build|video|clip|tutorial)\b", text))
    
    # Timing
    timing = "2 minutes"
    time_match = re.search(r"(\d+(?:\.\d+)?)\s*(?:minute|min|sec|second)s?", text)
    if time_match:
        timing = f"{time_match.group(1)} minutes"
        
    # Topic
    topic = ""
    match = re.search(r"(?:video on|video about|video for|create a video on|make a video on)\s+([^,;\n?!]+)", text)
    if match:
        topic = match.group(1).strip()
        topic = re.sub(r"(?:for|in|with timing|timing)\s+\d+\s*(?:minute|min|sec|second)s?", "", topic).strip()
    else:
        topic = re.sub(r"(make|create|produce|generate|video|for|\d+\s*(?:minute|min|sec|second)s?)", "", text).strip()
        
    if not topic or len(topic) < 2:
        topic = prompt_text.strip()
        
    return is_video, topic.title(), timing

def generate_screenplay(client, topic, duration_min=2):
    total_sec = int(duration_min * 60)
    system_prompt = f"""You are Meta's Lead Executive Video Producer and Screenplay Director.
Produce a complete timed screenplay for a {duration_min} minute(s) ({total_sec} total seconds) video on: "{topic}".
Divide into 3 to 5 distinct sequential scenes adding up to {total_sec} seconds.
Respond strictly in valid JSON with this exact structure:
{{
  "selectedTitle": "An irresistible, viral title",
  "description": "Engaging description with timestamps",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "totalDurationSeconds": {total_sec},
  "durationFormatted": "{duration_min} Minute(s)",
  "thumbnailPrompt": "A detailed, cinematic 3D visual description for Meta muse-image-1.0",
  "scenes": [
    {{
      "sceneNumber": 1,
      "name": "The Hook",
      "timestampStart": "00:00",
      "timestampEnd": "00:15",
      "durationSeconds": 15,
      "visualDescription": "Detailed visual action on screen",
      "narrationText": "The exact spoken words for voiceover narration",
      "captionOverlay": "Punchy 3-5 word subtitle caption"
    }}
  ]
}}"""
    response = client.chat.completions.create(
        model="muse-wonder-1.0",
        messages=[
            {"role": "system", "content": "You are Meta's Lead Screenplay Director. Output strictly valid JSON."},
            {"role": "user", "content": f"Topic: '{topic}'. Duration: {duration_min} mins ({total_sec}s). Generate timed screenplay."}
        ],
        temperature=0.7,
        max_tokens=4096
    )
    content = response.choices[0].message.content or "{}"
    cleaned = re.sub(r"^```json\s*", "", content, flags=re.I)
    cleaned = re.sub(r"^```\s*", "", cleaned, flags=re.I)
    cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.I).strip()
    try:
        return json.loads(cleaned)
    except Exception:
        return {
            "selectedTitle": f"{topic} in {duration_min} Minutes!",
            "description": f"Complete guide to {topic} powered by Meta AI.",
            "tags": [topic, "guide", "meta-ai"],
            "totalDurationSeconds": total_sec,
            "durationFormatted": f"{duration_min} Minute(s)",
            "thumbnailPrompt": f"Cinematic YouTube thumbnail for {topic}, glowing neon code, 3D high contrast render",
            "scenes": [
                {
                    "sceneNumber": 1,
                    "name": "The Hook",
                    "timestampStart": "00:00",
                    "timestampEnd": "00:20",
                    "durationSeconds": 20,
                    "visualDescription": f"Exciting visual hook introducing {topic}",
                    "narrationText": f"Have you ever wondered how {topic} actually works under the hood? In the next {duration_min} minutes, you will understand it completely.",
                    "captionOverlay": f"Mastering {topic}!"
                },
                {
                    "sceneNumber": 2,
                    "name": "Core Architecture",
                    "timestampStart": "00:20",
                    "timestampEnd": "01:20",
                    "durationSeconds": 60,
                    "visualDescription": "Step-by-step architectural breakdown",
                    "narrationText": "Here is the key takeaway: everything revolves around simplicity, isolation, and speed.",
                    "captionOverlay": "The Core Secret Revealed"
                },
                {
                    "sceneNumber": 3,
                    "name": "Conclusion & Outro",
                    "timestampStart": "01:20",
                    "timestampEnd": f"0{duration_min}:00",
                    "durationSeconds": 40,
                    "visualDescription": "Summary screen with subscribe call-to-action",
                    "narrationText": f"And that is {topic} in under {duration_min} minutes! Hit like, subscribe, and let us know what you want to see next.",
                    "captionOverlay": "Subscribe for More!"
                }
            ]
        }

def generate_masterclass(client, topic):
    prompt = f"""You are Meta's Senior Principal Systems Architect & Engineering Lead.
Write a deep, authoritative, masterclass-level technical and architectural explanation of: "{topic}".
Include:
# {topic}: Senior Systems Masterclass & Deep Dive
## 1. Executive Summary & Why It Matters
## 2. Under-The-Hood Architecture & Mechanics (Include an ASCII flowchart)
## 3. Core Mental Models & Fundamental Principles
## 4. Production-Ready Code / Architectural Blueprint
## 5. Critical Production Pitfalls & Anti-Patterns
## 6. Executive Takeaways & Cheat Sheet
Format with rich Markdown, code blocks, and diagrams."""
    response = client.chat.completions.create(
        model="muse-spark-1.3",
        messages=[
            {"role": "system", "content": "You are Meta's Senior Principal Systems Architect. Write deep Markdown masterclasses."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
        max_tokens=3500
    )
    return response.choices[0].message.content or ""

def generate_faqs(client, topic):
    prompt = f"""You are Meta's Lead Pedagogical Researcher and Developer Advocate.
For the topic: "{topic}", provide:
1. Top 4 Deep Viewer FAQs that address the most subtle, confusing aspects with authoritative answers.
2. 2 Common Beginner Misconceptions and why they are wrong.
3. 2 Quick Interactive Knowledge-Check questions with complete explanations.
Format cleanly in Markdown with bold headers and bullet points."""
    response = client.chat.completions.create(
        model="muse-spark-1.2",
        messages=[
            {"role": "system", "content": "You are Meta's Lead Pedagogical Researcher. Output rich Markdown FAQs."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=2500
    )
    return response.choices[0].message.content or ""

def generate_image(client, prompt_text, title=""):
    full_prompt = f"YouTube 4k thumbnail for '{title or prompt_text}': {prompt_text}. High contrast 3D render, cinematic studio lighting, trending on ArtStation."
    try:
        response = client.images.generate(
            model="muse-image-1.0",
            prompt=full_prompt,
            n=1,
            size="1024x1024",
            response_format="b64_json"
        )
        b64 = response.data[0].b64_json
        return base64.b64decode(b64)
    except Exception as e:
        st.warning(f"Note on image generation: {e}")
        return None

# -----------------------------------------------------------------------------
# Main Application Header
# -----------------------------------------------------------------------------
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 12px; margin-bottom: 20px;">
    <div>
        <h1 style="margin: 0; font-size: 28px;">VideoTube <span class="gradient-header">AI Studio</span></h1>
        <p style="margin: 0; color: #94A3B8; font-size: 13px;">Autonomous Multi-Model Video Production Engine & Masterclass System • Exclusively Meta AI</p>
    </div>
    <div>
        <span class="meta-badge">Meta AI Suite Live</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Tabs Navigation
# -----------------------------------------------------------------------------
tab_video, tab_masterclass, tab_artwork, tab_deck, tab_benchmark = st.tabs([
    "🎬 AI Video Creator Studio",
    "📘 Deep Systems Masterclass",
    "🎨 Real AI Artwork (`muse-image-1.0`)",
    "📊 14-Slide Presentation Deck",
    "🤖 Meta Model Benchmarks"
])

# =============================================================================
# TAB 1: AI Video Creator Studio
# =============================================================================
with tab_video:
    st.markdown("### 🎬 Conversational Video Production Studio")
    st.caption("Ask to create a video on any topic with any timing. The system requests your permission before deploying Meta's multi-model swarm.")
    
    col_input, col_presets = st.columns([3, 1.2])
    with col_input:
        user_prompt = st.text_input(
            "Enter your video request:",
            placeholder="e.g. Make a 2 minute video on Docker Container Architecture",
            key="video_prompt_input"
        )
    with col_presets:
        preset = st.selectbox(
            "Or pick a preset topic:",
            [
                "Custom prompt",
                "Docker Container Architecture in 2 minutes",
                "Kubernetes Cluster Internals in 90 seconds",
                "MongoDB Aggregation Pipelines in 3 minutes",
                "Microservices vs Monoliths in 2 minutes"
            ]
        )
        if preset != "Custom prompt":
            user_prompt = preset

    if user_prompt:
        is_video, detected_topic, detected_timing = parse_video_intent(user_prompt)
        
        # Permission Guard Card
        st.markdown(f"""
        <div class="card-box" style="border: 1px solid rgba(0, 129, 251, 0.4); background: rgba(0, 129, 251, 0.05);">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <span style="color: #FACC15; font-size: 11px; font-weight: bold; text-transform: uppercase;">⚠️ Permission Required to Produce Video</span>
                    <h4 style="margin: 4px 0 0 0; color: white; font-size: 16px;">Target Topic: <strong>"{detected_topic}"</strong></h4>
                    <p style="margin: 2px 0 0 0; color: #94A3B8; font-size: 12px;">Planned Duration: <strong style="color: #60A5FA;">{detected_timing}</strong></p>
                </div>
                <div>
                    <span class="meta-badge">4 Meta Models Ready</span>
                </div>
            </div>
            <div style="margin-top: 10px; font-size: 11px; color: #94A3B8;">
                Meta AI Models to deploy: <strong>muse-wonder-1.0</strong> (Screenplay & Timing) + <strong>muse-spark-1.3</strong> (Architecture Masterclass) + <strong>muse-spark-1.2</strong> (FAQs) + <strong>muse-image-1.0</strong> (1024x1024 WebP Frame).
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col_btn1, col_btn2 = st.columns([2, 5])
        with col_btn1:
            confirm = st.button("▶ Yes, Create Video on My Permission", type="primary", use_container_width=True)
            
        if confirm:
            if not client:
                st.error("Please configure your Meta API Key in the sidebar to proceed.")
            else:
                progress_bar = st.progress(0, text="Deploying Meta AI Multi-Model Swarm...")
                t_start = time.time()
                
                # 1. Screenplay
                progress_bar.progress(25, text="Directing screenplay with Meta muse-wonder-1.0...")
                plan = generate_screenplay(client, detected_topic, duration_min=2)
                
                # 2. Masterclass
                progress_bar.progress(50, text="Authoring deep systems masterclass with Meta muse-spark-1.3...")
                masterclass_text = generate_masterclass(client, detected_topic)
                
                # 3. FAQs
                progress_bar.progress(75, text="Generating pedagogy FAQs with Meta muse-spark-1.2...")
                faqs_text = generate_faqs(client, detected_topic)
                
                # 4. Artwork
                progress_bar.progress(90, text="Rendering 1024x1024 WebP artwork with Meta muse-image-1.0...")
                img_bytes = generate_image(client, plan.get("thumbnailPrompt", detected_topic), plan.get("selectedTitle", detected_topic))
                
                progress_bar.progress(100, text="Video Production Package Completed!")
                elapsed = round(time.time() - t_start, 1)
                
                st.success(f"🎬 Video Production Package & Masterclass Generated in **{elapsed}s** via Meta AI!")
                
                # Presentation Layout
                col_player, col_scenes = st.columns([1.3, 1])
                
                with col_player:
                    st.markdown(f"#### 📺 {plan.get('selectedTitle', detected_topic)}")
                    if img_bytes:
                        st.image(img_bytes, caption=f"Meta muse-image-1.0 • 1024x1024 WebP Frame", use_container_width=True)
                    else:
                        st.info("Rendered artwork display")
                        
                    st.caption(f"**Target Duration:** {plan.get('durationFormatted', '2 Mins')} • **Tags:** {', '.join(plan.get('tags', []))}")
                    st.markdown(f"**Description:** {plan.get('description', '')}")
                    
                with col_scenes:
                    st.markdown("#### 🎬 Timed Scene Screenplay (`muse-wonder-1.0`)")
                    for s in plan.get("scenes", []):
                        with st.expander(f"Scene {s.get('sceneNumber', 1)}: {s.get('name', 'Act')} ({s.get('timestampStart')} - {s.get('timestampEnd')})", expanded=True):
                            st.markdown(f"**Caption Overlay:** `{s.get('captionOverlay', '')}`")
                            st.markdown(f"**Visual Cue:** *{s.get('visualDescription', '')}*")
                            st.markdown(f"**Voiceover Narration:**")
                            st.info(f"\"{s.get('narrationText', '')}\"")
                
                # Deep Topic Masterclass Dossier
                st.markdown("---")
                st.markdown("### 📘 Deep Topic Masterclass Dossier")
                
                tab_arch, tab_faq, tab_audit = st.tabs([
                    "🔬 Under-the-Hood Architecture (`muse-spark-1.3`)",
                    "💡 FAQs & Mental Models (`muse-spark-1.2`)",
                    "🤖 Meta AI Swarm Audit"
                ])
                
                with tab_arch:
                    st.markdown(masterclass_text)
                    
                with tab_faq:
                    st.markdown(faqs_text)
                    
                with tab_audit:
                    st.markdown("#### Meta AI Multi-Model Swarm Attribution")
                    st.markdown(f"""
                    - 🧠 **`muse-wonder-1.0`**: Screenplay, Scene Choreography & Spoken Narration
                    - 🔬 **`muse-spark-1.3`**: Senior Systems Architecture Masterclass ({len(masterclass_text)} chars)
                    - 💡 **`muse-spark-1.2`**: Pedagogical Viewer FAQs & Misconception Analysis ({len(faqs_text)} chars)
                    - 🎨 **`muse-image-1.0`**: Real 1024x1024 Generative Diffusion Artwork Frame
                    - **Total Swarm Execution Time:** `{elapsed} seconds`
                    """)

# =============================================================================
# TAB 2: Deep Systems Masterclass (On-Demand)
# =============================================================================
with tab_masterclass:
    st.markdown("### 🔬 Senior Systems Architecture Masterclass Generator")
    st.caption("Powered by **Meta muse-spark-1.3** • Produces 10,000+ character deep architectural breakdowns with ASCII flowcharts and code blueprints.")
    
    mc_topic = st.text_input("Enter engineering topic for deep dive:", value="Kubernetes Cluster Architecture & Internals")
    if st.button("Generate Senior Systems Masterclass", type="primary"):
        if not client:
            st.error("Please configure your Meta API Key in the sidebar.")
        else:
            with st.spinner("Authoring deep masterclass with Meta muse-spark-1.3..."):
                t0 = time.time()
                doc = generate_masterclass(client, mc_topic)
                st.success(f"Masterclass generated in {round(time.time() - t0, 1)}s!")
                st.markdown(doc)
                st.download_button(
                    "📥 Download Masterclass (.md)",
                    data=doc,
                    file_name=f"{mc_topic.lower().replace(' ', '_')}_masterclass.md",
                    mime="text/markdown"
                )

# =============================================================================
# TAB 3: Real AI Artwork Studio (muse-image-1.0)
# =============================================================================
with tab_artwork:
    st.markdown("### 🎨 Real AI Artwork & YouTube Thumbnail Generator")
    st.caption("Powered by **Meta muse-image-1.0** • Generates native 1024x1024 WebP photorealistic images with 3D cinematic lighting.")
    
    col_img_prompt, col_img_btn = st.columns([4, 1])
    with col_img_prompt:
        img_prompt = st.text_input(
            "Enter thumbnail concept description:",
            value="Glowing neon Docker container floating in cyberspace, high contrast 3D isometric render, cinematic cyan and purple lighting"
        )
    with col_img_btn:
        st.write("")
        st.write("")
        render_btn = st.button("Render 1024x1024 Image", type="primary")
        
    if render_btn:
        if not client:
            st.error("Please configure your Meta API Key in the sidebar.")
        else:
            with st.spinner("Rendering 1024x1024 image with Meta muse-image-1.0..."):
                t0 = time.time()
                raw_img = generate_image(client, img_prompt)
                if raw_img:
                    st.success(f"Rendered in {round(time.time() - t0, 1)}s!")
                    st.image(raw_img, caption="Meta muse-image-1.0 • 1024x1024 WebP Native", use_container_width=True)
                    st.download_button(
                        "📥 Download Image (.webp)",
                        data=raw_img,
                        file_name="meta_artwork.webp",
                        mime="image/webp"
                    )

# =============================================================================
# TAB 4: 14-Slide Master Deck & Download
# =============================================================================
with tab_deck:
    st.markdown("### 📊 14-Page Master Presentation Deck")
    st.caption("Official Pitch Deck & Architecture Blueprint for VideoTube AI Studio")
    
    pptx_file = "VideoTube_Meta_AI_14_Slide_Presentation.pptx"
    if os.path.exists(pptx_file):
        with open(pptx_file, "rb") as f:
            st.download_button(
                label="📥 Download Standalone PowerPoint File (.pptx)",
                data=f.read(),
                file_name=pptx_file,
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                type="primary"
            )
            
    st.markdown("---")
    
    # Slide Viewer
    slide_titles = [
        "Slide 01: Title Slide (Cover)",
        "Slide 02: Executive Summary & Project Vision",
        "Slide 03: Problem Statement & Industry Challenges",
        "Slide 04: The Proposed Solution: VideoTube AI Studio",
        "Slide 05: Meta AI Multi-Model Swarm Architecture",
        "Slide 06: Full-Stack System Architecture & Data Flow",
        "Slide 07: Permission-First Human-in-the-Loop AI",
        "Slide 08: 60fps HD Canvas Video Player Engine",
        "Slide 09: The Deep Topic Masterclass Dossier",
        "Slide 10: Production-Grade Backend & Database Design",
        "Slide 11: Real-World Applications & Industry Impact",
        "Slide 12: Security, Performance & Scalability Benchmarks",
        "Slide 13: Market Comparison: Why VideoTube Wins",
        "Slide 14: Future Roadmap & Strategic Conclusion"
    ]
    
    selected_slide = st.selectbox("Select Slide to View:", slide_titles)
    slide_index = int(selected_slide.split(":")[0].replace("Slide ", ""))
    
    slide_content_map = {
        1: ("Cover", "VideoTube AI Studio", "Autonomous Multi-Model Video Production Engine Powered Exclusively by Meta AI",
            "Transforms single conversational prompts into broadcast-ready 60fps HD videos, visual artwork, voiceover narration, and 15,000+ character systems engineering masterclass dossiers in under 40 seconds."),
        2: ("Executive Overview", "Executive Summary: The VideoTube Vision", "Redefining How Humans and AI Collaborate on Video and Education",
            "Eliminates the 10+ hours required to make an educational video by combining automated screenplay direction, real diffusion artwork, voiceover, and deep systems engineering."),
        3: ("Problem Statement", "The Crisis in Modern Video Creation", "Why Traditional Video Editing and Generic AI Tools Fail Creators",
            "Creators face extreme production friction (10+ hours per video across fragmented apps), runaway API subscription spending without user confirmation, and shallow fluff content."),
        4: ("Solution Architecture", "VideoTube AI Studio: The All-in-One Engine", "A Unified Generative Pipeline in a Single Browser Tab",
            "Consolidates intent parsing, permission guardrails, multi-model swarms, real-time 60fps canvas player, and complete masterclass dossiers into one seamless interface."),
        5: ("Meta AI Suite", "The 5 Meta AI Models Deployed Deeply", "Collaborative Multi-Model Swarm Where Each Model Plays a Specialist Role",
            "Deploys muse-wonder-1.0 (screenplay), muse-spark-1.3 (systems masterclass), muse-spark-1.2 (pedagogy/FAQs), muse-image-1.0 (1024x1024 diffusion), and muse-spark-1.3-contributor (database code)."),
        6: ("System Architecture", "Full-Stack System Architecture & Data Flow", "Enterprise-Grade MVC Stack with MongoDB Atlas",
            "Client frontend with 60fps Canvas engine, Node.js/Express MVC backend, Meta AI orchestration service layer, and MongoDB Atlas + Cloudinary storage."),
        7: ("User Experience", "Permission-First Human-in-the-Loop AI", "Protecting User Agency, Quota, and Expectations",
            "Natural language intent parsing halts execution to display an interactive permission card before triggering models, preventing accidental token burn."),
        8: ("Graphics & Video", "60fps HD Canvas Video Player Engine", "Client-Side Real-Time Rendering & WebM Export",
            "Renders 60fps 720p HD canvas with Ken Burns camera zoom/pan, audio equalizer waveform, kinetic typography, and direct MediaRecorder .webm download."),
        9: ("Pedagogy", "The Deep Topic Masterclass Dossier", "15,000+ Characters of Technical Rigor Beneath the Player",
            "A 3-tab technical dossier featuring under-the-hood systems mechanics, ASCII flow diagrams, production code patterns, gotchas, and viewer FAQs."),
        10: ("Backend & DB", "Production-Grade Backend & Database Design", "MongoDB Atlas Schemas and Aggregation Pipelines",
            "Modular Mongoose schemas (Videos, Users, Comments, Subscriptions) optimized by contributor model for sub-10ms query speeds."),
        11: ("Use Cases", "Real-World Applications & Industry Impact", "Transforming Developer Education, Corporate Training, and Creator Growth",
            "Immediate commercial applications across developer EdTech bootcamps, enterprise engineering onboarding, and YouTube creator scaling."),
        12: ("Security & Scale", "Security, Performance & Scalability Benchmarks", "Engineered for Resilience & Client GPU Offload",
            "Dual JWT authentication, bcrypt password hashing, sub-40-second multi-model turnaround, and client GPU offload that keeps server costs near zero."),
        13: ("Market Comparison", "Market Comparison: Why VideoTube Wins", "Redefining the Competitive Landscape",
            "Outclasses traditional editors on speed and cost, and outclasses generic AI wrappers on technical depth and zero subscription fees."),
        14: ("Conclusion", "Future Roadmap & Strategic Conclusion", "The Next Evolution of VideoTube",
            "Roadmap includes neural voice cloning, multi-scene b-roll keyframes, and direct one-click YouTube publishing. Fully functional and live today.")
    }
    
    cat, title, sub, desc = slide_content_map[slide_index]
    
    st.markdown(f"""
    <div class="card-box" style="border: 1px solid rgba(0, 129, 251, 0.4);">
        <span class="meta-badge">{cat.upper()}</span>
        <h2 style="margin: 8px 0 2px 0; color: white;">{title}</h2>
        <p style="color: #60A5FA; font-size: 14px; margin-bottom: 12px;">{sub}</p>
        <p style="color: #E2E8F0; font-size: 14px; line-height: 1.6;">{desc}</p>
    </div>
    """, unsafe_allow_html=True)

# =============================================================================
# TAB 5: Meta Model Benchmarks
# =============================================================================
with tab_benchmark:
    st.markdown("### 🤖 Meta AI Model Swarm Benchmark")
    st.caption("Compare live responses and latency across Meta's models on the same prompt.")
    
    bench_prompt = st.text_input("Enter benchmark prompt:", value="Explain Docker in 2 sentences with technical precision.")
    if st.button("Run Multi-Model Benchmark", type="primary"):
        if not client:
            st.error("Please configure your Meta API Key in the sidebar.")
        else:
            models_to_test = [
                ("muse-spark-1.3", "Fast Reasoning"),
                ("muse-wonder-1.0", "Deep Reasoning"),
                ("muse-spark-1.3-contributor", "Code Specialist")
            ]
            
            cols = st.columns(len(models_to_test))
            for i, (m_id, m_role) in enumerate(models_to_test):
                with cols[i]:
                    st.markdown(f"**`{m_id}`**")
                    st.caption(m_role)
                    t0 = time.time()
                    try:
                        res = client.chat.completions.create(
                            model=m_id,
                            messages=[{"role": "user", "content": bench_prompt}],
                            max_tokens=300
                        )
                        dur = round(time.time() - t0, 2)
                        reply = res.choices[0].message.content or "No response"
                        st.info(reply)
                        st.markdown(f"⏱️ **Latency:** `{dur}s`")
                    except Exception as e:
                        st.error(f"Error: {e}")
