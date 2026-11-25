"use client";
// Reads, saves, and deletes progress photos in the browser (v1 storage).
import { useMemo, useSyncExternalStore } from "react";
import { newestFirst, parseProgressPhotos, type ProgressPhoto } from "./progressPhotos";

export const PHOTOS_KEY = "fct.v1.progress-photos";
const CHANGED = "fct:progress-photos-changed";

function subscribe(onChange: () => void) {
  window.addEventListener("storage", onChange);
  window.addEventListener(CHANGED, onChange);
  return () => {
    window.removeEventListener("storage", onChange);
    window.removeEventListener(CHANGED, onChange);
  };
}

function readRaw(): string | null {
  try {
    return window.localStorage.getItem(PHOTOS_KEY);
  } catch {
    return null;
  }
}

function write(list: ProgressPhoto[]): boolean {
  try {
    window.localStorage.setItem(PHOTOS_KEY, JSON.stringify(list));
    window.dispatchEvent(new Event(CHANGED));
    return true;
  } catch {
    return false; // for example storage is full
  }
}

export function addProgressPhoto(photo: Omit<ProgressPhoto, "id">): boolean {
  const id = typeof crypto !== "undefined" && "randomUUID" in crypto ? crypto.randomUUID() : String(Date.now());
  return write([...parseProgressPhotos(readRaw()), { ...photo, id }]);
}

/** Removes the photo for good (Later-AC5). */
export function deleteProgressPhoto(id: string): boolean {
  return write(parseProgressPhotos(readRaw()).filter((p) => p.id !== id));
}

export function useProgressPhotos(): { loaded: boolean; photos: ProgressPhoto[] } {
  const raw = useSyncExternalStore(subscribe, readRaw, () => undefined);
  const photos = useMemo(() => (raw === undefined ? [] : newestFirst(parseProgressPhotos(raw))), [raw]);
  return { loaded: raw !== undefined, photos };
}
