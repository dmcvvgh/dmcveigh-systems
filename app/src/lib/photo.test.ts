import { describe, expect, it } from "vitest";
import { checkPhotoFile, MAX_PHOTO_BYTES, PHOTO_ERROR } from "./photo";
import { standInEstimate, sumFoods } from "./estimate";
import { newestFirst, parseProgressPhotos } from "./progressPhotos";

describe("S1-AC6: invalid or oversized file", () => {
  it("accepts JPG and PNG under 10 MB", () => {
    expect(checkPhotoFile({ type: "image/jpeg", size: 1000 })).toBeNull();
    expect(checkPhotoFile({ type: "image/png", size: MAX_PHOTO_BYTES })).toBeNull();
  });
  it("rejects other file types with the spec's message", () => {
    expect(checkPhotoFile({ type: "application/pdf", size: 1000 })).toBe(PHOTO_ERROR);
    expect(checkPhotoFile({ type: "image/gif", size: 1000 })).toBe(PHOTO_ERROR);
    expect(PHOTO_ERROR).toBe("Use a JPG or PNG under 10 MB");
  });
  it("rejects a file over 10 MB", () => {
    expect(checkPhotoFile({ type: "image/jpeg", size: MAX_PHOTO_BYTES + 1 })).toBe(PHOTO_ERROR);
  });
});

describe("stand-in estimate (S1-AC1, AC3, AC7)", () => {
  it("treats a normal photo as a sample meal and says it is a sample", () => {
    const r = standInEstimate("lunch.jpg");
    expect(r.kind).toBe("meal");
    if (r.kind === "meal") {
      expect(r.isSample).toBe(true);
      expect(r.foods.length).toBeGreaterThan(0);
    }
  });
  it("treats notfood in the name as not food", () => {
    expect(standInEstimate("My-NotFood.png").kind).toBe("not-food");
  });
  it("treats fail in the name as a failed read", () => {
    expect(standInEstimate("fail.jpg").kind).toBe("error");
  });
  it("returns a fresh copy each time, so editing one result cannot change the next", () => {
    const a = standInEstimate("a.jpg");
    const b = standInEstimate("b.jpg");
    if (a.kind === "meal" && b.kind === "meal") {
      a.foods[0].calories = 1;
      expect(b.foods[0].calories).not.toBe(1);
    }
  });
});

describe("sumFoods", () => {
  it("adds calories and each macro", () => {
    expect(
      sumFoods([
        { name: "a", calories: 100, protein: 10, fats: 1, carbs: 5 },
        { name: "b", calories: 50, protein: 2, fats: 2, carbs: 8 },
      ]),
    ).toEqual({ calories: 150, protein: 12, fats: 3, carbs: 13 });
  });
});

describe("progress photos (Later-AC4, AC5)", () => {
  const p = (id: string, date: string) => ({ id, date, image: "data:image/jpeg;base64,AAAA" });
  it("reads saved photos and skips damaged entries", () => {
    expect(parseProgressPhotos(JSON.stringify([p("a", "2026-11-25"), { id: 1 }, { id: "x", date: "d", image: "http://evil" }]))).toEqual([
      p("a", "2026-11-25"),
    ]);
    expect(parseProgressPhotos(null)).toEqual([]);
    expect(parseProgressPhotos("junk")).toEqual([]);
  });
  it("lists the newest first", () => {
    expect(newestFirst([p("old", "2026-11-01"), p("new", "2026-11-25")]).map((x) => x.id)).toEqual(["new", "old"]);
  });
});
