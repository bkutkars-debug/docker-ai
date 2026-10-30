import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Theme Colors
    BG_COLOR = RGBColor(11, 15, 25)         # #0B0F19
    CARD_BG = RGBColor(20, 28, 45)          # #141C2D
    CARD_BORDER = RGBColor(40, 56, 85)      # #283855
    META_BLUE = RGBColor(0, 129, 251)       # #0081FB
    CYAN = RGBColor(0, 210, 255)            # #00D2FF
    EMERALD = RGBColor(16, 185, 129)        # #10B981
    YELLOW = RGBColor(250, 204, 21)         # #FACC15
    WHITE = RGBColor(255, 255, 255)
    GRAY_LIGHT = RGBColor(226, 232, 240)    # #E2E8F0
    GRAY_MUTED = RGBColor(148, 163, 184)    # #94A3B8

    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_COLOR
        bg.line.fill.background()
        return bg

    def add_header(slide, slide_num, category, title, subtitle=""):
        # Header Container
        header_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(1.1))
        tf = header_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Category & Slide Num
        p0 = tf.paragraphs[0]
        r_num = p0.add_run()
        r_num.text = f"SLIDE {slide_num:02d}  •  "
        r_num.font.name = "Arial"
        r_num.font.size = Pt(11)
        r_num.font.bold = True
        r_num.font.color.rgb = META_BLUE

        r_cat = p0.add_run()
        r_cat.text = category.upper()
        r_cat.font.name = "Arial"
        r_cat.font.size = Pt(11)
        r_cat.font.bold = True
        r_cat.font.color.rgb = CYAN

        # Main Title
        p1 = tf.add_paragraph()
        r_title = p1.add_run()
        r_title.text = title
        r_title.font.name = "Arial"
        r_title.font.size = Pt(24)
        r_title.font.bold = True
        r_title.font.color.rgb = WHITE

        if subtitle:
            r_sub = p1.add_run()
            r_sub.text = f"  |  {subtitle}"
            r_sub.font.name = "Arial"
            r_sub.font.size = Pt(14)
            r_sub.font.color.rgb = GRAY_MUTED

    def add_footer(slide):
        footer_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.733), Inches(0.35))
        tf = footer_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = "VideoTube AI Studio"
        r1.font.bold = True
        r1.font.size = Pt(9)
        r1.font.color.rgb = META_BLUE

        r2 = p.add_run()
        r2.text = "  •  Autonomous Video Production Engine Powered Exclusively by Meta AI  •  Confidential & Proprietary"
        r2.font.size = Pt(9)
        r2.font.color.rgb = GRAY_MUTED

    def add_card(slide, left, top, width, height, title, items, badge="", accent_color=META_BLUE):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = CARD_BORDER
        card.line.width = Pt(1.2)

        tb = slide.shapes.add_textbox(Inches(left + 0.25), Inches(top + 0.2), Inches(width - 0.5), Inches(height - 0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

        # Title
        p_title = tf.paragraphs[0]
        if badge:
            r_badge = p_title.add_run()
            r_badge.text = f"[{badge}] "
            r_badge.font.name = "Arial"
            r_badge.font.size = Pt(11)
            r_badge.font.bold = True
            r_badge.font.color.rgb = accent_color

        r_t = p_title.add_run()
        r_t.text = title
        r_t.font.name = "Arial"
        r_t.font.size = Pt(15)
        r_t.font.bold = True
        r_t.font.color.rgb = WHITE

        # Items
        for item in items:
            p = tf.add_paragraph()
            p.space_before = Pt(6)
            
            if isinstance(item, tuple):
                lead, desc = item
                r_lead = p.add_run()
                r_lead.text = f"• {lead}: "
                r_lead.font.bold = True
                r_lead.font.size = Pt(11)
                r_lead.font.color.rgb = CYAN

                r_desc = p.add_run()
                r_desc.text = desc
                r_desc.font.size = Pt(11)
                r_desc.font.color.rgb = GRAY_LIGHT
            else:
                r_text = p.add_run()
                r_text.text = f"• {item}"
                r_text.font.size = Pt(11)
                r_text.font.color.rgb = GRAY_LIGHT

    # =========================================================================
    # SLIDE 1: Title Slide (Cover)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Decorative Glowing Banner
    banner = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.8), Inches(11.733), Inches(0.08))
    banner.fill.solid()
    banner.fill.fore_color.rgb = META_BLUE
    banner.line.fill.background()

    # Main Title Block
    title_box = s1.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(11.733), Inches(3.2))
    tf1 = title_box.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    r_tag = p0.add_run()
    r_tag.text = "NEXT-GENERATION MULTIMODAL PLATFORM\n"
    r_tag.font.name = "Arial"
    r_tag.font.size = Pt(14)
    r_tag.font.bold = True
    r_tag.font.color.rgb = CYAN

    r_main = p0.add_run()
    r_main.text = "VideoTube AI Studio\n"
    r_main.font.name = "Arial"
    r_main.font.size = Pt(44)
    r_main.font.bold = True
    r_main.font.color.rgb = WHITE

    r_sub = p0.add_run()
    r_sub.text = "Autonomous Multi-Model Video Production Engine & Masterclass System Powered Exclusively by Meta AI"
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(18)
    r_sub.font.color.rgb = GRAY_MUTED

    # Highlights Pills
    pills = [
        ("Zero 3rd-Party APIs", "100% Native Meta AI Suite"),
        ("Permission-Guarded", "Safe Conversational Flow"),
        ("60fps HD Canvas Engine", "Client-Side Video Player & WebM Exporter"),
        ("Deep Masterclass", "15,000+ Char Systems Dossier")
    ]
    pill_w = 2.75
    for i, (head, sub) in enumerate(pills):
        px = 0.8 + i * 2.98
        p_card = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(px), Inches(5.4), Inches(2.8), Inches(1.2))
        p_card.fill.solid()
        p_card.fill.fore_color.rgb = CARD_BG
        p_card.line.color.rgb = CARD_BORDER

        ptb = s1.shapes.add_textbox(Inches(px + 0.15), Inches(5.5), Inches(2.5), Inches(1.0))
        ptf = ptb.text_frame
        ptf.word_wrap = True
        pp0 = ptf.paragraphs[0]
        pr0 = pp0.add_run()
        pr0.text = head + "\n"
        pr0.font.bold = True
        pr0.font.size = Pt(12)
        pr0.font.color.rgb = EMERALD

        pr1 = pp0.add_run()
        pr1.text = sub
        pr1.font.size = Pt(10)
        pr1.font.color.rgb = GRAY_LIGHT

    add_footer(s1)

    # =========================================================================
    # SLIDE 2: Executive Summary & Project Vision
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, 2, "Executive Overview", "Executive Summary: The VideoTube Vision", "Redefining AI Video Creation")
    
    add_card(s2, 0.8, 1.8, 5.7, 4.8, "The Vision & Transformation", [
        ("Core Mission", "Bridge the gap between conversational AI and full-stack video production by eliminating manual scripting, rendering, and asset collation."),
        ("One-Prompt Production", "Users simply ask in natural language (e.g. 'Make a 2-min video on Docker') and receive a complete broadcast-ready production package in 35 seconds."),
        ("Exclusively Meta-Powered", "Direct integration with Meta's official API (https://api.meta.ai/v1) using the user's free Meta developer key—zero OpenAI or paid SaaS dependencies."),
        ("Beyond Video", "Delivers both an interactive 60fps HD video experience AND an in-depth systems architecture masterclass dossier.")
    ], badge="MISSION", accent_color=META_BLUE)

    add_card(s2, 6.8, 1.8, 5.7, 4.8, "Key Platform Metrics & Milestones", [
        ("5 Specialized Models", "Orchestrated in real-time parallel swarms (Wonder, Spark 1.3, Spark 1.2, Image 1.0, Contributor)."),
        ("100% Real Visuals", "Generates native 1024x1024 WebP photorealistic visual frames and thumbnails saved directly to disk."),
        ("Zero Binary Overhead", "Plays and exports 720p HD 60fps WebM videos entirely inside the browser using HTML5 Canvas & Web Audio (no ffmpeg server bottlenecks)."),
        ("Enterprise Architecture", "Complete MVC Node.js/Express backend paired with MongoDB Atlas cloud persistence and JWT token authentication.")
    ], badge="IMPACT", accent_color=EMERALD)
    add_footer(s2)

    # =========================================================================
    # SLIDE 3: Problem Statement & Industry Challenges
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, 3, "Problem Statement", "The Crisis in Modern Video Creation", "Why Traditional Workflows Fail")

    add_card(s3, 0.8, 1.8, 3.7, 4.8, "1. Extreme Production Friction", [
        ("10+ Hours Per Video", "Writing timed scripts, drafting screenplays, sourcing graphics, recording voiceovers, and editing take days."),
        ("High Tool Fragmentation", "Creators juggle ChatGPT for text, Midjourney for images, ElevenLabs for voice, and Premiere for editing."),
        ("High Barrier to Entry", "Novice creators and educators lack professional video editing skills and costly hardware.")
    ], badge="FRICTION", accent_color=RGBColor(244, 63, 94))

    add_card(s3, 4.8, 1.8, 3.7, 4.8, "2. Uncontrolled AI Spending", [
        ("Expensive Paid API Keys", "Most AI video wrappers mandate expensive OpenAI, Claude, or ElevenLabs subscription credits."),
        ("Accidental Token Burn", "Standard chat bots immediately burn high token costs without asking user confirmation or specifying timing."),
        ("Closed Ecosystems", "Creators are locked into proprietary platforms with subscription paywalls.")
    ], badge="COSTS", accent_color=YELLOW)

    add_card(s3, 8.8, 1.8, 3.7, 4.8, "3. Superficial Depth", [
        ("Fluff Content", "Typical AI video tools produce shallow, generic bullet points that lack technical rigor and true depth."),
        ("No Systems Architecture", "Complex engineering concepts (e.g. Docker, K8s, MongoDB) are oversimplified into useless platitudes."),
        ("No Code Blueprints", "Learners leave without runnable code, mental models, or architectural diagrams.")
    ], badge="QUALITY", accent_color=RGBColor(168, 85, 247))
    add_footer(s3)

    # =========================================================================
    # SLIDE 4: The Proposed Solution: VideoTube AI Studio
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, 4, "Solution Architecture", "VideoTube AI Studio: The All-in-One Engine", "Unified Multimodal Platform")

    add_card(s4, 0.8, 1.8, 5.7, 4.8, "Unified Workflow Pipeline", [
        ("1. Conversational Intent", "Chat assistant detects topic, planned timing, and user goals from natural language input."),
        ("2. Permission Safeguard", "System presents an interactive permission modal requiring explicit confirmation before calling AI models."),
        ("3. Swarm Orchestration", "Simultaneously triggers Meta Reasoning, Image Diffusion, Systems Masterclass, and FAQ models in parallel."),
        ("4. Interactive Delivery", "Instantly renders a 60fps HD player, Ken Burns zoom motion, voice narration, audio wave visualizer, and masterclass dossier.")
    ], badge="PIPELINE", accent_color=META_BLUE)

    add_card(s4, 6.8, 1.8, 5.7, 4.8, "Distinctive Platform Capabilities", [
        ("Instant WebM Video Export", "Click 'Export Video (.webm)' to record the canvas and audio directly to a video file on your computer."),
        ("Database One-Click Save", "Directly saves video packages, thumbnails, and metadata to MongoDB Atlas with schema validation."),
        ("Zero Cloud SaaS Fees", "Operates entirely on Meta's official API with the user's free API key."),
        ("Masterclass Learning Hub", "Provides tabbed architectural diagrams, runnable code examples, and pedagogy FAQs alongside the video.")
    ], badge="FEATURES", accent_color=EMERALD)
    add_footer(s4)

    # =========================================================================
    # SLIDE 5: Meta AI Multi-Model Swarm Architecture
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, 5, "Meta AI Suite", "The 5 Meta AI Models Deployed Deeply", "Specialized Model Swarm")

    models_data = [
        ("muse-wonder-1.0", "Meta Reasoning & Screenplay Director", [
            ("Role", "Orchestrates timed 3-5 scene screenplay"),
            ("Output", "Exact duration, hook, body, conclusion, camera direction, voiceover narration script"),
            ("Specialty", "Deep chain-of-thought storytelling & timing alignment")
        ], META_BLUE),
        ("muse-spark-1.3", "Senior Principal Systems Architect", [
            ("Role", "Writes in-depth technical masterclass"),
            ("Output", "10,000+ char deep dive: under-the-hood mechanics, ASCII diagrams, code blueprints, gotchas"),
            ("Specialty", "Authoritative, production-grade technical pedagogy")
        ], CYAN),
        ("muse-spark-1.2", "Lead Pedagogical Researcher", [
            ("Role", "Viewer FAQs & mental models"),
            ("Output", "6,000+ char FAQ breakdown, beginner misconceptions, interactive knowledge checks"),
            ("Specialty", "High-retention educational frameworks")
        ], EMERALD),
        ("muse-image-1.0", "Generative Image Diffusion", [
            ("Role", "Visual artwork & video frames"),
            ("Output", "Real 1024x1024 WebP photorealistic frames & YouTube thumbnails saved to disk"),
            ("Specialty", "High-CTR composition, 3D cinematic lighting")
        ], RGBColor(236, 72, 153))
    ]

    for i, (m_name, m_role, details, color) in enumerate(models_data):
        mx = 0.8 + i * 2.98
        add_card(s5, mx, 1.8, 2.8, 4.8, m_name, details, badge=m_role.split()[0].upper(), accent_color=color)
    add_footer(s5)

    # =========================================================================
    # SLIDE 6: System Architecture & Technical Stack
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, 6, "System Architecture", "Full-Stack System Architecture & Data Flow", "Production-Grade Engineering")

    add_card(s6, 0.8, 1.8, 3.7, 4.8, "Client Layer (Frontend)", [
        ("Single-Page Studio", "Responsive dark-mode UI styled with Tailwind CSS and FontAwesome."),
        ("60fps Canvas Engine", "1280x720 HD rendering viewport with Ken Burns pan/zoom and audio visualizer."),
        ("Web Audio & Speech", "Browser SpeechSynthesis for natural narration synchronized with scene captions."),
        ("MediaRecorder API", "Direct in-browser WebM video recording and export without server encoding.")
    ], badge="FRONTEND", accent_color=CYAN)

    add_card(s6, 4.8, 1.8, 3.7, 4.8, "Server Layer (Backend)", [
        ("Node.js & Express", "Modular REST API architecture adhering to industry MVC standards."),
        ("Orchestration Service", "metaAi.service.js dispatches parallel calls with Promise.allSettled."),
        ("Error Resilient", "Automatic fallback plan generation ensuring 100% uptime even on API timeouts."),
        ("JWT Auth & Cookies", "Secure cookie-based authentication with accessToken and refreshToken.")
    ], badge="BACKEND", accent_color=META_BLUE)

    add_card(s6, 8.8, 1.8, 3.7, 4.8, "Database & Storage Layer", [
        ("MongoDB Atlas", "Mongoose ODM schemas for Users, Videos, Comments, Playlists, and Subscriptions."),
        ("Cloudinary CDN", "Integrated media asset pipeline for avatars, covers, and uploaded video files."),
        ("Local Disk Cache", "Generated WebP artwork stored directly in public/thumbnails/ for instant zero-latency serving."),
        ("Aggregation Pipelines", "High-efficiency MongoDB pipelines with $lookup, $match, and pagination.")
    ], badge="STORAGE", accent_color=EMERALD)
    add_footer(s6)

    # =========================================================================
    # SLIDE 7: Permission-Guarded Human-In-The-Loop Workflow
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, 7, "User Experience", "Permission-First Human-In-The-Loop AI", "Protecting User Agency & Resources")

    add_card(s7, 0.8, 1.8, 5.7, 4.8, "How Intent Detection Works", [
        ("Intent Extraction", "Regex-powered natural language parser identifies video creation verbs ('make', 'create', 'produce') and target topics."),
        ("Duration Parsing", "Extracts custom timing specifications (e.g. '90 seconds', '2 minutes', '5 mins') with sensible defaults."),
        ("Confirmation Gate", "Instead of auto-running costly generation, the assistant pauses and displays an interactive permission card."),
        ("Modal Action", "Presents 'Yes, Create Video on My Permission' alongside model transparency badges.")
    ], badge="DETECTION", accent_color=YELLOW)

    add_card(s7, 6.8, 1.8, 5.7, 4.8, "Why This Architecture Matters", [
        ("Zero Accidental Generations", "Prevents accidental API credit consumption from casual conversational questions."),
        ("Explicit User Control", "Users review topic scope and planned timing before triggering the 4-model swarm."),
        ("Full Transparency", "Displays exactly which Meta models will be invoked and their specific roles."),
        ("Instant Cancellation", "User can cancel with one click or refine prompt parameters before executing.")
    ], badge="SECURITY", accent_color=EMERALD)
    add_footer(s7)

    # =========================================================================
    # SLIDE 8: Real-Time 60fps HD Canvas Video Player Engine
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, 8, "Graphics & Video", "60fps HD Canvas Video Player Engine", "Client-Side Real-Time Rendering")

    add_card(s8, 0.8, 1.8, 3.7, 4.8, "1. Visual Canvas Pipeline", [
        ("1280x720 HD Resolution", "Renders true 16:9 widescreen canvas with double-buffering at 60 frames per second."),
        ("Ken Burns Zoom & Pan", "Dynamic smooth zoom and pan motion applied to Meta-generated artwork."),
        ("Kinetic Typography", "Lower-third scene caption overlays styled with high-contrast text shadows and backdrop blur.")
    ], badge="VISUALS", accent_color=META_BLUE)

    add_card(s8, 4.8, 1.8, 3.7, 4.8, "2. Audio & Narration Sync", [
        ("SpeechSynthesis Voiceover", "Synchronizes browser speech synthesis engine with exact scene script timings."),
        ("Audio Waveform Visualizer", "Dynamic multi-bar audio equalizer pulsing in real-time with narration beats."),
        ("Scene Scrubbing", "Click any scene in the storyboard breakdown to instantly jump playback to that act.")
    ], badge="AUDIO", accent_color=CYAN)

    add_card(s8, 8.8, 1.8, 3.7, 4.8, "3. Zero-Binary WebM Export", [
        ("MediaRecorder API", "Captures canvas video stream and speech audio directly in browser memory."),
        ("One-Click Download", "Exports standalone .webm video file ready to upload to YouTube, LinkedIn, or Twitter."),
        ("No ffmpeg Server Bottleneck", "Zero server CPU load for video rendering; scales seamlessly to millions of users.")
    ], badge="EXPORT", accent_color=EMERALD)
    add_footer(s8)

    # =========================================================================
    # SLIDE 9: Deep Topic Masterclass Dossier System
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, 9, "Pedagogy & Knowledge", "The Deep Topic Masterclass Dossier", "15,000+ Characters of Technical Depth")

    add_card(s9, 0.8, 1.8, 3.7, 4.8, "Tab 1: Systems Architecture", [
        ("Powered by muse-spark-1.3", "Meta's senior principal systems architect model."),
        ("Under-the-Hood Mechanics", "Detailed explanation of kernel operations, memory management, and data flow."),
        ("ASCII Flow Diagrams", "Visual text architecture diagrams illustrating components and pipelines."),
        ("Production Code Blueprint", "Runnable, production-grade Dockerfile, compose, or backend code patterns.")
    ], badge="TAB 1", accent_color=META_BLUE)

    add_card(s9, 4.8, 1.8, 3.7, 4.8, "Tab 2: FAQs & Mental Models", [
        ("Powered by muse-spark-1.2", "Meta's pedagogical developer advocate model."),
        ("Top 4 In-Depth FAQs", "Answers the most confusing and subtle technical questions for engineers."),
        ("2 Core Misconceptions", "Explains why common beginner mental models fail in production."),
        ("Knowledge Checks", "Interactive quiz questions to reinforce key concepts.")
    ], badge="TAB 2", accent_color=CYAN)

    add_card(s9, 8.8, 1.8, 3.7, 4.8, "Tab 3: Meta Models Audit", [
        ("Live Multi-Model Audit", "Real-time verification showing all Meta AI models deployed."),
        ("Role Attribution", "Clearly maps which model generated the screenplay, artwork, masterclass, or FAQs."),
        ("Token & Latency Tracking", "Monitors execution timing and ensures system reliability.")
    ], badge="TAB 3", accent_color=EMERALD)
    add_footer(s9)

    # =========================================================================
    # SLIDE 10: Production-Grade Backend & Database Design
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, 10, "Database & Backend", "Production-Grade Backend & Database Design", "MongoDB Atlas Architecture")

    add_card(s10, 0.8, 1.8, 5.7, 4.8, "MongoDB Mongoose Schema Architecture", [
        ("Video Model", "Stores title, description, duration, views, isPublished, videoFile, and thumbnail URLs."),
        ("User Model", "Stores username, email, fullName, avatar, coverImage, watchHistory, and hashed passwords with bcrypt."),
        ("Engagement Models", "Dedicated schemas for Comments, Likes, Playlists, and channel Subscriptions."),
        ("Indexes & Efficiency", "Compound indexes on userId, createdAt, and text search fields for sub-10ms query execution.")
    ], badge="SCHEMAS", accent_color=META_BLUE)

    add_card(s10, 6.8, 1.8, 5.7, 4.8, "Aggregation & Controller Optimization", [
        ("Contributor Model Tuning", "muse-spark-1.3-contributor writes optimized MongoDB pipelines ($match early, $lookup, $project minimal fields)."),
        ("Asynchronous MVC Design", "Wrapped in asyncHandler utility with standard ApiError and ApiResponse classes."),
        ("Cloudinary Asset Integration", "Automated upload middleware handles thumbnail and media CDN syncing."),
        ("Graceful Degradation", "Server boots even during temporary DB network retries so AI tools remain 100% accessible.")
    ], badge="CONTROLLERS", accent_color=EMERALD)
    add_footer(s10)

    # =========================================================================
    # SLIDE 11: Real-World Demonstration & Use Cases
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, 11, "Use Cases", "Real-World Applications & Industry Impact", "Who Needs VideoTube?")

    add_card(s11, 0.8, 1.8, 3.7, 4.8, "Developer Education & EdTech", [
        ("Micro-Tutorials", "Generate 2-minute architectural breakdowns of Docker, Kubernetes, Kafka, or GraphQL."),
        ("Course Creators", "Produce entire video lecture series with accompanying masterclass notes in hours instead of months."),
        ("Coding Bootcamps", "Deliver automated, interactive video summaries for daily student assignments.")
    ], badge="EDTECH", accent_color=CYAN)

    add_card(s11, 4.8, 1.8, 3.7, 4.8, "Corporate Knowledge & Onboarding", [
        ("Internal Architecture Briefs", "Convert technical PRDs and engineering documentation into engaging video briefings."),
        ("Employee Onboarding", "Rapidly create standardized video training for company tools, security protocols, and APIs."),
        ("Product Demos", "Sales and solutions engineers produce tailored video explainers for prospective clients.")
    ], badge="ENTERPRISE", accent_color=META_BLUE)

    add_card(s11, 8.8, 1.8, 3.7, 4.8, "Content Creators & Marketing", [
        ("YouTube Tech Channels", "Automate scriptwriting, artwork generation, viral titles, and tags in seconds."),
        ("LinkedIn & Social Video", "Export high-engagement short-form video clips directly formatted for social feeds."),
        ("SEO-Driven Content", "Generates high-CTR metadata and descriptions designed to rank at the top of YouTube search.")
    ], badge="CREATORS", accent_color=EMERALD)
    add_footer(s11)

    # =========================================================================
    # SLIDE 12: Security, Performance & Scalability
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, 12, "Security & Scale", "Security, Performance & Scalability Benchmarks", "Engineered for Resilience")

    add_card(s12, 0.8, 1.8, 3.7, 4.8, "Authentication & Data Security", [
        ("JWT Dual-Token Auth", "Short-lived Access Tokens (1d) paired with long-lived Refresh Tokens (10d) stored in httpOnly cookies."),
        ("Bcrypt Password Hashing", "Zero plain-text password storage; 10 salt rounds with automated pre-save hooks."),
        ("CORS & Sanitization", "Configurable CORS origins, express JSON payload caps, and XSS sanitization across all chat endpoints.")
    ], badge="SECURITY", accent_color=YELLOW)

    add_card(s12, 4.8, 1.8, 3.7, 4.8, "High-Throughput Performance", [
        ("Concurrent Model Swarm", "Dispatches screenplay, masterclass, and FAQs in parallel via Promise.allSettled."),
        ("Sub-40s Total Turnaround", "Complete multi-model package generated in under 40 seconds on live Meta endpoints."),
        ("Local WebP Image Storage", "Zero cloud egress delay; thumbnails served directly via Express static file cache.")
    ], badge="SPEED", accent_color=CYAN)

    add_card(s12, 8.8, 1.8, 3.7, 4.8, "Server Scalability", [
        ("Stateless Node.js Layer", "Easily containerized with Docker and auto-scaled across Kubernetes worker pods."),
        ("Client-Side Rendering Offload", "Canvas rendering and WebM video encoding happen on the client GPU, keeping server load near zero."),
        ("MongoDB Atlas Clustering", "Auto-sharded database with high-availability replication clusters.")
    ], badge="SCALABILITY", accent_color=EMERALD)
    add_footer(s12)

    # =========================================================================
    # SLIDE 13: Comparative Analysis & Competitive Edge
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, 13, "Competitive Analysis", "Market Comparison: Why VideoTube Wins", "Redefining the Competitive Landscape")

    add_card(s13, 0.8, 1.8, 3.7, 4.8, "Traditional Video Editing", [
        ("Cost", "$300 - $600/yr (Adobe Premiere / Final Cut Pro)."),
        ("Time", "4 - 8 hours per finished video."),
        ("Complexity", "Steep learning curve; requires keyframing, audio mixing, rendering."),
        ("Output", "Only video; zero interactive technical masterclass.")
    ], badge="LEGACY", accent_color=RGBColor(244, 63, 94))

    add_card(s13, 4.8, 1.8, 3.7, 4.8, "Generic AI Video Wrappers", [
        ("Cost", "$30 - $120/mo in third-party API subscription credits."),
        ("Architecture", "Single general LLM prompt wrapper with basic text overlays."),
        ("Depth", "Shallow, generic bullet points; no real systems architecture."),
        ("Lock-in", "Tied to OpenAI / ElevenLabs proprietary cloud APIs.")
    ], badge="COMPETITORS", accent_color=YELLOW)

    add_card(s13, 8.8, 1.8, 3.7, 4.8, "VideoTube AI Studio", [
        ("Cost", "100% Free with Meta developer API key."),
        ("Time", "Under 40 seconds total production time."),
        ("Multi-Model Swarm", "Orchestrates 5 specialized Meta AI models collaboratively."),
        ("Depth", "Playable 60fps video + 15,000+ char technical masterclass dossier.")
    ], badge="VIDEOTUBE", accent_color=EMERALD)
    add_footer(s13)

    # =========================================================================
    # SLIDE 14: Roadmap, Future Enhancements & Conclusion
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, 14, "Conclusion & Roadmap", "Future Roadmap & Strategic Vision", "The Next Evolution of VideoTube")

    add_card(s14, 0.8, 1.8, 5.7, 4.8, "Development Roadmap (2026 - 2027)", [
        ("Phase 1: Meta Voice Clone & TTS", "Integrate native muse-voice-transcribe-1.0 and neural voice cloning for ultra-realistic narration accents."),
        ("Phase 2: Automated Multi-Platform Publishing", "Direct YouTube Data API v3 and LinkedIn Video API publishing with one-click scheduling."),
        ("Phase 3: Multi-Scene Generative B-Roll", "Generate distinct 1024x1024 WebP visual keyframes for every individual scene act."),
        ("Phase 4: Collaborative Team Workspaces", "Multi-user editorial review, brand voice presets, and enterprise team analytics.")
    ], badge="ROADMAP", accent_color=CYAN)

    add_card(s14, 6.8, 1.8, 5.7, 4.8, "Conclusion & Key Takeaways", [
        ("Autonomous Creation", "VideoTube proves that multi-model AI can autonomously produce high-fidelity video content and deep education."),
        ("Real-World Engineering", "Combines rock-solid Node.js/MongoDB backend design with cutting-edge Meta AI models."),
        ("Zero Vendor Lock-In", "A self-contained, open, and extensible platform powered entirely by your Meta API key."),
        ("Live & Ready Today", "Fully functional, verified, and running live at http://localhost:8000.")
    ], badge="SUMMARY", accent_color=EMERALD)
    add_footer(s14)

    # Save presentation
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    out = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else "VideoTube_Meta_AI_Presentation.pptx")
    create_deck(out)
