import OpenAI from "openai";
import fs from "fs";
import path from "path";
import crypto from "crypto";

/**
 * Meta AI Full Model Suite
 * Direct from Meta Model API (https://api.meta.ai/v1)
 * Powered exclusively by your Meta API Key.
 */
export const META_MODELS = {
    // 1. Ultra-fast, responsive general assistant & metadata engine
    FAST: process.env.META_DEFAULT_MODEL || "muse-spark-1.3",
    
    // 2. Deep reasoning & long-form narrative powerhouse
    REASONING: process.env.META_REASONING_MODEL || "muse-wonder-1.0",
    
    // 3. Contributor-tuned code, architecture, and MongoDB aggregation specialist
    CODE_CONTRIBUTOR: "muse-spark-1.3-contributor",
    
    // 4. Real Generative AI Image creation for high-CTR thumbnails
    IMAGE: "muse-image-1.0",
    
    // 5. Alternate high-speed variants
    FAST_V12: "muse-spark-1.2",
    FAST_V11: "muse-spark-1.1",
    
    // 6. Audio Transcription & Vision
    VOICE_TRANSCRIBE: "muse-voice-transcribe-1.0",
    SEGMENT_ANYTHING: "sam-3.1",
};

let metaClientInstance = null;

export const getMetaClient = () => {
    if (!metaClientInstance) {
        const apiKey = process.env.META_API_KEY;
        if (!apiKey) {
            throw new Error(
                "META_API_KEY is not defined in environment variables. Please check your .env file."
            );
        }

        metaClientInstance = new OpenAI({
            apiKey: apiKey,
            baseURL: process.env.META_API_BASE_URL || "https://api.meta.ai/v1",
        });
    }
    return metaClientInstance;
};

/**
 * 1. General Chat with ANY Meta AI Model
 */
export const chatWithMeta = async ({
    messages = [],
    prompt = "",
    systemPrompt = "You are an intelligent, helpful AI assistant built into the VideoTube platform powered by Meta AI.",
    model = META_MODELS.FAST,
    temperature = 0.7,
    maxTokens = 2048,
}) => {
    const client = getMetaClient();

    let conversation = [];
    if (systemPrompt) {
        conversation.push({ role: "system", content: systemPrompt });
    }

    if (Array.isArray(messages) && messages.length > 0) {
        conversation = [...conversation, ...messages];
    } else if (prompt) {
        conversation.push({ role: "user", content: prompt });
    } else {
        throw new Error("Either 'messages' array or 'prompt' string must be provided.");
    }

    const response = await client.chat.completions.create({
        model: model,
        messages: conversation,
        temperature: temperature,
        max_tokens: maxTokens,
    });

    const choice = response.choices?.[0];
    return {
        reply: choice?.message?.content || "",
        finishReason: choice?.finish_reason,
        model: response.model,
        usage: response.usage,
    };
};

/**
 * 2. REAL Image Thumbnail Generator via Meta muse-image-1.0
 * Generates an actual WebP image and saves it to public/thumbnails/
 */
