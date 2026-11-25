"use client";
// Reads and saves workouts in the browser (v1 storage). Same pattern as useMeals.
import { useMemo, useSyncExternalStore } from "react";
import { parseWorkouts, type Workout } from "./workouts";

export const WORKOUTS_KEY = "fct.v1.workouts";
const CHANGED = "fct:workouts-changed";

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
    return window.localStorage.getItem(WORKOUTS_KEY);
  } catch {
    return null;
  }
}

/** Adds one workout. Returns false if the browser would not store it. */
export function addWorkout(workout: Omit<Workout, "id">): boolean {
  try {
    const list = parseWorkouts(readRaw());
    const id = typeof crypto !== "undefined" && "randomUUID" in crypto ? crypto.randomUUID() : String(Date.now());
    list.push({ ...workout, id });
    window.localStorage.setItem(WORKOUTS_KEY, JSON.stringify(list));
    window.dispatchEvent(new Event(CHANGED));
    return true;
  } catch {
    return false;
  }
}

/** `loaded` is false on the server and during the first browser render. */
export function useWorkouts(): { loaded: boolean; workouts: Workout[] } {
  const raw = useSyncExternalStore(subscribe, readRaw, () => undefined);
  const workouts = useMemo(() => (raw === undefined ? [] : parseWorkouts(raw)), [raw]);
  return { loaded: raw !== undefined, workouts };
}
