"use client";
// Temporary home page for Task 2: shows the saved plan. Task 4 replaces it with the Today screen.
import Link from "next/link";
import { maintenanceCalories, splitWeek, weeklyBudget } from "@/lib/budget";
import { weeksUntil } from "@/lib/profile";
import { useProfile } from "@/lib/useProfile";

const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

export default function Home() {
  const { loaded, profile } = useProfile();
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
      <Link href="/setup" className="mt-4 inline-flex min-h-12 items-center rounded-xl bg-gray-200 px-4 font-semibold">
        Change my goal
      </Link>
    </main>
  );
}