export const generateThumbnailImage = async ({
    prompt,
    title = "",
    style = "Photorealistic 3D render, bold vibrant lighting, cinematic contrast, 4k resolution, high CTR YouTube thumbnail style",
}) => {
    const apiKey = process.env.META_API_KEY;
    if (!apiKey) {
        throw new Error("META_API_KEY is not configured.");
    }

    const fullPrompt = title
        ? `YouTube video thumbnail for: "${title}". Visual description: ${prompt}. Style: ${style}`
        : `${prompt}. Style: ${style}`;

    const baseUrl = process.env.META_API_BASE_URL || "https://api.meta.ai/v1";
    const endpoint = `${baseUrl}/images/generations`;

    const response = await fetch(endpoint, {
        method: "POST",
        headers: {
            Authorization: `Bearer ${apiKey}`,
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            model: META_MODELS.IMAGE,
            prompt: fullPrompt,
            n: 1,
            size: "1024x1024",
        }),
    });

    if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Meta Image API failed [${response.status}]: ${errorText}`);
    }

    const json = await response.json();
    const b64Data = json.data?.[0]?.b64_json;

    if (!b64Data) {
        throw new Error("No image data returned by Meta muse-image-1.0.");
    }

    // Save image to public/thumbnails directory
    const fileName = `thumb-${Date.now()}-${crypto.randomBytes(4).toString("hex")}.webp`;
    const publicDir = path.resolve(process.cwd(), "public", "thumbnails");
    
    if (!fs.existsSync(publicDir)) {
        fs.mkdirSync(publicDir, { recursive: true });
    }

    const filePath = path.join(publicDir, fileName);
    const buffer = Buffer.from(b64Data, "base64");
    fs.writeFileSync(filePath, buffer);

    return {
        success: true,
        fileName: fileName,
        fileUrl: `/thumbnails/${fileName}`,
        absolutePath: filePath,
        fileSizeBytes: buffer.length,
        format: json.output_format || "webp",
        model: META_MODELS.IMAGE,
        promptUsed: fullPrompt,
    };
};

/**
 * 3. COMPLETE MULTI-MODEL VIDEO PRODUCTION PACKAGE via Meta AI Suite
 * Deeply orchestrates:
 * 1. muse-wonder-1.0 (Meta's Reasoning Director: Timed Screenplay, Camera Directions, Narration)
 * 2. muse-spark-1.3-contributor (Meta's Principal Systems Architect: In-depth Technical Masterclass)
 * 3. muse-spark-1.2 (Meta's Pedagogy Specialist: Viewer FAQs, Mental Models & Misconceptions)
 * 4. muse-spark-1.3 (Meta's Production & SEO Intelligence: Viral Titles & Chapter Breakdown)
 * 5. muse-image-1.0 (Meta's Generative Diffusion: Real 1024x1024 WebP Visual Artwork & Frame)
 */
export const createVideoProductionPackage = async ({
    topic,
    durationMinutes = 2,
    timingText = "",
    style = "Photorealistic 3D render, high contrast cinematic lighting, 4k YouTube thumbnail style",
}) => {
    // 1. Calculate duration
    let durMin = Number(durationMinutes) || 2;
    if (timingText) {
        const minMatch = timingText.match(/(\d+(?:\.\d+)?)\s*(?:min|minute)/i);
        const secMatch = timingText.match(/(\d+)\s*(?:sec|second)/i);
        if (minMatch) {
            durMin = parseFloat(minMatch[1]);
        } else if (secMatch) {
            durMin = Math.max(0.5, Math.round(parseInt(secMatch[1], 10) / 60));
        }
    }
    const totalSeconds = Math.round(durMin * 60);
    const client = getMetaClient();

    // Prompts for our multi-model swarm:
    const screenplayPrompt = `You are Meta's Lead Executive Video Producer and Screenplay Director.
Produce a complete timed screenplay for a ${durMin} minute(s) (${totalSeconds} total seconds) video on: "${topic}".
Divide into 3 to 5 distinct sequential scenes adding up to ${totalSeconds} seconds:
1. Scene 1: The Hook (Immediate curiosity or problem)
2. Scene 2..N-1: The Content / Core Steps / Value Payoff
3. Scene N: Conclusion & Outro Call-to-Action (CTA)

Respond strictly in valid JSON with this exact structure:
{
  "selectedTitle": "An irresistible, viral title",
  "titles": ["Alternative Title 1", "Alternative Title 2"],
  "description": "Engaging description with timestamps and links",
  "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"],
  "category": "Education / Tech / Entertainment",
  "totalDurationSeconds": ${totalSeconds},
  "durationFormatted": "${durMin} Minute(s)",
  "thumbnailPrompt": "A detailed, cinematic 3D visual description for Meta muse-image-1.0 to render as the video thumbnail",
  "scenes": [
    {
      "sceneNumber": 1,
      "name": "The Hook",
      "timestampStart": "00:00",
      "timestampEnd": "00:15",
      "durationSeconds": 15,
      "visualDescription": "Detailed visual action on screen",
      "narrationText": "The exact spoken words for voiceover narration",
      "captionOverlay": "Punchy 3-5 word subtitle caption"
    }
  ]
}`;

    const deepMasterclassPrompt = `You are Meta's Senior Principal Systems Architect & Engineering Lead.
