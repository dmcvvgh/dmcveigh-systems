"use client";
// Log a workout by hand: S2-AC1. Calories burned are typed in (no health-app sync in v1).
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, useSyncExternalStore } from "react";
import { dayKey } from "@/lib/meals";
import { addWorkout } from "@/lib/useWorkouts";
import { validateWorkout } from "@/lib/workouts";

const field = "mt-1 w-full rounded-lg border border-gray-300 px-3 py-3 text-base";
const today = () => dayKey(new Date());

export default function WorkoutForm() {
  const router = useRouter();
  // "Today" is read only in the browser (empty while the page is built on the server).
  const defaultDay = useSyncExternalStore(() => () => {}, today, () => "");
  const [form, setForm] = useState({ exercise: "", weightLb: "", caloriesBurned: "" });
  const [date, setDate] = useState<string | null>(null); // null = still the default (today)
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [saveError, setSaveError] = useState(false);
  const dateValue = date ?? defaultDay;

  const set = (key: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((f) => ({ ...f, [key]: e.target.value }));

  function save(e: React.FormEvent) {
    e.preventDefault();
    const result = validateWorkout({ ...form, date: dateValue });
    if (!result.ok) {
      setErrors(result.errors);
      return;
    }
    setErrors({});
    if (addWorkout(result.workout)) router.push("/");
    else setSaveError(true);
  }

  return (
    <form onSubmit={save} noValidate className="mx-auto max-w-sm space-y-4 p-4">
      <h1 className="text-xl font-semibold">Log a workout</h1>
      <label className="block text-sm font-medium">
        Exercise
        <input className={field} value={form.exercise} onChange={set("exercise")} placeholder="Bench press" aria-invalid={!!errors.exercise} />
        {errors.exercise && <span role="alert" className="mt-1 block text-sm text-red-700">{errors.exercise}</span>}
      </label>
      <label className="block text-sm font-medium">
        Weight lifted (pounds, leave empty if none)
        <input className={field} inputMode="decimal" value={form.weightLb} onChange={set("weightLb")} aria-invalid={!!errors.weightLb} />
        {errors.weightLb && <span role="alert" className="mt-1 block text-sm text-red-700">{errors.weightLb}</span>}
      </label>
      <label className="block text-sm font-medium">
        Calories burned
        <input className={field} inputMode="decimal" value={form.caloriesBurned} onChange={set("caloriesBurned")} aria-invalid={!!errors.caloriesBurned} />
        {errors.caloriesBurned && <span role="alert" className="mt-1 block text-sm text-red-700">{errors.caloriesBurned}</span>}
      </label>
      <label className="block text-sm font-medium">
        Day
        <input className={field} type="date" value={dateValue} onChange={(e) => setDate(e.target.value)} />
        {errors.date && <span role="alert" className="mt-1 block text-sm text-red-700">{errors.date}</span>}
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
          Save workout
        </button>
      </div>
    </form>
  );
}
