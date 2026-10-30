import { asyncHandler } from "../utils/asyncHandler.js";
import { ApiError } from "../utils/ApiError.js";
import { ApiResponse } from "../utils/ApiResponse.js";
import { Video } from "../models/video.models.js";
import {
    chatWithMeta,
    createVideoProductionPackage,
    parseVideoCreationIntent,
    generateVideoMetadata,
    generateVideoScript,
    summarizeVideo,
    generateThumbnailConcepts,
    generateThumbnailImage,
    generateCodeArchitecture,
    compareMetaModels,
    moderateContent,
    listAvailableModels,
    META_MODELS,
} from "../services/metaAi.service.js";

/**
 * 1. General Chat with ANY Meta AI Model & Smart Video Intent Detection
 * POST /api/v1/ai/chat
 * If user says "Make a video on X for Y minutes", it requests permission or generates the video package!
 */
export const handleAiPrompt = asyncHandler(async (req, res) => {
    const { prompt, messages, model, confirmed, timing, topic: clientTopic } = req.body ?? {};

    // Safely extract user text
    const userText = (typeof prompt === "string" ? prompt : "") || 
                     (Array.isArray(messages) && messages.length > 0 ? messages[messages.length - 1]?.content : "") || 
                     "";

    // 1. Check if user explicitly confirmed video creation
    if (confirmed && clientTopic) {
        const videoPkg = await createVideoProductionPackage({
            topic: clientTopic,
            timingText: timing || "2 minutes",
        });

        const previewSnippet = videoPkg.deepExplanation?.content
            ? videoPkg.deepExplanation.content.split("\n\n").slice(0, 3).join("\n\n")
            : `Deep architectural analysis of ${videoPkg.topic}`;

        const modelNames = (videoPkg.modelsUsed || [])
            .map((m) => (typeof m === "string" ? m : m.model))
            .join(", ");

        return res.status(200).json(
            new ApiResponse(
                200,
                {
                    reply: `🎬 **Video Production Package & Deep Topic Masterclass Generated on Your Permission!**\n\n* **Topic:** **${videoPkg.topic}**\n* **Target Duration:** **${videoPkg.durationFormatted}**\n* **Selected Title:** **${videoPkg.selectedTitle}**\n* **Meta AI Multi-Model Swarm:** ${modelNames}\n\n---\n\n### 📘 Deep Topic Technical Overview:\n${previewSnippet}\n\n*(Full Interactive 60fps Video Player & Deep Masterclass Dossier rendered below)*`,
                    videoPackage: videoPkg,
                    model: "Meta AI Multi-Model Suite (Wonder + Spark + Image)",
                },
                "Video package created successfully upon user permission"
            )
        );
    }

    if (!userText.trim()) {
        throw new ApiError(400, "Please provide either a 'prompt' string or a 'messages' array.");
    }

    // 2. Check if the message contains intent to create a video
    const videoIntent = parseVideoCreationIntent(userText);
    const hasImmediateConfirmation = /\b(yes|proceed|confirm|go ahead|do it)\b/i.test(userText);

    if (videoIntent && !hasImmediateConfirmation) {
        return res.status(200).json(
            new ApiResponse(
                200,
                {
                    reply: `🎬 **Video Creation Request Detected!**\n\n* **Topic:** **${videoIntent.topic}**\n* **Timing:** **${videoIntent.timing}**\n\nI am ready to deploy Meta's multi-model suite:\n- 🧠 **muse-wonder-1.0**: Timed scene-by-scene screenplay & voiceover narration\n- 🔬 **muse-spark-1.3**: Deep technical under-the-hood masterclass explanation & systems architecture\n- 💡 **muse-spark-1.2**: In-depth viewer FAQs, conceptual mental models & pedagogical insights\n- 🎨 **muse-image-1.0**: Real 1024x1024 WebP visual artwork & HD thumbnail\n\n👉 **Would you like me to proceed with creating this video and deep masterclass on your permission?**`,
                    actionRequired: {
                        type: "CONFIRM_VIDEO_CREATION",
                        topic: videoIntent.topic,
                        timing: videoIntent.timing,
                    },
                    model: META_MODELS.FAST,
                },
                "Video creation confirmation requested"
            )
        );
    }

    // 3. If user said "Yes" right after a video request or prompt asks to make it directly
    if (videoIntent && hasImmediateConfirmation) {
        const videoPkg = await createVideoProductionPackage({
            topic: videoIntent.topic,
            timingText: videoIntent.timing,
        });

        const previewSnippet = videoPkg.deepExplanation?.content
            ? videoPkg.deepExplanation.content.split("\n\n").slice(0, 3).join("\n\n")
            : `Deep architectural analysis of ${videoPkg.topic}`;

        return res.status(200).json(
            new ApiResponse(
                200,
                {
                    reply: `🎬 **Video Production Package & Deep Topic Masterclass Generated!**\n\n* **Topic:** **${videoPkg.topic}**\n* **Target Duration:** **${videoPkg.durationFormatted}**\n* **Selected Title:** **${videoPkg.selectedTitle}**\n* **Meta AI Multi-Model Swarm:** \`muse-wonder-1.0\`, \`muse-spark-1.3\`, \`muse-spark-1.2\`, \`muse-image-1.0\`\n\n---\n\n### 📘 Deep Topic Technical Overview:\n${previewSnippet}\n\n*(Full Interactive 60fps Video Player & Deep Masterclass Dossier rendered below)*`,
                    videoPackage: videoPkg,
                    model: "Meta AI Multi-Model Suite",
                },
                "Video created on user confirmation"
            )
        );
    }

    // Standard chat completion
    const selectedModel = model || META_MODELS.FAST;
    const result = await chatWithMeta({
        prompt: userText,
        messages,
        model: selectedModel,
    });

    return res.status(200).json(
        new ApiResponse(200, result, `Response generated successfully via Meta ${selectedModel}`)
    );
});

