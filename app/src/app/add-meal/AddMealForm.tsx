"use client";
// Add a meal by hand: S1-AC4 (time and totals), AC8 (Cancel), AC9 (by hand, any time), AC10 (error).
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, useSyncExternalStore } from "react";
import { validateMeal } from "@/lib/meals";
import { addMeal } from "@/lib/useMeals";

const field = "mt-1 w-full rounded-lg border border-gray-300 px-3 py-3 text-base";

/** Now, as text for a date-and-time box, in the user's own time zone. */
function nowForInput(): string {
  const d = new Date();
  d.setMinutes(d.getMinutes() - d.getTimezoneOffset());
  return d.toISOString().slice(0, 16);
}

export default function AddMealForm() {
  const router = useRouter();
  // "Now" is read only in the browser (empty while the page is built on the server).
  const defaultTime = useSyncExternalStore(() => () => {}, nowForInput, () => "");
  const [form, setForm] = useState({ name: "", calories: "", protein: "", fats: "", carbs: "" });
  const [eatenAt, setEatenAt] = useState<string | null>(null); // null = still the default (now)
  const timeValue = eatenAt ?? defaultTime;
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [saveError, setSaveError] = useState(false);

  const set = (key: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((f) => ({ ...f, [key]: e.target.value }));

  function save(e: React.FormEvent) {
    e.preventDefault();
    const result = validateMeal({ ...form, eatenAt: timeValue });
    if (!result.ok) {
      setErrors(result.errors);
      return;
    }
    setErrors({});
    if (addMeal({ ...result.meal, source: "hand" })) router.push("/");
    else setSaveError(true);
  }

  return (
    <form onSubmit={save} noValidate className="mx-auto max-w-sm space-y-4 p-4">
      <h1 className="text-xl font-semibold">Add a meal by hand</h1>
      <label className="block text-sm font-medium">
        What did you eat?
        <input className={field} value={form.name} onChange={set("name")} placeholder="Chicken rice bowl" />
      </label>
      <label className="block text-sm font-medium">
        Calories
        <input className={field} inputMode="decimal" value={form.calories} onChange={set("calories")} aria-invalid={!!errors.calories} />
        {errors.calories && <span role="alert" className="mt-1 block text-sm text-red-700">{errors.calories}</span>}
      </label>
      <div className="grid grid-cols-3 gap-2">
        {(["protein", "fats", "carbs"] as const).map((k) => (
          <label key={k} className="block text-sm font-medium capitalize">
            {k} (g)
            <input className={field} inputMode="decimal" value={form[k]} onChange={set(k)} aria-invalid={!!errors[k]} />
            {errors[k] && <span role="alert" className="mt-1 block text-xs text-red-700">{errors[k]}</span>}
          </label>
        ))}
      </div>
      <label className="block text-sm font-medium">
        When did you eat it?
        <input className={field} type="datetime-local" value={timeValue} onChange={(e) => setEatenAt(e.target.value)} />
        {errors.eatenAt && <span role="alert" className="mt-1 block text-sm text-red-700">{errors.eatenAt}</span>}
      </label>
      {saveError && (
        <p role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-800">
          Could not save on this device. Check that your browser allows site storage.
        </p>
      )}
      <div className="flex gap-2">
        <Link href="/" className="inline-flex min-h-12 flex-1 items-center justify-center rounded-xl bg-gray-200 font-semibold">
          Cancel
        </Link>
        <button type="submit" className="min-h-12 flex-1 rounded-xl bg-green-700 font-semibold text-white">
          Save meal
        </button>
      </div>
    </form>
  );
}
