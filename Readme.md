# 🎬 VideoTube AI Studio • Powered by Meta AI

> **Autonomous Multi-Model Video Production Engine & Systems Masterclass Platform**  
> Powered **exclusively** by Meta AI (`https://api.meta.ai/v1`) using Meta's official model suite (`muse-wonder-1.0`, `muse-spark-1.3`, `muse-spark-1.2`, `muse-image-1.0`, and `muse-spark-1.3-contributor`).

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)
[![Node.js Version](https://img.shields.io/badge/Node.js-v18%2B-green.svg)](https://nodejs.org/)
[![Database](https://img.shields.io/badge/Database-MongoDB%20Atlas-emerald.svg)](https://www.mongodb.com/atlas)
[![AI Suite](https://img.shields.io/badge/AI%20Suite-Meta%20AI%20Direct-blue.svg)](https://api.meta.ai/v1)

---

## 🌟 Overview

**VideoTube AI Studio** is an enterprise-grade multimodal platform that turns simple conversational prompts (e.g., *"Make a 2 minute video on Docker Container Architecture"*) into:
1. **A Playable 60fps HD Canvas Video:** Complete with timed sequential scenes, cinematic Ken Burns zoom/pan camera motion, kinetic subtitle typography, dynamic audio waveform visualizer, and voiceover narration.
2. **Instant WebM Video Export:** One-click client-side video recording via `MediaRecorder` API that exports standalone `.webm` video files without requiring server-side `ffmpeg` binaries.
3. **Deep Systems Masterclass Dossier (15,000+ characters):** A 3-tab technical dossier rendered beneath the player featuring kernel mechanics, ASCII diagrams, production code patterns, common pitfalls, and pedagogical viewer FAQs.
4. **Cloud Database Persistence:** One-click saving of generated video packages, metadata, and WebP artwork directly to **MongoDB Atlas**.
5. **Interactive 14-Slide Presentation Deck:** Built-in web slide deck (`/presentation.html`) with fullscreen presentation mode, speaker notes, and downloadable `.pptx` file.

---

## 🤖 The 5 Meta AI Models Deployed

VideoTube does **not** rely on expensive third-party paid subscriptions (OpenAI, Claude, ElevenLabs). It connects natively to Meta's official API (`https://api.meta.ai/v1`) using your Meta developer API key:

| Model ID | Meta AI Specialization | Deliverable in VideoTube |
|---|---|---|
| 🧠 **`muse-wonder-1.0`** | Deep Reasoning & Screenplay Direction | Timed 3–5 act sequential screenplay (Hook, Core Acts, CTA), camera directions, and narration voiceover. |
| 🔬 **`muse-spark-1.3`** | Senior Systems Architecture | 10,000+ character under-the-hood technical masterclass, ASCII diagrams, code blueprints, and gotchas. |
| 💡 **`muse-spark-1.2`** | Pedagogy & Developer Education | 6,000+ character FAQ breakdown, subtle mental models, misconception teardowns, and interactive knowledge checks. |
| 🎨 **`muse-image-1.0`** | Generative Native Diffusion | Native 1024×1024 WebP photorealistic visual frames and YouTube thumbnails saved directly to disk. |
| ⚡ **`muse-spark-1.3-contributor`** | Backend & Database Engineering | High-performance MongoDB aggregation pipelines, compound indexes, and controller architecture. |

---

## 🎈 Instant Streamlit Cloud Deployment

You can deploy and run this application directly on **Streamlit Community Cloud** with zero local setup:

1. Visit [**share.streamlit.io**](https://share.streamlit.io) and log in with your GitHub account (`bkutkars-debug`).
2. Click **Create app** (or **New app**).
3. Select your repository:
   - **Repository:** `bkutkars-debug/docker-ai`
   - **Branch:** `main`
   - **Main file path:** `streamlit_app.py`
   - **App URL (optional):** Pick a custom subdomain (e.g. `docker-meta-ai.streamlit.app`)
4. Click **Advanced settings** -> **Secrets**, and enter your Meta API Key:
   ```toml
   META_API_KEY = "LLM_2508659049627425_SP-O03SsEsHr97OwAejF4x6H5kM"
   ```
5. Click **Deploy!** — Streamlit Cloud will install dependencies from `requirements.txt` and launch your live studio URL in under 2 minutes.

---

## 🚀 Quick Start (Local)

### 1. Clone the Repository
```bash
git clone https://github.com/bkutkars-debug/docker-ai.git
cd docker-ai
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Configure Environment Variables
Copy `.env.sample` to `.env` and insert your credentials:
```bash
cp .env.sample .env
```
Ensure your `.env` contains your Meta developer key:
```env
PORT=8000
MONGODB_URL=mongodb+srv://<username>:<password>@cluster0.mongodb.net/
CORS_ORIGIN=*

ACCESS_TOKEN_SECRET=your_jwt_access_token_secret
ACCESS_TOKEN_EXPIRY=1d
REFRESH_TOKEN_SECRET=your_jwt_refresh_token_secret
REFRESH_TOKEN_EXPIRY=10d 

CLOUDINARY_CLOUD_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_cloudinary_key
CLOUDINARY_API_SECRET=your_cloudinary_secret

# Meta AI API Configuration
META_API_KEY=LLM_YOUR_META_API_KEY
META_API_BASE_URL=https://api.meta.ai/v1
META_DEFAULT_MODEL=muse-spark-1.3
META_REASONING_MODEL=muse-wonder-1.0
```

### 4. Start the Application
```bash
npm start
# or for auto-reload during development:
npm run dev
```

### 5. Access the Studio in Your Browser
- **Studio UI:** [http://localhost:8000](http://localhost:8000)
- **Interactive 14-Page Pitch Deck:** [http://localhost:8000/presentation.html](http://localhost:8000/presentation.html)
- **Download PowerPoint Presentation:** [http://localhost:8000/VideoTube_Meta_AI_14_Slide_Presentation.pptx](http://localhost:8000/VideoTube_Meta_AI_14_Slide_Presentation.pptx)

---

## 🎬 How the Video Production Engine Works

1. **Conversational Prompt:**  
   In the Chat Assistant, type:
   > *"Make a 2 minute video on Docker Container Architecture"*
2. **Permission Guard:**  
   The assistant detects the topic and duration and presents an interactive permission card:
   > **Permission Required to Produce Video**  
   > *Target: "Docker Container Architecture" • Timing: 2 minutes*  
   > *Models to deploy: muse-wonder-1.0 + muse-spark-1.3 + muse-spark-1.2 + muse-image-1.0*  
   > `[Yes, Create Video on My Permission]`
3. **Multi-Model Parallel Swarm:**  
   On confirmation, `Promise.allSettled` dispatches calls across Meta's models concurrently.
4. **Playback & Export:**  
   - 60fps HD Canvas video plays through scenes with Ken Burns camera motion and narration.
   - Click **Export Video (.webm)** to download the video file directly.
   - Click **Save to VideoTube DB** to persist the video to MongoDB Atlas.

---

## 📡 API Endpoints Reference

All AI-specific routes are mounted under `/api/v1/ai`:

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/ai/chat` | Main conversational assistant with video intent detection & permission gates |
| `POST` | `/api/v1/ai/create-video` | Dedicated multi-model video production package generator |
| `POST` | `/api/v1/ai/save-video` | Saves generated video package, metadata & artwork to MongoDB |
| `POST` | `/api/v1/ai/thumbnail-image` | Generates real 1024×1024 WebP thumbnail via `muse-image-1.0` |
| `POST` | `/api/v1/ai/code-architect` | Generates MongoDB pipelines & controllers via `muse-spark-1.3-contributor` |
| `POST` | `/api/v1/ai/script` | Generates full YouTube screenplay via `muse-wonder-1.0` |
| `POST` | `/api/v1/ai/metadata` | Generates high-CTR viral titles & SEO tags via `muse-spark-1.3` |
| `GET` | `/api/v1/ai/models` | Lists live available Meta AI models |
| `POST` | `/api/v1/ai/compare-models` | Runs live benchmark across Meta AI models |

---

## 🏛️ System Architecture

```
[ User Browser / Client ]
      │
      ├──> HTML5 60fps Canvas Video Engine (Ken Burns motion, Audio Equalizer)
      ├──> Web Audio API & SpeechSynthesis Voiceover
      ├──> MediaRecorder Client-Side WebM Exporter
      └──> Single-Page Studio UI (Tailwind CSS, FontAwesome)
            │
            ▼  HTTP / REST
[ Node.js & Express MVC Backend ]
      │
      ├──> Auth Middleware (JWT Token Verification in httpOnly Cookies)
      ├──> AI Controllers & Intent Parsing Service
      └──> Meta AI Orchestration Service Layer (metaAi.service.js)
            │
            ├──> muse-wonder-1.0 (Screenplay & Timing)
            ├──> muse-spark-1.3 (Systems Masterclass)
            ├──> muse-spark-1.2 (Pedagogy & FAQs)
            ├──> muse-image-1.0 (1024x1024 WebP Visual Artwork)
            └──> muse-spark-1.3-contributor (Database Aggregations)
                  │
                  ▼
[ Persistence & Storage ]
      ├──> MongoDB Atlas (Videos, Users, Comments, Likes, Playlists)
      ├──> Cloudinary CDN (Media assets)
      └──> Local Static Cache (/public/thumbnails/*.webp)
```

---

## 📊 Presentation Deck

A 14-slide widescreen presentation deck is included in this repository:
- **Web Presentation:** Open `/presentation.html` in your browser.
- **PowerPoint File:** [`VideoTube_Meta_AI_14_Slide_Presentation.pptx`](./VideoTube_Meta_AI_14_Slide_Presentation.pptx)
- **Deck Generator Script:** [`generate_pitch_deck.py`](./generate_pitch_deck.py) (uses `python-pptx` to rebuild the deck anytime).

---

## 📄 License

This project is licensed under the **MIT License**.