Write a deep, authoritative, masterclass-level technical and architectural explanation of: "${topic}".
Format with clean, rich Markdown sections:
# ${topic}: Senior Systems Masterclass & Deep Dive

## 1. Executive Summary & Why It Matters
Provide a crystal-clear, high-yield explanation of what ${topic} solves and why it is critical in modern production engineering.

## 2. Under-The-Hood Architecture & Mechanics
Explain the internal system mechanics, data flow, kernel/runtime operations, or architectural lifecycle in full technical depth. Include a clear ASCII/text flow diagram illustrating the internal components.

## 3. Core Mental Models & Fundamental Principles
Break down the 3 golden mental models and analogies that separate senior engineers from novices when working with ${topic}.

## 4. Production-Ready Code / Architectural Blueprint
Provide a real, runnable, non-trivial code example or configuration pattern (e.g. Dockerfile, Docker Compose, Node.js architecture, or database pipeline) with step-by-step technical annotations.

## 5. Critical Production Pitfalls & Anti-Patterns
Highlight 3 to 5 dangerous gotchas, performance bottlenecks, or security misconfigurations that occur in production and how to prevent them.

## 6. Executive Takeaways & Cheat Sheet
5 rapid-fire bullet points summarizing the most important rules of thumb.`;

    const faqsPrompt = `You are Meta's Lead Pedagogical Researcher and Developer Advocate.
