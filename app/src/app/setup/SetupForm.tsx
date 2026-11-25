"use client";
// Set-up: biometrics, then goal and heavy lifting days. Covers S3-AC1, AC2, AC3, AC8, AC10.
import { useRouter } from "next/navigation";
import { useState } from "react";
import {
  checkGoalSafety,
  missingBiometrics,
  type Biometrics,
  type Direction,
} from "@/lib/budget";
import { validateGoal, weeksUntil, type Profile } from "@/lib/profile";
import { saveProfile, useProfile } from "@/lib/useProfile";

const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const LABELS: Record<string, string> = {
  sex: "Sex",
  age: "Age",
  heightIn: "Height",
  weightLb: "Weight",
  intensity: "Training intensity",
};
const input = "mt-1 w-full rounded-lg border border-gray-300 px-3 py-3 text-base";
const primary = "min-h-12 rounded-xl bg-green-700 px-4 font-semibold text-white";
const secondary = "min-h-12 rounded-xl bg-gray-200 px-4 font-semibold text-gray-900";

type Step = "biometrics" | "confirm" | "goal";

export default function SetupForm() {
  const { loaded, profile } = useProfile();
  if (!loaded) return <p className="p-4 text-sm text-gray-600">Loading...</p>;
  // `key` re-creates the form with the saved values the first time they are known.
  return <Form key={profile ? "saved" : "new"} saved={profile} />;
}

function num(v: string): number | undefined {
  const n = Number(v);
  return v.trim() === "" || !Number.isFinite(n) ? undefined : n;
}

