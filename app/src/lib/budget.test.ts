import { describe, expect, it } from "vitest";
import {
  checkGoalSafety,
  maintenanceCalories,
  missingBiometrics,
  splitWeek,
  weeklyBudget,
  type Biometrics,
} from "./budget";

const person: Biometrics = { sex: "male", age: 21, heightIn: 70, weightLb: 175, intensity: "moderate" };
const smaller: Biometrics = { sex: "female", age: 21, heightIn: 62, weightLb: 125, intensity: "moderate" };

describe("S3-AC7: weekly budget depends on biometrics and intensity", () => {
  it("gives a smaller, lighter person a lower budget than a larger, heavier one", () => {
    expect(maintenanceCalories(smaller)).toBeLessThan(maintenanceCalories(person));
  });
  it("gives a higher budget for higher training intensity", () => {
    const light = maintenanceCalories({ ...person, intensity: "light" });
    const high = maintenanceCalories({ ...person, intensity: "high" });
    expect(high).toBeGreaterThan(light);
  });
  it("is lower than maintenance for a cut and higher for a bulk", () => {
    const base = maintenanceCalories(person) * 7;
    expect(weeklyBudget(person, { direction: "cut", amountLb: 5, weeks: 10 })).toBeLessThan(base);
    expect(weeklyBudget(person, { direction: "bulk", amountLb: 5, weeks: 10 })).toBeGreaterThan(base);
  });
  it("uses about 3,500 calories per pound", () => {
    const base = maintenanceCalories(person) * 7;
    const cut = weeklyBudget(person, { direction: "cut", amountLb: 10, weeks: 10 }); // 1 lb a week
    expect(base - cut).toBe(3500);
  });
});

describe("S3-AC8: heavy days get more than rest days", () => {
  it("adds up to the weekly budget (within rounding)", () => {
    const { perDay } = splitWeek(14000, [1, 3, 5]);
    expect(Math.abs(perDay.reduce((a, b) => a + b, 0) - 14000)).toBeLessThanOrEqual(3);
  });
  it("gives each heavy day more than each rest day", () => {
    const { perDay } = splitWeek(14000, [1, 3, 5]);
    expect(perDay[1]).toBeGreaterThan(perDay[0]);
    expect(perDay[3]).toBeGreaterThan(perDay[2]);
  });
});

describe("S3-AC9: no heavy days picked", () => {
  it("splits the budget evenly and says so", () => {
    const plan = splitWeek(14000, []);
    expect(plan.splitEvenly).toBe(true);
    expect(new Set(plan.perDay).size).toBe(1);
  });
});

describe("S3-AC10: unsafe goals", () => {
  it("flags losing more than 2 lb a week and suggests a smaller goal", () => {
    const result = checkGoalSafety(person, { direction: "cut", amountLb: 10, weeks: 2 }); // 5 lb a week
    expect(result.unsafe).toBe(true);
    expect(result.saferAmountLb).toBeLessThan(10);
    expect(result.saferAmountLb).toBeLessThanOrEqual(4); // 2 lb a week for 2 weeks
  });
  it("flags a daily budget under 1,200 calories", () => {
    const result = checkGoalSafety(smaller, { direction: "cut", amountLb: 8, weeks: 4 });
    expect(result.unsafe).toBe(true);
    expect(result.reasons.join(" ")).toMatch(/1200/);
  });
  it("accepts a gentle cut", () => {
    expect(checkGoalSafety(person, { direction: "cut", amountLb: 5, weeks: 10 }).unsafe).toBe(false);
  });
  it("does not flag a bulk", () => {
    expect(checkGoalSafety(person, { direction: "bulk", amountLb: 10, weeks: 2 }).unsafe).toBe(false);
  });
});

describe("S3-AC2: missing biometrics", () => {
  it("names each missing item", () => {
    expect(missingBiometrics({ age: 21 })).toEqual(["sex", "heightIn", "weightLb", "intensity"]);
  });
  it("accepts a complete set", () => {
    expect(missingBiometrics(person)).toEqual([]);
  });
  it("rejects zero or negative numbers", () => {
    expect(missingBiometrics({ ...person, age: 0 })).toEqual(["age"]);
  });
});
