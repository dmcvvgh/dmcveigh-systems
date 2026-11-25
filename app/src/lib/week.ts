// The week behind the Today screen: budget, eaten, burned, and what is left (S3-AC6, AC8).
import { maintenanceCalories, splitWeek, weeklyBudget } from "./budget";
import { dayKey, dayTotals, type Meal } from "./meals";
import { weeksUntil, type Profile } from "./profile";

/** The seven days of the week containing `today`, Sunday first. */
export function weekDays(today: Date): Date[] {
  const start = new Date(today.getFullYear(), today.getMonth(), today.getDate() - today.getDay());
  return Array.from({ length: 7 }, (_, i) => new Date(start.getFullYear(), start.getMonth(), start.getDate() + i));
}

export interface WeekSummary {
  weeklyBudget: number;
  /** Calories planned for each day, Sunday first. Heavy days get more. */
  perDay: number[];
  splitEvenly: boolean;
  todayIndex: number;
  /** Calories eaten each day. null for days that have not happened yet. */
  eatenByDay: (number | null)[];
  /** Estimated calories burned each day: maintenance plus logged workouts. null for future days. */
  burnedByDay: (number | null)[];
  eatenToday: number;
  burnedToday: number;
  todayBudget: number;
  eatenWeek: number;
  /** Weekly budget minus eaten so far this week. Negative means over budget. */
  leftWeek: number;
}

/**
 * @param extraBurned calories from logged workouts, keyed by yyyy-mm-dd (empty until workouts exist)
 */
export function summarizeWeek(
  profile: Profile,
  meals: Meal[],
  extraBurned: Record<string, number>,
  today: Date,
): WeekSummary {
  const weeks = Math.max(weeksUntil(profile.goal.targetDate, today), 1);
  const budget = weeklyBudget(profile.biometrics, { ...profile.goal, weeks });
  const plan = splitWeek(budget, profile.heavyDays);
  const maintenance = maintenanceCalories(profile.biometrics);
  const days = weekDays(today);
  const todayIndex = today.getDay();

  const eatenByDay = days.map((d, i) => (i <= todayIndex ? dayTotals(meals, d).calories : null));
  const burnedByDay = days.map((d, i) => (i <= todayIndex ? maintenance + (extraBurned[dayKey(d)] ?? 0) : null));
  const eatenWeek = eatenByDay.reduce<number>((sum, v) => sum + (v ?? 0), 0);

  return {
    weeklyBudget: budget,
    perDay: plan.perDay,
    splitEvenly: plan.splitEvenly,
    todayIndex,
    eatenByDay,
    burnedByDay,
    eatenToday: eatenByDay[todayIndex] ?? 0,
    burnedToday: burnedByDay[todayIndex] ?? 0,
    todayBudget: plan.perDay[todayIndex],
    eatenWeek,
    leftWeek: budget - eatenWeek,
  };
}
