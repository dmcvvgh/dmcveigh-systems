// Workouts: what the user did, entered by hand in v1 (S2-AC1).

export interface Workout {
  id: string;
  date: string; // yyyy-mm-dd, the day it happened
  exercise: string;
  weightLb: number; // weight lifted; 0 for exercise with no weights
  caloriesBurned: number; // typed in by the user
}

export interface WorkoutInput {
  exercise: string;
  weightLb: string; // text from the form
  caloriesBurned: string;
  date: string;
}

export const EXERCISE_ERROR = "Enter the exercise, like Bench press";
export const WEIGHT_ERROR = "Enter pounds as a number, like 135";
export const BURNED_ERROR = "Enter calories burned as a number, like 250";
export const DATE_ERROR = "Pick the day you worked out.";

export type WorkoutResult = { ok: true; workout: Omit<Workout, "id"> } | { ok: false; errors: Record<string, string> };

function toNumber(text: string): number | null {
  const t = text.trim();
  if (t === "") return null;
  const n = Number(t);
  return Number.isFinite(n) && n >= 0 ? n : NaN;
}

/** Checks a workout typed in by hand. Empty weight or calories count as 0. */
export function validateWorkout(input: WorkoutInput): WorkoutResult {
  const errors: Record<string, string> = {};
  if (input.exercise.trim() === "") errors.exercise = EXERCISE_ERROR;
  const weight = toNumber(input.weightLb);
  if (weight !== null && Number.isNaN(weight)) errors.weightLb = WEIGHT_ERROR;
  const burned = toNumber(input.caloriesBurned);
  if (burned !== null && Number.isNaN(burned)) errors.caloriesBurned = BURNED_ERROR;
  if (!/^\d{4}-\d{2}-\d{2}$/.test(input.date) || Number.isNaN(Date.parse(input.date))) errors.date = DATE_ERROR;
  if (Object.keys(errors).length > 0) return { ok: false, errors };
  return {
    ok: true,
    workout: {
      date: input.date,
      exercise: input.exercise.trim(),
      weightLb: weight ?? 0,
      caloriesBurned: burned ?? 0,
    },
  };
}

/** Calories burned in logged workouts, added up for each day (yyyy-mm-dd). */
export function burnedByDate(workouts: Workout[]): Record<string, number> {
  const out: Record<string, number> = {};
  for (const w of workouts) out[w.date] = (out[w.date] ?? 0) + w.caloriesBurned;
  return out;
}

/** Reads saved workouts from text. Damaged entries are skipped, never a crash. */
export function parseWorkouts(raw: string | null): Workout[] {
  if (!raw) return [];
  try {
    const list = JSON.parse(raw) as unknown;
    if (!Array.isArray(list)) return [];
    return list.filter(
      (w): w is Workout =>
        !!w &&
        typeof w.id === "string" &&
        typeof w.date === "string" &&
        typeof w.exercise === "string" &&
        typeof w.weightLb === "number" &&
        typeof w.caloriesBurned === "number",
    );
  } catch {
    return [];
  }
}
