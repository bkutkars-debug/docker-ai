import { randomBytes } from "node:crypto";
import { mkdirSync } from "node:fs";
import { dirname, extname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import multer from "multer";

const uploadDirectory = resolve(
  dirname(fileURLToPath(import.meta.url)),
  "../../public/temp"
);

mkdirSync(uploadDirectory, { recursive: true });

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, uploadDirectory);
  },
  filename: function (req, file, cb) {
    randomBytes(16, function (err, raw) {
      if (err) return cb(err);
      cb(null, `${raw.toString("hex")}${extname(file.originalname)}`);
    });
  },
});

export const upload = multer({ storage });
