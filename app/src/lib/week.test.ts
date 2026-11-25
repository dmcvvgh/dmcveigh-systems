import { describe, expect, it } from "vitest";
import { maintenanceCalories } from "./budget";
import type { Meal } from "./meals";
import type { Profile } from "./profile";
import { summarizeWeek, weekDays } from "./week";

const profile: Profile = {
  biometrics: { sex: "male", age: 21, heightIn: 70, weightLb: 175, intensity: "moderate" },
  goal: { direction: "cut", amountLb: 6, targetDate: "2027-02-03" },
  heavyDays: [1, 3, 5],
};
const wed = new Date(2026, 10, 25, 14, 0); // Wednesday Nov 25, 2026
const meal = (id: string, when: string, calories: number): Meal => ({
  id, name: id, calories, protein: 0, fats: 0, carbs: 0, eatenAt: new Date(when).toISOString(), source: "hand",
});

describe("weekDays", () => {
  it("runs Sunday to Saturday around today", () => {
    const days = weekDays(wed);
    expect(days).toHaveLength(7);
    expect(days[0].getDay()).toBe(0);
    expect(days[3].getDate()).toBe(25);
    expect(days[6].getDay()).toBe(6);
  });
});

describe("summarizeWeek (S3-AC6, AC8)", () => {
  const meals = [
    meal("mon", "2026-11-23T12:00", 2000),
    meal("tue", "2026-11-24T12:00", 1800),
    meal("wed-a", "2026-11-25T08:00", 320),
    meal("wed-b", "2026-11-25T12:40", 610),
    meal("last week", "2026-11-20T12:00", 5000),
  ];
  const s = summarizeWeek(profile, meals, { "2026-11-25": 380 }, wed);

  it("counts only this week's meals", () => {
    expect(s.eatenWeek).toBe(2000 + 1800 + 930);
  });
  it("shows what is left this week", () => {
    expect(s.leftWeek).toBe(s.weeklyBudget - s.eatenWeek);
  });
  it("totals today's meals", () => {
    expect(s.eatenToday).toBe(930);
  });
  it("uses maintenance as burned, plus logged workouts", () => {
    const m = maintenanceCalories(profile.biometrics);
    expect(s.burnedToday).toBe(m + 380);
    expect(s.burnedByDay[1]).toBe(m);
  });
  it("leaves future days empty for the chart", () => {
    expect(s.eatenByDay.slice(4)).toEqual([null, null, null]);
    expect(s.burnedByDay.slice(4)).toEqual([null, null, null]);
  });
  it("gives heavy days a bigger budget (Wednesday is heavy)", () => {
    expect(s.todayIndex).toBe(3);
    expect(s.todayBudget).toBeGreaterThan(s.perDay[2]);
  });
  it("goes negative when over budget", () => {
    const over = summarizeWeek(profile, [meal("big", "2026-11-25T12:00", 99999)], {}, wed);
    expect(over.leftWeek).toBeLessThan(0);
  });
});
