import { describe, expect, it } from "vitest";
import { BURNED_ERROR, burnedByDate, EXERCISE_ERROR, parseWorkouts, validateWorkout, type Workout } from "./workouts";

const base = { exercise: "Bench press", weightLb: "135", caloriesBurned: "250", date: "2026-11-25" };

describe("S2-AC1: log a workout (exercise and weight lifted)", () => {
  it("saves the exercise, weight, calories and day", () => {
    const r = validateWorkout(base);
    expect(r).toEqual({ ok: true, workout: { date: "2026-11-25", exercise: "Bench press", weightLb: 135, caloriesBurned: 250 } });
  });
  it("asks for the exercise", () => {
    expect(validateWorkout({ ...base, exercise: "  " })).toEqual({ ok: false, errors: { exercise: EXERCISE_ERROR } });
  });
  it("counts empty weight and calories as 0 (for example a run)", () => {
    const r = validateWorkout({ ...base, weightLb: "", caloriesBurned: "" });
    expect(r.ok && r.workout.weightLb + r.workout.caloriesBurned).toBe(0);
  });
  it("rejects calories or weight that are not numbers", () => {
    const r = validateWorkout({ ...base, caloriesBurned: "lots", weightLb: "-3" });
    expect(!r.ok && r.errors.caloriesBurned).toBe(BURNED_ERROR);
    expect(!r.ok && r.errors.weightLb).toBeTruthy();
  });
  it("rejects a missing day", () => {
    expect(validateWorkout({ ...base, date: "" }).ok).toBe(false);
  });
});

const w = (id: string, date: string, cal: number): Workout => ({ id, date, exercise: id, weightLb: 0, caloriesBurned: cal });

describe("burnedByDate", () => {
  it("adds up calories for each day", () => {
    expect(burnedByDate([w("a", "2026-11-25", 200), w("b", "2026-11-25", 180), w("c", "2026-11-24", 90)])).toEqual({
      "2026-11-25": 380,
      "2026-11-24": 90,
    });
  });
  it("is empty with no workouts", () => {
    expect(burnedByDate([])).toEqual({});
  });
});

describe("parseWorkouts", () => {
  it("handles missing or damaged text", () => {
    expect(parseWorkouts(null)).toEqual([]);
    expect(parseWorkouts("nope")).toEqual([]);
  });
  it("skips damaged entries", () => {
    const good = w("ok", "2026-11-25", 100);
    expect(parseWorkouts(JSON.stringify([good, { id: 1 }]))).toEqual([good]);
  });
});