function Form({ saved }: { saved: Profile | null }) {
  const router = useRouter();
  const b = saved?.biometrics;
  const [step, setStep] = useState<Step>("biometrics");
  const [sex, setSex] = useState<string>(b?.sex ?? "");
  const [age, setAge] = useState(b ? String(b.age) : "");
  const [heightIn, setHeightIn] = useState(b ? String(b.heightIn) : "");
  const [weightLb, setWeightLb] = useState(b ? String(b.weightLb) : "");
  const [intensity, setIntensity] = useState<string>(b?.intensity ?? "");
  const [direction, setDirection] = useState<string>(saved?.goal.direction ?? "");
  const [amount, setAmount] = useState(saved ? String(saved.goal.amountLb) : "");
  const [date, setDate] = useState(saved?.goal.targetDate ?? "");
  const [heavy, setHeavy] = useState<number[]>(saved?.heavyDays ?? []);
  const [missing, setMissing] = useState<string[]>([]);
  const [goalError, setGoalError] = useState<string | null>(null);
  const [unsafe, setUnsafe] = useState<{ reasons: string[]; saferAmountLb: number } | null>(null);
  const [saveError, setSaveError] = useState(false);

  const entered = { sex, age: num(age), heightIn: num(heightIn), weightLb: num(weightLb), intensity };

  function review() {
    const m = missingBiometrics(entered);
    setMissing(m);
    if (m.length === 0) setStep("confirm");
  }

  function save(amountLb: number) {
    const profile: Profile = {
      biometrics: entered as Biometrics,
      goal: { direction: direction as Direction, amountLb, targetDate: date },
      heavyDays: [...heavy].sort(),
    };
    if (saveProfile(profile)) router.push("/");
    else setSaveError(true);
  }

  function submitGoal() {
    const today = new Date();
    const error = validateGoal({ direction, amountLb: num(amount), targetDate: date }, today);
    setGoalError(error);
    if (error) return;
    const safety = checkGoalSafety(entered as Biometrics, {
      direction: direction as Direction,
      amountLb: num(amount)!,
      weeks: weeksUntil(date, today),
    });
    if (safety.unsafe) setUnsafe({ reasons: safety.reasons, saferAmountLb: safety.saferAmountLb ?? 0 });
    else save(num(amount)!);
  }

  const toggleDay = (d: number) => setHeavy((h) => (h.includes(d) ? h.filter((x) => x !== d) : [...h, d]));

  return (
    <div className="mx-auto max-w-sm p-4">
      <h1 className="text-xl font-semibold">{saved ? "Update your plan" : "Set up your plan"}</h1>

      {step === "biometrics" && (
        <section className="mt-4 space-y-4" aria-label="About you">
          <p className="text-sm text-gray-600">
            Step 1 of 2. These numbers set your calorie budget. They stay on this device.
          </p>
          {missing.length > 0 && (
            <div role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-800">
              Please fill in: {missing.map((k) => LABELS[k] ?? k).join(", ")}.
            </div>
          )}
          <label className="block text-sm font-medium">
            Sex
            <select className={input} value={sex} onChange={(e) => setSex(e.target.value)}>
              <option value="">Choose...</option>
              <option value="female">Female</option>
              <option value="male">Male</option>
            </select>
          </label>
          <label className="block text-sm font-medium">
            Age
            <input className={input} inputMode="numeric" value={age} onChange={(e) => setAge(e.target.value)} />
          </label>
          <label className="block text-sm font-medium">
            Height (inches, for example 5&apos;10&quot; is 70)
            <input className={input} inputMode="decimal" value={heightIn} onChange={(e) => setHeightIn(e.target.value)} />
          </label>
          <label className="block text-sm font-medium">
            Weight (pounds)
            <input className={input} inputMode="decimal" value={weightLb} onChange={(e) => setWeightLb(e.target.value)} />
          </label>
          <label className="block text-sm font-medium">
            How intense do you want to train?
            <select className={input} value={intensity} onChange={(e) => setIntensity(e.target.value)}>
              <option value="">Choose...</option>
              <option value="light">Light</option>
              <option value="moderate">Moderate</option>
              <option value="high">High</option>
            </select>
          </label>
          <button className={`${primary} w-full`} onClick={review}>
            Review
          </button>
        </section>
      )}

      {step === "confirm" && (
        <section className="mt-4 space-y-4" aria-label="Confirm">
          <p className="text-sm text-gray-600">Check these before you set a goal. Wrong numbers give a wrong budget.</p>
          <dl className="grid grid-cols-2 gap-2 rounded-lg bg-gray-50 p-3 text-sm">
            <dt>Sex</dt><dd className="font-medium capitalize">{sex}</dd>
            <dt>Age</dt><dd className="font-medium">{age}</dd>
            <dt>Height</dt><dd className="font-medium">{heightIn} in</dd>
            <dt>Weight</dt><dd className="font-medium">{weightLb} lb</dd>
            <dt>Intensity</dt><dd className="font-medium capitalize">{intensity}</dd>
          </dl>
          <div className="flex gap-2">
            <button className={`${secondary} flex-1`} onClick={() => setStep("biometrics")}>Edit</button>
            <button className={`${primary} flex-1`} onClick={() => setStep("goal")}>Looks right</button>
          </div>
        </section>
      )}

      {step === "goal" && (
        <section className="mt-4 space-y-4" aria-label="Goal">
          <p className="text-sm text-gray-600">Step 2 of 2. Your goal and your heavy lifting days.</p>
          {goalError && (
            <div role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-800">{goalError}</div>
          )}
          <label className="block text-sm font-medium">
            Goal
            <select className={input} value={direction} onChange={(e) => setDirection(e.target.value)}>
              <option value="">Choose...</option>
              <option value="cut">Cut weight</option>
              <option value="bulk">Bulk weight</option>
            </select>
          </label>
          <label className="block text-sm font-medium">
            How many pounds?
            <input className={input} inputMode="decimal" value={amount} onChange={(e) => setAmount(e.target.value)} />
          </label>
          <label className="block text-sm font-medium">
            By when?
            <input className={input} type="date" value={date} onChange={(e) => setDate(e.target.value)} />
          </label>
          <fieldset>
            <legend className="text-sm font-medium">Heavy lifting days</legend>
            <div className="mt-1 grid grid-cols-7 gap-1">
              {DAYS.map((name, d) => (
                <button
                  key={name}
                  type="button"
                  aria-pressed={heavy.includes(d)}
                  onClick={() => toggleDay(d)}
                  className={`min-h-11 rounded-lg border px-0 text-sm font-medium ${
                    heavy.includes(d) ? "border-green-700 bg-green-700 text-white" : "border-gray-300 bg-white"
                  }`}
                >
                  {name}
                </button>
              ))}
            </div>
            <p className="mt-1 text-xs text-gray-600">
              {heavy.length === 0
                ? "None picked: your calories will be split evenly across the week."
                : "These days get more calories, and the other days get fewer."}
            </p>
          </fieldset>
          {saveError && (
            <div role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-800">
              Could not save on this device. Check that your browser allows site storage.
            </div>
          )}
          <div className="flex gap-2">
            <button className={`${secondary} flex-1`} onClick={() => setStep("biometrics")}>Back</button>
            <button className={`${primary} flex-1`} onClick={submitGoal}>Save plan</button>
          </div>
        </section>
      )}

      {unsafe && (
        <div role="dialog" aria-modal="true" aria-label="Start with a smaller goal" className="fixed inset-0 grid place-items-center bg-black/40 p-4">
          <div className="max-w-sm rounded-2xl bg-white p-4 shadow-xl">
            <h2 className="text-lg font-semibold">Let&apos;s start smaller</h2>
            <ul className="mt-2 list-disc pl-5 text-sm text-gray-700">
              {unsafe.reasons.map((r) => <li key={r}>{r}</li>)}
            </ul>
            {unsafe.saferAmountLb > 0 ? (
              <p className="mt-2 text-sm text-gray-700">
                A safer first goal for that date is {unsafe.saferAmountLb} lb. You can work up to a bigger goal later.
              </p>
            ) : (
              <p className="mt-2 text-sm text-gray-700">Try a later date or a smaller amount.</p>
            )}
            <div className="mt-4 flex gap-2">
              <button className={`${secondary} flex-1`} onClick={() => setUnsafe(null)}>Change my goal</button>
              {unsafe.saferAmountLb > 0 && (
                <button className={`${primary} flex-1`} onClick={() => save(unsafe.saferAmountLb)}>
                  Use {unsafe.saferAmountLb} lb
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
