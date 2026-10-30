import mongoose from "mongoose";
import { DB_NAME } from "../constants.js";

const connectDB = async () => {
  try {
    const mongoUrl = process.env.MONGODB_URL;
    if (!mongoUrl) {
      throw new Error("MONGODB_URL is not set in the environment.");
    }

    const connectionInstance = await mongoose.connect(mongoUrl, {
      dbName: DB_NAME,
    });

    console.log(`MONGODB connected: ${connectionInstance.connection.host}`);
  } catch (error) {
    console.error("MONGODB connection error:", error);
    process.exit(1);
  }
};

export default connectDB;