/**
 * 2. Dedicated Video Production Endpoint (On User Permission)
 * POST /api/v1/ai/create-video
 * Body: { topic: string, timing?: string, durationMinutes?: number, style?: string }
 */
export const handleCreateVideoPackage = asyncHandler(async (req, res) => {
    const { topic, timing, durationMinutes, style } = req.body ?? {};

    if (!topic || typeof topic !== "string" || topic.trim() === "") {
        throw new ApiError(400, "Field 'topic' is required to create a video.");
    }

    const videoPkg = await createVideoProductionPackage({
        topic: topic.trim(),
        timingText: timing,
        durationMinutes,
        style,
    });

    return res.status(201).json(
        new ApiResponse(201, videoPkg, "Complete video production generated via Meta AI Suite")
    );
});

/**
 * 3. Save Generated Video to MongoDB Database
 * POST /api/v1/ai/save-video
 * Body: { title, description, duration, thumbnail, videoFile }
 */
export const handleSaveVideo = asyncHandler(async (req, res) => {
    const { title, description, duration, thumbnail, videoFile } = req.body ?? {};

    if (!title) {
        throw new ApiError(400, "Title is required to save video.");
    }

    const savedVideo = await Video.create({
        title: title.trim(),
        description: description || "Created with Meta AI",
        duration: duration ? Number(duration) : 120,
        thumbnail: thumbnail || "/thumbnails/test-thumb.webp",
        videoFile: videoFile || thumbnail || "/thumbnails/test-thumb.webp",
        isPublished: true,
        owner: req.user?._id || null,
    });

    return res.status(201).json(
        new ApiResponse(201, savedVideo, "Video saved successfully to VideoTube database!")
    );
});

/**
 * 4. REAL Image Thumbnail Generator via Meta muse-image-1.0
 * POST /api/v1/ai/generate-thumbnail-image
 */
export const handleGenerateThumbnailImage = asyncHandler(async (req, res) => {
    const { prompt, title, style } = req.body ?? {};

    if (!prompt && !title) {
        throw new ApiError(400, "Either a 'prompt' or 'title' is required to generate a thumbnail image.");
    }

    const imageResult = await generateThumbnailImage({
        prompt: prompt || `Click-worthy YouTube thumbnail for video: ${title}`,
        title,
        style,
    });

    return res.status(201).json(
        new ApiResponse(201, imageResult, "Real YouTube thumbnail generated successfully via Meta muse-image-1.0")
    );
});

/**
 * 4b. Brainstorm Thumbnail Concept Psychology
 * POST /api/v1/ai/thumbnails
 */
export const handleThumbnailIdeas = asyncHandler(async (req, res) => {
    const { title, description, visualStyle } = req.body ?? {};

    if (!title || typeof title !== "string" || title.trim() === "") {
        throw new ApiError(400, "Field 'title' is required to brainstorm thumbnail concepts.");
    }

    const thumbnailData = await generateThumbnailConcepts({
        title: title.trim(),
        description,
        visualStyle,
    });

    return res.status(200).json(
        new ApiResponse(200, thumbnailData, "Thumbnail concepts generated successfully via Meta AI")
    );
});