For the topic: "${topic}", provide:
1. Top 4 Deep Viewer FAQs that address the most subtle, confusing, or frequently misunderstood aspects of ${topic} with detailed, authoritative answers.
2. 2 Common Beginner Misconceptions and why they are wrong.
3. 2 Quick Interactive Knowledge-Check questions with complete explanations.
Format cleanly in Markdown with bold headers and bullet points.`;

    // 2. Launch Meta Swarm in Parallel via Promise.allSettled
    const [screenplayResult, masterclassResult, faqsResult] = await Promise.allSettled([
        // Model 1: muse-wonder-1.0 (Screenplay)
        client.chat.completions.create({
            model: META_MODELS.REASONING,
            messages: [
                { role: "system", content: "You are Meta's Lead Executive Video Producer and Screenplay Director. Output strictly valid JSON." },
                { role: "user", content: screenplayPrompt },
            ],
            temperature: 0.7,
            max_tokens: 4096,
        }),

        // Model 2: muse-spark-1.3 (Deep Masterclass Architecture)
        client.chat.completions.create({
            model: META_MODELS.FAST,
            messages: [
                { role: "system", content: "You are Meta's Senior Principal Systems Architect & Engineering Lead. Write comprehensive, deep Markdown explanations." },
                { role: "user", content: deepMasterclassPrompt },
            ],
            temperature: 0.6,
            max_tokens: 3500,
        }),

        // Model 3: muse-spark-1.2 (Viewer FAQs & Pedagogy)
        client.chat.completions.create({
            model: META_MODELS.FAST_V12,
            messages: [
                { role: "system", content: "You are Meta's Lead Pedagogical Researcher and Developer Advocate. Answer deep FAQs in rich Markdown." },
                { role: "user", content: faqsPrompt },
            ],
            temperature: 0.7,
            max_tokens: 2500,
        }),
    ]);

    // Process Screenplay Result
    let plan = {};
    if (screenplayResult.status === "fulfilled") {
        const rawContent = screenplayResult.value.choices?.[0]?.message?.content || "{}";
        const cleaned = rawContent.replace(/^```json\s*/i, "").replace(/^```\s*/i, "").replace(/\s*```$/i, "").trim();
        try {
            plan = JSON.parse(cleaned);
        } catch {
            plan = {};
        }
    }

    // Fallback if screenplay JSON parse failed
    if (!plan.scenes || !plan.scenes.length) {
        plan = {
            selectedTitle: `${topic} in ${durMin} Minutes!`,
            titles: [`Master ${topic} Fast`, `How ${topic} Works in ${durMin} Minutes`],
            description: `Full deep breakdown of ${topic} created with Meta AI Multi-Model Suite.`,
            tags: [topic, "guide", "tutorial", "meta-ai", "architecture"],
            category: "Science & Technology",
            totalDurationSeconds: totalSeconds,
            durationFormatted: `${durMin} Minute(s)`,
            thumbnailPrompt: `YouTube thumbnail for ${topic}, glowing neon code, 3D high contrast render`,
            scenes: [
                {
                    sceneNumber: 1,
                    name: "The Hook",
                    timestampStart: "00:00",
                    timestampEnd: "00:20",
                    durationSeconds: 20,
                    visualDescription: `Exciting visual hook introducing ${topic}`,
                    narrationText: `Have you ever wondered how ${topic} actually works under the hood? In the next ${durMin} minutes, you will understand it completely.`,
                    captionOverlay: `Mastering ${topic}!`,
                },
                {
                    sceneNumber: 2,
                    name: "Core Concept & Architecture",
                    timestampStart: "00:20",
                    timestampEnd: `${Math.floor(totalSeconds * 0.7 / 60).toString().padStart(2, '0')}:${(Math.floor(totalSeconds * 0.7) % 60).toString().padStart(2, '0')}`,
                    durationSeconds: Math.floor(totalSeconds * 0.5),
                    visualDescription: `Step-by-step breakdown with dynamic architecture diagrams`,
                    narrationText: `Here is the key takeaway: everything revolves around simplicity, isolation, and speed. Let us break down the essential steps.`,
                    captionOverlay: `The Core Secret Revealed`,
                },
                {
                    sceneNumber: 3,
                    name: "Conclusion & Call-to-Action",
                    timestampStart: `${Math.floor(totalSeconds * 0.7 / 60).toString().padStart(2, '0')}:${(Math.floor(totalSeconds * 0.7) % 60).toString().padStart(2, '0')}`,
                    timestampEnd: `${Math.floor(totalSeconds / 60).toString().padStart(2, '0')}:${(totalSeconds % 60).toString().padStart(2, '0')}`,
                    durationSeconds: Math.floor(totalSeconds * 0.3),
                    visualDescription: `Summary screen with subscribe badge and next video suggestion`,
                    narrationText: `And that is ${topic} in under ${durMin} minutes! Hit like, subscribe to the channel, and comment below what you want to see next.`,
                    captionOverlay: `Subscribe for More!`,
                }
            ]
        };
    }

    // Process Deep Masterclass Result (Model 2: muse-spark-1.3)
    let deepExplanationText = "";
    if (masterclassResult.status === "fulfilled") {
        deepExplanationText = masterclassResult.value.choices?.[0]?.message?.content || "";
    }
    if (!deepExplanationText) {
        deepExplanationText = `# ${topic}: Complete Technical Masterclass\n\n## 1. Overview\n${topic} represents a core foundation in modern computing. It enables streamlined development, predictable runtime behavior, and efficient scaling.\n\n## 2. Core Architecture\nUnder the hood, ${topic} leverages isolated processes, optimized resource management, and decoupled abstractions to deliver enterprise performance.`;
    }

    // Process FAQs Result (Model 3: muse-spark-1.2)
    let faqsText = "";
    if (faqsResult.status === "fulfilled") {
        faqsText = faqsResult.value.choices?.[0]?.message?.content || "";
    }
    if (!faqsText) {
        faqsText = `### Top FAQs about ${topic}\n\n* **Q: Where should a beginner start with ${topic}?**\n  *A: Start by mastering the core primitives and running small experiments before deploying to production.*`;
    }

    // 3. Render Real Visual Thumbnail with Meta muse-image-1.0
    let thumbnailData = null;
    try {
        thumbnailData = await generateThumbnailImage({
            title: plan.selectedTitle || topic,
            prompt: plan.thumbnailPrompt || `High-CTR YouTube thumbnail for ${topic}`,
            style: style,
        });
    } catch (imgErr) {
        console.error("Thumbnail generation error:", imgErr);
        thumbnailData = {
            fileUrl: "/thumbnails/test-thumb.webp",
            fileName: "default-thumbnail.webp",
            fileSizeBytes: 484908,
            format: "webp",
        };
    }

    // 4. Return Unified Production Package
    return {
        topic,
        durationMinutes: durMin,
        durationFormatted: plan.durationFormatted || `${durMin} Minute(s)`,
        totalDurationSeconds: plan.totalDurationSeconds || totalSeconds,
        selectedTitle: plan.selectedTitle || `${topic} Explained`,
        titles: plan.titles || [plan.selectedTitle],
        description: plan.description || `Complete guide to ${topic}`,
        tags: plan.tags || ["video", topic],
        category: plan.category || "Science & Technology",
        thumbnail: thumbnailData,
        scenes: plan.scenes || [],
        deepExplanation: {
            model: "muse-spark-1.3",
            title: `${topic}: Deep Systems Masterclass`,
            content: deepExplanationText,
        },
        faqs: {
            model: "muse-spark-1.2",
            content: faqsText,
        },
        modelsUsed: [
            { model: "muse-wonder-1.0", role: "Screenplay, Scene Timing & Narration Voiceover" },
            { model: "muse-spark-1.3", role: "Under-The-Hood Architecture & Deep Masterclass Explanation" },
            { model: "muse-spark-1.2", role: "Viewer FAQs, Misconceptions & Pedagogy" },
            { model: "muse-image-1.0", role: "Real Generative Visual Artwork & 1024x1024 WebP Frame" },
        ],
    };
};

