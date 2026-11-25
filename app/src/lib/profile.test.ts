import { describe, expect, it } from "vitest";
import { parseProfile, validateGoal, weeksUntil } from "./profile";

const today = new Date(2026, 10, 25); // Nov 25, 2026

describe("weeksUntil", () => {
  it("counts weeks to a later date", () => {
    expect(weeksUntil("2026-12-09", today)).toBe(2);
  });
});

describe("S3-AC3: goal needs a direction, an amount, and a date", () => {
  it("accepts a good goal", () => {
    expect(validateGoal({ direction: "cut", amountLb: 10, targetDate: "2027-02-01" }, today)).toBeNull();
  });
  it("asks for cut or bulk", () => {
    expect(validateGoal({ amountLb: 10, targetDate: "2027-02-01" }, today)).toMatch(/cut or bulk/);
  });
  it("asks for an amount that is a number", () => {
    expect(validateGoal({ direction: "cut", targetDate: "2027-02-01" }, today)).toMatch(/pounds/);
    expect(validateGoal({ direction: "cut", amountLb: 0, targetDate: "2027-02-01" }, today)).toMatch(/pounds/);
  });
  it("rejects a date that is not at least a week away", () => {
    expect(validateGoal({ direction: "cut", amountLb: 5, targetDate: "2026-11-27" }, today)).toMatch(/week/);
    expect(validateGoal({ direction: "cut", amountLb: 5, targetDate: "2026-01-01" }, today)).toMatch(/week/);
  });
});

describe("parseProfile", () => {
  it("returns null for empty or damaged text", () => {
    expect(parseProfile(null)).toBeNull();
    expect(parseProfile("not json")).toBeNull();
    expect(parseProfile("{}")).toBeNull();
  });
  it("reads a saved profile back", () => {
    const profile = {
      biometrics: { sex: "male", age: 21, heightIn: 70, weightLb: 175, intensity: "moderate" },
      goal: { direction: "cut", amountLb: 8, targetDate: "2027-02-01" },
      heavyDays: [1, 3, 5],
    };
    expect(parseProfile(JSON.stringify(profile))).toEqual(profile);
  });
});
