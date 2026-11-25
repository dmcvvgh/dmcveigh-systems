import { describe, expect, it } from "vitest";
import { CALORIES_ERROR, dayTotals, mealsOn, parseMeals, validateMeal, type Meal } from "./meals";

const base = { name: "Chicken rice bowl", calories: "610", protein: "45", fats: "14", carbs: "70", eatenAt: "2026-11-25T12:40" };

describe("S1-AC10: calories must be a number", () => {
  it("rejects empty calories", () => {
    const r = validateMeal({ ...base, calories: "" });
    expect(r).toEqual({ ok: false, errors: { calories: CALORIES_ERROR } });
    expect(CALORIES_ERROR).toBe("Enter calories as a number, like 450");
  });
  it("rejects text and negative numbers", () => {
    expect(validateMeal({ ...base, calories: "lots" }).ok).toBe(false);
    expect(validateMeal({ ...base, calories: "-5" }).ok).toBe(false);
  });
  it("accepts a number", () => {
    const r = validateMeal(base);
    expect(r.ok).toBe(true);
    if (r.ok) expect(r.meal.calories).toBe(610);
  });
});

describe("S1-AC9: add by hand", () => {
  it("lets macros be left empty (counted as 0)", () => {
    const r = validateMeal({ ...base, protein: "", fats: "", carbs: "" });
    expect(r.ok && r.meal.protein + r.meal.fats + r.meal.carbs).toBe(0);
  });
  it("rejects a macro that is not a number", () => {
    const r = validateMeal({ ...base, protein: "abc" });
    expect(!r.ok && r.errors.protein).toBeTruthy();
  });
  it("uses 'Meal' when no name is given", () => {
    const r = validateMeal({ ...base, name: "  " });
    expect(r.ok && r.meal.name).toBe("Meal");
  });
  it("keeps the time eaten, so a meal can be logged later", () => {
    const r = validateMeal({ ...base, eatenAt: "2026-11-25T08:15" });
    expect(r.ok && new Date(r.meal.eatenAt).getHours()).toBe(8);
  });
  it("rejects a missing time", () => {
    expect(validateMeal({ ...base, eatenAt: "" }).ok).toBe(false);
  });
});

const meal = (id: string, eatenAt: string, calories: number, protein = 0): Meal => ({
  id, name: id, calories, protein, fats: 0, carbs: 0, eatenAt: new Date(eatenAt).toISOString(), source: "hand",
});
const day = new Date(2026, 10, 25, 20, 0);

describe("S1-AC4: daily totals", () => {
  const meals = [
    meal("lunch", "2026-11-25T12:40", 610, 45),
    meal("breakfast", "2026-11-25T08:15", 320, 20),
    meal("yesterday", "2026-11-24T19:00", 900, 60),
  ];
  it("adds calories and each macro for that day only", () => {
    expect(dayTotals(meals, day)).toEqual({ calories: 930, protein: 65, fats: 0, carbs: 0 });
  });
  it("lists the day's meals oldest first", () => {
    expect(mealsOn(meals, day).map((m) => m.id)).toEqual(["breakfast", "lunch"]);
  });
  it("is zero when nothing was eaten", () => {
    expect(dayTotals([], day).calories).toBe(0);
  });
});

describe("parseMeals", () => {
  it("returns an empty list for missing or damaged text", () => {
    expect(parseMeals(null)).toEqual([]);
    expect(parseMeals("oops")).toEqual([]);
    expect(parseMeals('{"a":1}')).toEqual([]);
  });
  it("skips damaged entries but keeps good ones", () => {
    const good = meal("ok", "2026-11-25T08:00", 100);
    expect(parseMeals(JSON.stringify([good, { id: 1 }]))).toEqual([good]);
  });
});
