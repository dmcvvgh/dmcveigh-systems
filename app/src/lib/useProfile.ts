"use client";
// Reads and saves the profile in the browser. Works with server rendering: on the server there is
// no storage, so it reports "not loaded yet" and the screen waits instead of flashing wrong data.
import { useMemo, useSyncExternalStore } from "react";
import { parseProfile, PROFILE_KEY, type Profile } from "./profile";

const CHANGED = "fct:profile-changed";

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
    return window.localStorage.getItem(PROFILE_KEY);
  } catch {
    return null; // storage can be blocked, for example in a private window
  }
}

export function saveProfile(profile: Profile): boolean {
  try {
    window.localStorage.setItem(PROFILE_KEY, JSON.stringify(profile));
    window.dispatchEvent(new Event(CHANGED));
    return true;
  } catch {
    return false;
  }
}

/** `loaded` is false on the server and during the first browser render. */
export function useProfile(): { loaded: boolean; profile: Profile | null } {
  const raw = useSyncExternalStore(subscribe, readRaw, () => undefined);
  const profile = useMemo(() => (raw === undefined ? null : parseProfile(raw)), [raw]);
  return { loaded: raw !== undefined, profile };
}
