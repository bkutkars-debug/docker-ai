import "dotenv/config";
import connectDB from "./db/index.js";
import { app } from "./app.js";

const port = process.env.PORT || 8000;

connectDB()
  .then(() => {
    app.listen(port, () => {
      console.log(`=================================================`);
      console.log(`🚀 VideoTube Server is running at http://localhost:${port}`);
      console.log(`🤖 Meta AI Studio UI: http://localhost:${port}`);
      console.log(`📡 Meta AI API base: http://localhost:${port}/api/v1/ai`);
      console.log(`=================================================`);
    });
  })
  .catch((err) => {
    console.error("MONGO db connection failed !!!", err);
    // Even if Mongo connection is retrying, start the server so AI tools can be used
    app.listen(port, () => {
      console.log(`⚠️ Server running without DB on http://localhost:${port} (AI endpoints active)`);
    });
  });
