// Meals: what the user ate, the rules for saving one, and daily totals (S1-AC4, AC9, AC10).

export interface Meal {
  id: string;
  name: string;
  calories: number;
  protein: number;
  fats: number;
  carbs: number;
  eatenAt: string; // ISO date and time
  source: "hand" | "photo";
}

export interface MealInput {
  name: string;
  calories: string; // text from the form
  protein: string;
  fats: string;
  carbs: string;
  eatenAt: string; // ISO date and time
}

export const CALORIES_ERROR = "Enter calories as a number, like 450"; // S1-AC10
export const MACRO_ERROR = "Enter grams as a number, like 30";

export type MealResult = { ok: true; meal: Omit<Meal, "id" | "source"> } | { ok: false; errors: Record<string, string> };

function toNumber(text: string): number | null {
  const t = text.trim();
  if (t === "") return null;
  const n = Number(t);
  return Number.isFinite(n) && n >= 0 ? n : NaN;
}

/** Checks a meal typed in by hand. Calories are required; empty macros count as 0. */
export function validateMeal(input: MealInput): MealResult {
  const errors: Record<string, string> = {};
  const calories = toNumber(input.calories);
  if (calories === null || Number.isNaN(calories)) errors.calories = CALORIES_ERROR;
  const macros: Record<string, number> = {};
  for (const key of ["protein", "fats", "carbs"] as const) {
    const v = toNumber(input[key]);
    if (v !== null && Number.isNaN(v)) errors[key] = MACRO_ERROR;
    else macros[key] = v ?? 0;
  }
  if (Number.isNaN(Date.parse(input.eatenAt))) errors.eatenAt = "Pick the time you ate.";
  if (Object.keys(errors).length > 0) return { ok: false, errors };
  return {
    ok: true,
    meal: {
      name: input.name.trim() || "Meal",
      calories: calories as number,
      protein: macros.protein,
      fats: macros.fats,
      carbs: macros.carbs,
      eatenAt: new Date(input.eatenAt).toISOString(),
    },
  };
}

/** yyyy-mm-dd for a moment, in the user's own time zone. */
export function dayKey(d: Date): string {
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${d.getFullYear()}-${m}-${day}`;
}

export interface Totals {
  calories: number;
  protein: number;
  fats: number;
  carbs: number;
}

/** Meals eaten on one day, oldest first. */
export function mealsOn(meals: Meal[], day: Date): Meal[] {
  const key = dayKey(day);
  return meals
    .filter((m) => dayKey(new Date(m.eatenAt)) === key)
    .sort((a, b) => a.eatenAt.localeCompare(b.eatenAt));
}

/** The day's totals of calories and each macro (S1-AC4). */
export function dayTotals(meals: Meal[], day: Date): Totals {
  return mealsOn(meals, day).reduce(
    (t, m) => ({
      calories: t.calories + m.calories,
      protein: t.protein + m.protein,
      fats: t.fats + m.fats,
      carbs: t.carbs + m.carbs,
    }),
    { calories: 0, protein: 0, fats: 0, carbs: 0 },
  );
}

/** Reads saved meals from text. Anything damaged is skipped, never a crash. */
export function parseMeals(raw: string | null): Meal[] {
  if (!raw) return [];
  try {
    const list = JSON.parse(raw) as unknown;
    if (!Array.isArray(list)) return [];
    return list.filter(
      (m): m is Meal =>
        !!m &&
        typeof m.id === "string" &&
        typeof m.name === "string" &&
        typeof m.calories === "number" &&
        typeof m.protein === "number" &&
        typeof m.fats === "number" &&
        typeof m.carbs === "number" &&
        typeof m.eatenAt === "string" &&
        !Number.isNaN(Date.parse(m.eatenAt)),
    );
  } catch {
    return [];
  }
}

/** Now, as text for a date-and-time box, in the user's own time zone. Call only in the browser. */
export function nowForInput(): string {
  const d = new Date();
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
  return d.toISOString().slice(0, 16);
}
