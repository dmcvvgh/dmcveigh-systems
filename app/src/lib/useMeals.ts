"use client";
// Reads and saves meals in the browser (v1 storage). Same pattern as useProfile.
import { useMemo, useSyncExternalStore } from "react";
import { parseMeals, type Meal } from "./meals";

export const MEALS_KEY = "fct.v1.meals";
const CHANGED = "fct:meals-changed";

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
    return window.localStorage.getItem(MEALS_KEY);
  } catch {
    return null;
  }
}

/** Adds one meal. Returns false if the browser would not store it. */
export function addMeal(meal: Omit<Meal, "id">): boolean {
  try {
    const list = parseMeals(readRaw());
    const id = typeof crypto !== "undefined" && "randomUUID" in crypto ? crypto.randomUUID() : String(Date.now());
    list.push({ ...meal, id });
    window.localStorage.setItem(MEALS_KEY, JSON.stringify(list));
    window.dispatchEvent(new Event(CHANGED));
    return true;
  } catch {
    return false;
  }
}

/** `loaded` is false on the server and during the first browser render. */
export function useMeals(): { loaded: boolean; meals: Meal[] } {
  const raw = useSyncExternalStore(subscribe, readRaw, () => undefined);
  const meals = useMemo(() => (raw === undefined ? [] : parseMeals(raw)), [raw]);
  return { loaded: raw !== undefined, meals };
}
