import { Router } from "express";
import {
    handleAiPrompt,
    handleCreateVideoPackage,
    handleSaveVideo,
    handleGenerateMetadata,
    handleGenerateScript,
    handleSummarizeVideo,
    handleThumbnailIdeas,
    handleGenerateThumbnailImage,
    handleCodeArchitecture,
    handleCompareModels,
    handleContentModeration,
    handleListModels,
} from "../controllers/ai.controllers.js";
import { optionalJWT } from "../middlewares/auth.middleware.js";

const router = Router();

// 1. Live Meta AI Models
router.route("/models").get(handleListModels);

// 2. Chat with ANY Meta AI Model & Smart Video Intent Detection
router.route("/chat").post(optionalJWT, handleAiPrompt);

// 3. Complete Video Production Package (On User Permission)
router.route("/create-video").post(optionalJWT, handleCreateVideoPackage);

// 4. Save Generated Video to VideoTube Database
router.route("/save-video").post(optionalJWT, handleSaveVideo);

// 5. REAL AI Image Thumbnail Generator (powered by Meta muse-image-1.0)
router.route("/generate-thumbnail-image").post(optionalJWT, handleGenerateThumbnailImage);

// 6. Backend & MongoDB Code Architect (powered by Meta muse-spark-1.3-contributor)
router.route("/code-architect").post(optionalJWT, handleCodeArchitecture);

// 7. Full YouTube Script Generator (powered by Meta muse-wonder-1.0)
router.route("/script").post(optionalJWT, handleGenerateScript);

// 8. Video SEO & Tags Generator (powered by Meta muse-spark-1.3)
router.route("/metadata").post(optionalJWT, handleGenerateMetadata);

// 9. Multi-Model Benchmarking / Comparison
router.route("/compare").post(optionalJWT, handleCompareModels);

// 10. Video Content & Transcript Summarizer
router.route("/summarize").post(optionalJWT, handleSummarizeVideo);

// 11. Thumbnail Psychology & Concept Ideas
router.route("/thumbnails").post(optionalJWT, handleThumbnailIdeas);

// 12. Content & Comment Safety Moderation
router.route("/moderate").post(optionalJWT, handleContentModeration);

export default router;
