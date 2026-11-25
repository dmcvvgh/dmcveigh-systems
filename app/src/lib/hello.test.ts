import { describe, expect, it } from "vitest";
import { appName } from "./hello";

describe("appName", () => {
  it("returns the app name", () => {
    expect(appName()).toBe("Fitness and Calorie Tracker");
  });
});
