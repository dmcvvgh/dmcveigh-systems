"use client";
// Today (home) screen, after Mockup C: where you are today and this week. S1-AC5, S3-AC6, S3-AC8.
import Link from "next/link";
import WeekChart from "@/components/WeekChart";
import { dayKey, mealsOn } from "@/lib/meals";
import { summarizeWeek } from "@/lib/week";
import { useMeals } from "@/lib/useMeals";
import { useProfile } from "@/lib/useProfile";
import { useWorkouts } from "@/lib/useWorkouts";
import { burnedByDate } from "@/lib/workouts";

const DAY_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
const button = "inline-flex min-h-12 flex-1 items-center justify-center rounded-full px-4 text-base font-semibold";

function fmt(n: number) {
  return Math.round(n).toLocaleString("en-US");
}

export default function Today() {
  const { loaded, profile } = useProfile();
  const { meals } = useMeals();
  const { workouts } = useWorkouts();
  if (!loaded) return <p className="p-4 text-sm text-gray-600">Loading...</p>;

  if (!profile) {
    return (
      <main className="mx-auto max-w-sm p-4">
        <h1 className="text-xl font-semibold">Fitness and Calorie Tracker</h1>
        <p className="mt-2 text-sm text-gray-600">Set your goal to get a weekly calorie budget.</p>
        <Link href="/setup" className={`${button} mt-4 bg-green-700 text-white`}>Set up my plan</Link>
      </main>
    );
  }

  const today = new Date();
  const week = summarizeWeek(profile, meals, burnedByDate(workouts), today);
  const todaysWorkouts = workouts.filter((w) => w.date === dayKey(today));
  const todays = mealsOn(meals, today);
  const goal = profile.goal;
  const over = week.leftWeek < 0;
  const isHeavy = profile.heavyDays.includes(week.todayIndex);

  return (
    <main className="mx-auto max-w-sm p-4 pb-8">
      <h1 className="text-lg font-bold">
        Your {goal.direction}: {goal.amountLb} lb by {goal.targetDate}
      </h1>
      <p className="text-sm text-gray-600">
        {DAY_NAMES[week.todayIndex]}: about {fmt(week.todayBudget)} calories
        {week.splitEvenly ? " (split evenly)" : isHeavy ? " (heavy lifting day)" : " (rest day)"}
      </p>

      <div className="mt-3 grid grid-cols-3 gap-2 text-center">
        <div className="rounded-xl bg-green-50 p-2">
          <b className="block text-xl">{fmt(week.eatenToday)}</b>
          <span className="text-xs text-gray-600">eaten today</span>
        </div>
        <div className="rounded-xl bg-green-50 p-2">
          <b className="block text-xl">{fmt(week.burnedToday)}</b>
          <span className="text-xs text-gray-600">burned today</span>
        </div>
        <div className={`rounded-xl p-2 ${over ? "bg-red-50" : "bg-emerald-100"}`}>
          <b className="block text-xl">{fmt(Math.abs(week.leftWeek))}</b>
          <span className="text-xs text-gray-600">{over ? "over this week" : "left this week"}</span>
        </div>
      </div>

      <WeekChart eaten={week.eatenByDay} burned={week.burnedByDay} todayIndex={week.todayIndex} />

      <h2 className="mt-4 text-base font-semibold">Today</h2>
      {todays.length === 0 ? (
        <div className="mt-1 rounded-xl bg-gray-50 p-4 text-sm text-gray-700">
          <p className="font-medium">No meals logged yet today.</p>
          <p className="mt-1">Upload a photo of your first meal, or add it by hand.</p>
        </div>
      ) : (
        <ol className="mt-1 border-l-2 border-green-200 pl-3">
          {todays.map((m) => (
            <li key={m.id} className="mb-2 text-sm">
              {new Date(m.eatenAt).toLocaleTimeString([], { hour: "numeric", minute: "2-digit" })} &middot; {m.name}
              <small className="block text-gray-600">
                {fmt(m.calories)} kcal{m.source === "hand" ? " (by hand)" : ""}
              </small>
            </li>
          ))}
        </ol>
      )}

      {todaysWorkouts.length > 0 && (
        <>
          <h2 className="mt-4 text-base font-semibold">Workouts today</h2>
          <ul className="mt-1 border-l-2 border-orange-200 pl-3">
            {todaysWorkouts.map((w) => (
              <li key={w.id} className="mb-2 text-sm">
                {w.exercise}{w.weightLb > 0 ? `, ${fmt(w.weightLb)} lb` : ""}
                <small className="block text-gray-600">about {fmt(w.caloriesBurned)} kcal burned</small>
              </li>
            ))}
          </ul>
        </>
      )}

      <div className="mt-4 flex gap-2">
        <Link href="/add-meal" className={`${button} bg-green-100 text-gray-900`}>By hand</Link>
        <Link href="/add-photo" className={`${button} bg-green-700 text-white`}>+ Photo</Link>
      </div>
      <Link href="/log-workout" className={`${button} mt-2 w-full bg-orange-100 text-gray-900`}>Log a workout</Link>
      <p className="mt-4 text-center text-sm">
        <Link href="/setup" className="text-green-800 underline">Change my goal</Link> &middot; <Link href="/progress-photos" className="text-green-800 underline">Progress photos</Link>
      </p>
    </main>
  );
}