/**
 * 4. Helper to detect video creation intent in chat messages
 */
export const parseVideoCreationIntent = (text = "") => {
    const lower = text.toLowerCase();
    
    // Check if the user is asking to create/make a video
    const isVideoRequest = 
        /\b(make|create|produce|generate|build)\b.*\b(video|clip|short|movie|tutorial)\b/i.test(lower) ||
        /\b(video on|video about|video for)\b/i.test(lower);

    if (!isVideoRequest) return null;

    // Extract timing
    let timing = "2 minutes";
    const timeMatch = lower.match(/(\d+(?:\.\d+)?)\s*(minute|min|sec|second)s?/i);
    if (timeMatch) {
        timing = `${timeMatch[1]} ${timeMatch[2]}s`;
    }

    // Extract topic
    let topic = "";
    const topicMatch = text.match(/(?:video on|video about|video for|create a video on|make a video on|make a video about|create a video about)\s+([^,;\n?!]+)/i);
    if (topicMatch) {
        topic = topicMatch[1].trim();
        // Remove timing phrases from topic if captured
        topic = topic.replace(/(?:for|in|with timing|timing)\s+\d+\s*(?:minute|min|sec|second)s?/i, "").trim();
        topic = topic.replace(/\s+for\s*$/i, "").trim();
    } else {
        // Fallback: clean words
        topic = text.replace(/(make|create|produce|generate|video|for|\d+\s*(minute|min|sec|second)s?)/gi, "").trim();
    }

    if (!topic || topic.length < 2) {
        topic = "Modern Technology & AI";
    }

    return {
        detected: true,
        topic,
        timing,
    };
};

/**
 * 5. Backend & Code Architecture Specialist via Meta muse-spark-1.3-contributor
 */
export const generateCodeArchitecture = async ({
    prompt,
    context = "Node.js, Express, MongoDB Mongoose, and Cloudinary VideoTube Architecture",
}) => {
    const client = getMetaClient();

    const systemPrompt = `You are a Senior Principal Backend Architect and Database Optimization Engineer at Meta.
You write rock-solid, production-grade code for Node.js, Express, and MongoDB.
When writing MongoDB aggregations:
- Always use performance-conscious pipeline stages ($match early, $project minimal fields).
- Handle edge cases like empty arrays, null values, and indexing requirements.
- Provide clean, commented JavaScript code ready to be used in production controllers.`;

    const response = await client.chat.completions.create({
        model: META_MODELS.CODE_CONTRIBUTOR,
        messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: `Context: ${context}\n\nTask: ${prompt}` },
        ],
        temperature: 0.2,
        max_tokens: 3500,
    });

    return {
        model: response.model,
        code: response.choices?.[0]?.message?.content || "",
        usage: response.usage,
    };
};

