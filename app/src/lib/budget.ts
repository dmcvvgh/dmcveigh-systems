// Budget rules for S3 (weekly calorie budget, heavy and rest days, unsafe goals).
// Pure functions: no screen, no storage, so they are easy to test.

export type Sex = "female" | "male";
export type Intensity = "light" | "moderate" | "high";
export type Direction = "cut" | "bulk";

export interface Biometrics {
  sex: Sex;
  age: number;
  heightIn: number; // inches
  weightLb: number; // pounds
  intensity: Intensity;
}

export interface Goal {
  direction: Direction;
  amountLb: number; // how many pounds to lose or gain
  weeks: number; // time until the target date, in weeks
}

export const CALORIES_PER_POUND = 3500; // rough rule of thumb (S3-AC7)
export const MAX_LOSS_LB_PER_WEEK = 2; // unsafe above this (S3-AC10)
export const DAILY_FLOOR = 1200; // unsafe below this (S3-AC10)

// Standard activity multipliers used with the Mifflin-St Jeor formula.
const ACTIVITY: Record<Intensity, number> = {
  light: 1.375,
  moderate: 1.55,
  high: 1.725,
};

// Heavy lifting days get a bigger share of the week's calories than rest days (S3-AC8).
const HEAVY_WEIGHT = 1.2;
const REST_WEIGHT = 0.8;

/** Calories a person burns in a day at their activity level, before any goal. */
export function maintenanceCalories(b: Biometrics): number {
  const kg = b.weightLb * 0.45359237;
  const cm = b.heightIn * 2.54;
  const base = 10 * kg + 6.25 * cm - 5 * b.age + (b.sex === "male" ? 5 : -161);
  return Math.round(base * ACTIVITY[b.intensity]);
}

/** Weekly calorie budget: seven days of maintenance, minus (cut) or plus (bulk) the goal. */
export function weeklyBudget(b: Biometrics, g: Goal): number {
  const weekly = maintenanceCalories(b) * 7;
  const change = (g.amountLb / g.weeks) * CALORIES_PER_POUND;
  return Math.round(g.direction === "cut" ? weekly - change : weekly + change);
}

export interface DayPlan {
  /** One number per weekday, index 0 = Sunday ... 6 = Saturday. */
  perDay: number[];
  /** True when no heavy days were picked, so the budget was split evenly (S3-AC9). */
  splitEvenly: boolean;
}

/** Splits the weekly budget across the seven days, giving heavy days more (S3-AC8). */
export function splitWeek(weekly: number, heavyDays: number[]): DayPlan {
  const heavy = new Set(heavyDays);
  if (heavy.size === 0 || heavy.size === 7) {
    const each = Math.round(weekly / 7);
    return { perDay: Array(7).fill(each), splitEvenly: heavy.size === 0 };
  }
  const weights = [0, 1, 2, 3, 4, 5, 6].map((d) => (heavy.has(d) ? HEAVY_WEIGHT : REST_WEIGHT));
  const total = weights.reduce((a, w) => a + w, 0);
  return { perDay: weights.map((w) => Math.round((weekly * w) / total)), splitEvenly: false };
}

export interface SafetyCheck {
  unsafe: boolean;
  reasons: string[];
  /** A smaller starting amount (in pounds) that is within the limits, if the goal was unsafe. */
  saferAmountLb?: number;
}

/** Flags goals that would mean losing weight too fast or eating below the floor (S3-AC10). */
export function checkGoalSafety(b: Biometrics, g: Goal): SafetyCheck {
  if (g.direction === "bulk") return { unsafe: false, reasons: [] };
  const reasons: string[] = [];
  const lbPerWeek = g.amountLb / g.weeks;
  const dailyAverage = weeklyBudget(b, g) / 7;
  if (lbPerWeek > MAX_LOSS_LB_PER_WEEK) reasons.push(`That is ${lbPerWeek.toFixed(1)} lb a week; more than ${MAX_LOSS_LB_PER_WEEK} lb a week is too fast.`);
  if (dailyAverage < DAILY_FLOOR) reasons.push(`That works out to under ${DAILY_FLOOR} calories a day.`);
  if (reasons.length === 0) return { unsafe: false, reasons };

  // Largest weekly loss that respects both limits.
  const fromFloor = Math.max(0, ((maintenanceCalories(b) - DAILY_FLOOR) * 7) / CALORIES_PER_POUND);
  const safeLbPerWeek = Math.min(MAX_LOSS_LB_PER_WEEK, fromFloor);
  const saferAmountLb = Math.floor(safeLbPerWeek * g.weeks * 2) / 2; // round down to a half pound
  return { unsafe: true, reasons, saferAmountLb };
}

/** Validates the set-up form: returns the names of missing or invalid items (S3-AC2). */
export function missingBiometrics(input: Partial<Record<keyof Biometrics, unknown>>): string[] {
  const missing: string[] = [];
  if (input.sex !== "female" && input.sex !== "male") missing.push("sex");
  for (const key of ["age", "heightIn", "weightLb"] as const) {
    const v = input[key];
    if (typeof v !== "number" || !Number.isFinite(v) || v <= 0) missing.push(key);
  }
  if (input.intensity !== "light" && input.intensity !== "moderate" && input.intensity !== "high") missing.push("intensity");
  return missing;
}
