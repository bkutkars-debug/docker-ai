import { ApiError } from "../utils/ApiError.js";
import { asyncHandler } from "../utils/asyncHandler.js";
import jwt from "jsonwebtoken";
import { User } from "../models/user.models.js";

/**
 * Strict JWT Verification Middleware
 * Requires a valid accessToken in cookies or Authorization: Bearer <token>
 */
export const verifyJWT = asyncHandler(async (req, _, next) => {
    try {
        const token =
            req.cookies?.accessToken ||
            req.header("Authorization")?.replace("Bearer ", "");

        if (!token) {
            throw new ApiError(401, "Unauthorized request: No access token provided");
        }

        const decodedToken = jwt.verify(
            token,
            process.env.ACCESS_TOKEN_SECRET || "chai-aur-code"
        );

        const user = await User.findById(decodedToken?._id).select(
            "-password -refreshToken"
        );

        if (!user) {
            throw new ApiError(401, "Invalid Access Token: User not found");
        }

        req.user = user;
        next();
    } catch (error) {
        throw new ApiError(401, error?.message || "Invalid access token");
    }
});

/**
 * Optional JWT Verification Middleware
 * If a token is provided and valid, attaches req.user.
 * If no token is provided, proceeds with req.user = null without throwing 401.
 */
export const optionalJWT = asyncHandler(async (req, _, next) => {
    try {
        const token =
            req.cookies?.accessToken ||
            req.header("Authorization")?.replace("Bearer ", "");

        if (token) {
            const decodedToken = jwt.verify(
                token,
                process.env.ACCESS_TOKEN_SECRET || "chai-aur-code"
            );
            const user = await User.findById(decodedToken?._id).select(
                "-password -refreshToken"
            );
            if (user) {
                req.user = user;
            }
        }
    } catch {
        // Silently continue for optional auth
        req.user = null;
    }
    next();
});
