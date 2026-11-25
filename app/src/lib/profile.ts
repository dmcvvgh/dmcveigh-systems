// What the user told us at set-up, and how it is saved in the browser (v1 storage).
import { missingBiometrics, type Biometrics, type Direction } from "./budget";

export interface SavedGoal {
  direction: Direction;
  amountLb: number;
  targetDate: string; // yyyy-mm-dd
}

export interface Profile {
  biometrics: Biometrics;
  goal: SavedGoal;
  heavyDays: number[]; // 0 = Sunday ... 6 = Saturday
}

export const PROFILE_KEY = "fct.v1.profile";
const DAY_MS = 24 * 60 * 60 * 1000;

/** Whole weeks from `today` to `targetDate` (can be a fraction). */
export function weeksUntil(targetDate: string, today: Date): number {
  const target = new Date(`${targetDate}T00:00:00`);
  const start = new Date(today.getFullYear(), today.getMonth(), today.getDate());
  return (target.getTime() - start.getTime()) / DAY_MS / 7;
}

/** Checks the goal form. Returns an error message, or null when the goal is fine (S3-AC3). */
export function validateGoal(
  input: { direction?: string; amountLb?: number; targetDate?: string },
  today: Date,
): string | null {
  if (input.direction !== "cut" && input.direction !== "bulk") return "Choose cut or bulk.";
  if (typeof input.amountLb !== "number" || !Number.isFinite(input.amountLb) || input.amountLb <= 0)
    return "Enter how many pounds, like 10.";
  if (!input.targetDate || Number.isNaN(Date.parse(input.targetDate))) return "Pick a target date.";
  if (weeksUntil(input.targetDate, today) < 1) return "Pick a target date at least a week from today.";
  return null;
}

/** Reads a saved profile from text. Returns null if it is missing or damaged. */
export function parseProfile(raw: string | null): Profile | null {
  if (!raw) return null;
  try {
    const p = JSON.parse(raw) as Profile;
    if (missingBiometrics(p.biometrics ?? {}).length > 0) return null;
    const g = p.goal;
    if (!g || (g.direction !== "cut" && g.direction !== "bulk")) return null;
    if (typeof g.amountLb !== "number" || !(g.amountLb > 0) || !g.targetDate) return null;
    if (!Array.isArray(p.heavyDays)) return null;
    return p;
  } catch {
    return null;
  }
}