/**
 * 5. Backend & MongoDB Code Architect via Meta muse-spark-1.3-contributor
 * POST /api/v1/ai/code-architect
 */
export const handleCodeArchitecture = asyncHandler(async (req, res) => {
    const { prompt, context } = req.body ?? {};

    if (!prompt || typeof prompt !== "string" || prompt.trim() === "") {
        throw new ApiError(400, "Field 'prompt' is required for code architecture.");
    }

    const codeResult = await generateCodeArchitecture({
        prompt: prompt.trim(),
        context,
    });

    return res.status(200).json(
        new ApiResponse(200, codeResult, "Code architecture generated successfully via Meta muse-spark-1.3-contributor")
    );
});

/**
 * 6. Generate Complete YouTube Script via Meta muse-wonder-1.0 (Reasoning)
 * POST /api/v1/ai/script
 */
export const handleGenerateScript = asyncHandler(async (req, res) => {
    const { topic, durationMinutes, targetAudience, tone } = req.body ?? {};

    if (!topic || typeof topic !== "string" || topic.trim() === "") {
        throw new ApiError(400, "Field 'topic' is required to generate a video script.");
    }

    const duration = durationMinutes ? Number(durationMinutes) : 5;

    const scriptData = await generateVideoScript({
        topic: topic.trim(),
        durationMinutes: duration,
        targetAudience,
        tone,
    });

    return res.status(200).json(
        new ApiResponse(200, scriptData, "YouTube script generated successfully via Meta muse-wonder-1.0")
    );
});

/**
 * 7. Generate Video SEO & Tags via Meta muse-spark-1.3
 * POST /api/v1/ai/metadata
 */
export const handleGenerateMetadata = asyncHandler(async (req, res) => {
    const { topic, targetAudience, currentTitle, description } = req.body ?? {};

    if (!topic || typeof topic !== "string" || topic.trim() === "") {
        throw new ApiError(400, "Field 'topic' is required to generate video metadata.");
    }

    const metadata = await generateVideoMetadata({
        topic: topic.trim(),
        targetAudience,
        currentTitle,
        description,
    });

    return res.status(200).json(
        new ApiResponse(200, metadata, "Video SEO metadata generated successfully via Meta AI")
    );
});

/**
 * 8. Summarize Video Content / Transcript
 * POST /api/v1/ai/summarize
 */
export const handleSummarizeVideo = asyncHandler(async (req, res) => {
    const { title, description, transcript, summaryLength } = req.body ?? {};

    if (!title && !description && !transcript) {
        throw new ApiError(
            400,
            "At least one of 'title', 'description', or 'transcript' must be provided to summarize."
        );
    }

    const summaryData = await summarizeVideo({
        title,
        description,
        transcript,
        summaryLength,
    });

    return res.status(200).json(
        new ApiResponse(200, summaryData, "Video summary generated successfully via Meta AI")
    );
});

/**
 * 9. Multi-Model Comparison
 * POST /api/v1/ai/compare
 */
export const handleCompareModels = asyncHandler(async (req, res) => {
    const { prompt } = req.body ?? {};

    if (!prompt || typeof prompt !== "string" || prompt.trim() === "") {
        throw new ApiError(400, "Field 'prompt' is required for multi-model comparison.");
    }

    const comparison = await compareMetaModels({ prompt: prompt.trim() });

    return res.status(200).json(
        new ApiResponse(200, comparison, "Multi-model comparison completed across Meta AI models")
    );
});

/**
 * 10. Content Moderation
 * POST /api/v1/ai/moderate
 */
export const handleContentModeration = asyncHandler(async (req, res) => {
    const { text } = req.body ?? {};

    if (!text || typeof text !== "string" || text.trim() === "") {
        throw new ApiError(400, "Field 'text' is required for moderation.");
    }

    const modResult = await moderateContent({ text: text.trim() });

    return res.status(200).json(
        new ApiResponse(200, modResult, "Content moderation evaluated successfully via Meta AI")
    );
});

/**
 * 11. List All Meta AI Models
 * GET /api/v1/ai/models
 */
export const handleListModels = asyncHandler(async (_, res) => {
    const models = await listAvailableModels();
    return res.status(200).json(
        new ApiResponse(
            200,
            {
                configuredDefaults: META_MODELS,
                availableModels: models,
            },
            "Available Meta AI models retrieved successfully"
        )
    );
});
