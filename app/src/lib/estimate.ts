// Turns a meal photo into foods, calories, and macros (S1-AC1).
// v1 uses a clearly labeled STAND-IN. Task 7 swaps in Gemini behind the same function.

export interface Food {
  name: string;
  calories: number;
  protein: number;
  fats: number;
  carbs: number;
}

export type EstimateResult =
  | { kind: "meal"; foods: Food[]; isSample: boolean } // the system found food
  | { kind: "not-food" } // S1-AC3
  | { kind: "error" }; // S1-AC7: could not read the photo

const SAMPLE_MEAL: Food[] = [
  { name: "Grilled chicken breast", calories: 280, protein: 52, fats: 6, carbs: 0 },
  { name: "White rice, 1 cup", calories: 205, protein: 4, fats: 0, carbs: 45 },
  { name: "Steamed broccoli", calories: 55, protein: 4, fats: 1, carbs: 11 },
];

/**
 * Stand-in estimate. It does NOT look at the picture. It always returns the same sample meal,
 * except for two test hooks so every path can be tried: a file name containing "notfood" is
 * treated as not food, and one containing "fail" is treated as a failed read.
 */
export function standInEstimate(fileName: string): EstimateResult {
  const name = fileName.toLowerCase();
  if (name.includes("notfood")) return { kind: "not-food" };
  if (name.includes("fail")) return { kind: "error" };
  return { kind: "meal", foods: SAMPLE_MEAL.map((f) => ({ ...f })), isSample: true };
}

/** The one function the screens call. Task 7 replaces its body with the real photo reader. */
export async function estimateMeal(file: File): Promise<EstimateResult> {
  await new Promise((resolve) => setTimeout(resolve, 600)); // so the "reading" state is visible
  return standInEstimate(file.name);
}

export interface FoodTotals {
  calories: number;
  protein: number;
  fats: number;
  carbs: number;
}

export function sumFoods(foods: Food[]): FoodTotals {
  return foods.reduce(
    (t, f) => ({
      calories: t.calories + f.calories,
      protein: t.protein + f.protein,
      fats: t.fats + f.fats,
      carbs: t.carbs + f.carbs,
    }),
    { calories: 0, protein: 0, fats: 0, carbs: 0 },
  );
}