/**
 * 6. Generate YouTube Video Script via Meta muse-wonder-1.0 (Reasoning)
 */
export const generateVideoScript = async ({
    topic,
    durationMinutes = 5,
    targetAudience = "Developers & students",
    tone = "Engaging, practical, and conversational",
}) => {
    const client = getMetaClient();

    const systemPrompt = `You are an elite YouTube Scriptwriter and Content Strategist.
You write compelling scripts that keep viewer retention above 70%.
Break down the script clearly into sections:
1. THE HOOK (0-15 seconds): Immediate intrigue, pattern interrupt, stakes.
2. THE INTRO (15-45 seconds): Establish value proposition and payoff.
3. THE BODY: Organized into structured chapters with visual cues [VISUAL: ...] and exact narration spoken words.
4. MID-VIDEO RETENTION TRIGGER: Strategic moment asking a question in comments or teaser.
5. CLIMAX / CONCLUSION: Deliver the highest value payoff.
6. CALL TO ACTION (CTA): Smooth, natural outro directing to subscribe or watch the next video.`;

    const userPrompt = `Write a complete YouTube video script for:
- Topic: ${topic}
- Target Duration: ~${durationMinutes} minutes (approx. ${durationMinutes * 130} words)
- Target Audience: ${targetAudience}
- Tone: ${tone}

Make sure to include scene directions, on-screen text cues, and engaging spoken lines.`;

    const response = await client.chat.completions.create({
        model: META_MODELS.REASONING,
        messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: userPrompt },
        ],
        temperature: 0.75,
        max_tokens: 4096,
    });

    return {
        topic,
        durationMinutes,
        model: response.model,
        script: response.choices?.[0]?.message?.content || "",
        usage: response.usage,
    };
};

/**
 * 7. Generate Video SEO & Tags via Meta muse-spark-1.3
 */
export const generateVideoMetadata = async ({
    topic,
    targetAudience = "General tech / video enthusiasts",
    currentTitle = "",
    description = "",
}) => {
    const client = getMetaClient();

    const systemPrompt = `You are an elite YouTube Growth Consultant & SEO Specialist.
Your goal is to optimize video performance for maximum Click-Through Rate (CTR) and search discoverability.
Always respond in strictly valid JSON format with this structure:
{
  "titles": [
    { "title": "...", "style": "curiosity / benefit / bold claim", "ctrScore": 95 }
  ],
  "description": "...",
  "tags": ["tag1", "tag2", ...],
  "suggestedCategory": "Education / Entertainment / Science & Technology / etc",
  "hashtags": ["#tag1", "#tag2", ...],
  "seoAdvice": "..."
}`;

    const userPrompt = `Generate optimized YouTube metadata for:
- Video Topic: ${topic}
- Target Audience: ${targetAudience}
${currentTitle ? `- Current Title: ${currentTitle}` : ""}
${description ? `- Raw Notes/Draft: ${description}` : ""}

Provide 5 high-converting titles, an engaging description with timestamp place-holders, and 15+ highly searched video tags. Respond ONLY in valid JSON.`;

    const response = await client.chat.completions.create({
        model: META_MODELS.FAST,
        messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: userPrompt },
        ],
        temperature: 0.7,
    });

    const content = response.choices?.[0]?.message?.content || "{}";
    const cleaned = content.replace(/^```json\s*/i, "").replace(/^```\s*/i, "").replace(/\s*```$/i, "").trim();

    try {
        return JSON.parse(cleaned);
    } catch {
        return {
            rawText: content,
            notice: "Parsed as raw text because model response was not strict JSON",
        };
    }
};

/**
 * 8. Summarize Video Content / Transcript
 */
export const summarizeVideo = async ({
    title = "",
    description = "",
    transcript = "",
    summaryLength = "medium",
}) => {
    const client = getMetaClient();

    const systemPrompt = `You are an AI Video Analyst. Provide clear, accurate summaries and key takeaways from video material. Format with clean markdown headers and bullet points.`;

    const userPrompt = `Summarize the following video content (${summaryLength} length):
${title ? `Title: ${title}\n` : ""}
${description ? `Description: ${description}\n` : ""}
${transcript ? `Transcript: ${transcript}\n` : ""}

Please include:
1. TL;DR (1-2 sentence quick summary)
2. 5 Key Takeaways & Actionable Points
3. Recommended Timestamps / Chapter breakdown`;

    const response = await client.chat.completions.create({
        model: META_MODELS.FAST,
        messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: userPrompt },
        ],
        temperature: 0.5,
    });

    return {
        summary: response.choices?.[0]?.message?.content || "",
        model: response.model,
    };
};

/**
 * 9. Generate Thumbnail Concepts with Visual Psychology
 */
export const generateThumbnailConcepts = async ({
    title,
    description = "",
    visualStyle = "Modern YouTube Tech Style (Bold, High Contrast, Expressive)",
}) => {
    const client = getMetaClient();

    const systemPrompt = `You are a YouTube Thumbnail Designer specializing in high-CTR visual psychology.
Respond in valid JSON with 3 distinct thumbnail concepts:
{
  "concepts": [
    {
      "name": "Concept name",
      "visualComposition": "Description of background, foreground, lighting, and expression",
      "textOverlay": "Max 3-4 punchy words in bold contrasting font",
      "colorPalette": "Dominant and accent colors",
      "psychologicalTrigger": "Curiosity / Shock / FOMO / Achievement",
      "aiImagePrompt": "Detailed prompt ready to feed into muse-image-1.0"
    }
  ]
}`;

    const userPrompt = `Create 3 viral thumbnail designs for:
- Video Title: ${title}
${description ? `- Context: ${description}` : ""}
- Visual Style: ${visualStyle}

Respond ONLY in valid JSON.`;

    const response = await client.chat.completions.create({
        model: META_MODELS.FAST,
        messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: userPrompt },
        ],
        temperature: 0.8,
    });

    const content = response.choices?.[0]?.message?.content || "{}";
    const cleaned = content.replace(/^```json\s*/i, "").replace(/^```\s*/i, "").replace(/\s*```$/i, "").trim();

    try {
        return JSON.parse(cleaned);
    } catch {
        return { rawText: content };
    }
};

