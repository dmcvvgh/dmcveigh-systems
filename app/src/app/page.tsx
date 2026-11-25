"use client";
// Temporary home page for Task 2: shows the saved plan. Task 4 replaces it with the Today screen.
import Link from "next/link";
import { maintenanceCalories, splitWeek, weeklyBudget } from "@/lib/budget";
import { dayTotals, mealsOn } from "@/lib/meals";
import { weeksUntil } from "@/lib/profile";
import { useMeals } from "@/lib/useMeals";
import { useProfile } from "@/lib/useProfile";

const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

export default function Home() {
  const { loaded, profile } = useProfile();
  const { meals } = useMeals();
  if (!loaded) return <p className="p-4 text-sm text-gray-600">Loading...</p>;

  if (!profile) {
    return (
      <main className="mx-auto max-w-sm p-4">
        <h1 className="text-xl font-semibold">Fitness and Calorie Tracker</h1>
        <p className="mt-2 text-sm text-gray-600">Set your goal to get a weekly calorie budget.</p>
        <Link href="/setup" className="mt-4 inline-flex min-h-12 items-center rounded-xl bg-green-700 px-4 font-semibold text-white">
          Set up my plan
        </Link>
      </main>
    );
  }

  const weeks = weeksUntil(profile.goal.targetDate, new Date());
  const budget = weeklyBudget(profile.biometrics, { ...profile.goal, weeks: Math.max(weeks, 1) });
  const plan = splitWeek(budget, profile.heavyDays);
  const today = new Date();
  const todays = mealsOn(meals, today);
  const totals = dayTotals(meals, today);

  return (
    <main className="mx-auto max-w-sm p-4">
      <h1 className="text-xl font-semibold">Your plan</h1>
      <p className="text-sm text-gray-600">
        {profile.goal.direction === "cut" ? "Cut" : "Bulk"} {profile.goal.amountLb} lb by {profile.goal.targetDate}
      </p>
      <p className="mt-3 text-2xl font-bold">{budget.toLocaleString()} <span className="text-sm font-normal text-gray-600">calories a week</span></p>
      <p className="text-xs text-gray-600">About {maintenanceCalories(profile.biometrics).toLocaleString()} a day to stay the same weight.</p>
      {plan.splitEvenly && (
        <p className="mt-2 rounded-lg bg-yellow-50 p-2 text-xs text-yellow-900">No heavy lifting days picked, so calories are split evenly.</p>
      )}
      <ul className="mt-3 divide-y rounded-lg border">
        {plan.perDay.map((cal, d) => (
          <li key={d} className="flex justify-between px-3 py-2 text-sm">
            <span>{DAYS[d]} {profile.heavyDays.includes(d) && <span className="text-xs text-green-700">heavy</span>}</span>
            <span className="font-medium">{cal.toLocaleString()}</span>
          </li>
        ))}
      </ul>
      <h2 className="mt-6 text-lg font-semibold">Today&apos;s meals</h2>
      {todays.length === 0 ? (
        <p className="text-sm text-gray-600">Nothing logged yet today.</p>
      ) : (
        <>
          <p className="text-sm text-gray-700">
            {totals.calories.toLocaleString()} cal &middot; protein {totals.protein} g &middot; fats {totals.fats} g &middot; carbs {totals.carbs} g
          </p>
          <ul className="mt-2 divide-y rounded-lg border">
            {todays.map((m) => (
              <li key={m.id} className="flex justify-between px-3 py-2 text-sm">
                <span>
                  {new Date(m.eatenAt).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })} &middot; {m.name}
                </span>
                <span className="font-medium">{m.calories.toLocaleString()}</span>
              </li>
            ))}
          </ul>
        </>
      )}
      <div className="mt-4 flex gap-2">
        <Link href="/add-meal" className="inline-flex min-h-12 flex-1 items-center justify-center rounded-xl bg-green-700 px-4 font-semibold text-white">
          Add meal by hand
        </Link>
        <Link href="/setup" className="inline-flex min-h-12 flex-1 items-center justify-center rounded-xl bg-gray-200 px-4 font-semibold">
          Change my goal
        </Link>
      </div>
    </main>
  );
}
