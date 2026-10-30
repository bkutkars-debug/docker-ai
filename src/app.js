import express from "express";
import cors from "cors";
import cookieParser from "cookie-parser";

const app = express();

app.use(
  cors({
    origin: process.env.CORS_ORIGIN || "*",
    credentials: true,
  })
);

app.use(express.json({ limit: "64kb" }));
app.use(express.urlencoded({ extended: true, limit: "64kb" }));
app.use(express.static("public"));
app.use(cookieParser());

// Route imports
import userRouter from "./routes/user.routes.js";
import aiRouter from "./routes/ai.routes.js";

// Routes declaration
app.use("/api/v1/users", userRouter);
app.use("/api/v1/ai", aiRouter);

// Health check / Welcome route
app.get("/health", (_, res) => {
  res.status(200).json({
    status: "OK",
    service: "VideoTube Backend with Meta AI",
    modelsPoweredBy: "Meta AI (Muse Spark & Muse Wonder)",
    timestamp: new Date().toISOString(),
  });
});

app.use((err, req, res, next) => {
  if (err instanceof SyntaxError && err.status === 400 && "body" in err) {
    return res.status(400).json({
      success: false,
      message: "Invalid JSON payload",
    });
  }

  if (err?.statusCode) {
    return res.status(err.statusCode).json({
      success: false,
      message: err.message,
      errors: err.errors || [],
    });
  }

  return res.status(500).json({
    success: false,
    message: err?.message || "Internal server error",
  });
});

export { app };
