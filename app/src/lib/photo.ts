// Checks a chosen photo file before we use it (S1-AC6). Runs in the browser and in tests.

export const MAX_PHOTO_BYTES = 10 * 1024 * 1024; // 10 MB (a placeholder limit from the spec)
export const PHOTO_ERROR = "Use a JPG or PNG under 10 MB";

const ALLOWED_TYPES = ["image/jpeg", "image/png"];

/** Returns an error message, or null when the file can be used. */
export function checkPhotoFile(file: { type: string; size: number }): string | null {
  if (!ALLOWED_TYPES.includes(file.type)) return PHOTO_ERROR;
  if (file.size > MAX_PHOTO_BYTES) return PHOTO_ERROR;
  return null;
}