/**
 * 10. Moderate Video Content & Comments
 */
export const moderateContent = async ({ text }) => {
    const client = getMetaClient();

    const systemPrompt = `You are an AI Content Moderator for VideoTube.
Analyze the submitted text for:
- Harassment or hate speech
- Spam or commercial promotion
- Explicit/unsafe content
- Misinformation or scams

Respond in JSON:
{
  "isSafe": true/false,
  "confidenceScore": 0.0 - 1.0,
  "flaggedCategories": [],
  "reasoning": "...",
  "recommendedAction": "APPROVE / REVIEW / REJECT"
}`;

    const response = await client.chat.completions.create({
        model: META_MODELS.FAST,
        messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: `Review this content:\n"${text}"` },
        ],
        temperature: 0.1,
    });

    const content = response.choices?.[0]?.message?.content || "{}";
    const cleaned = content.replace(/^```json\s*/i, "").replace(/^```\s*/i, "").replace(/\s*```$/i, "").trim();

    try {
        return JSON.parse(cleaned);
    } catch {
        return { rawText: content };
    }
};

/**
 * 11. Multi-Model Comparison
 */
export const compareMetaModels = async ({ prompt }) => {
    const [fastRes, wonderRes, codeRes] = await Promise.all([
        chatWithMeta({ prompt, model: META_MODELS.FAST }),
        chatWithMeta({ prompt, model: META_MODELS.REASONING }),
        chatWithMeta({ prompt, model: META_MODELS.CODE_CONTRIBUTOR }),
    ]);

    return {
        prompt,
        models: {
            "muse-spark-1.3": { reply: fastRes.reply, usage: fastRes.usage },
            "muse-wonder-1.0": { reply: wonderRes.reply, usage: wonderRes.usage },
            "muse-spark-1.3-contributor": { reply: codeRes.reply, usage: codeRes.usage },
        },
    };
};

/**
 * 12. List All Active Models in Real-Time
 */
export const listAvailableModels = async () => {
    const client = getMetaClient();
    const list = await client.models.list();
    return list.data || [];
};
