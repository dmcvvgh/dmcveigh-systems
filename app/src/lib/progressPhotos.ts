// Progress photos saved from the "not a meal" screen (S1-AC3). Kept on this device only, and the
// user can delete them (Later-AC4, Later-AC5).

export interface ProgressPhoto {
  id: string;
  date: string; // yyyy-mm-dd
  image: string; // small picture stored as a data URL
}

/** Reads saved progress photos from text. Damaged entries are skipped. */
export function parseProgressPhotos(raw: string | null): ProgressPhoto[] {
  if (!raw) return [];
  try {
    const list = JSON.parse(raw) as unknown;
    if (!Array.isArray(list)) return [];
    return list.filter(
      (p): p is ProgressPhoto =>
        !!p && typeof p.id === "string" && typeof p.date === "string" && typeof p.image === "string" && p.image.startsWith("data:image/"),
    );
  } catch {
    return [];
  }
}

/** Newest first. */
export function newestFirst(photos: ProgressPhoto[]): ProgressPhoto[] {
  return [...photos].sort((a, b) => b.date.localeCompare(a.date));
}
