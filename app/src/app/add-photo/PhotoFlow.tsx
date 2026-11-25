"use client";
// Add a meal from a photo. S1-AC1 (estimate), AC2 (confirm or edit), AC3 (not a meal), AC4 (save),
// AC6 (bad file), AC7 (could not read), AC8 (Cancel). The photo is NOT saved for meals.
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useRef, useState, useSyncExternalStore } from "react";
import { estimateMeal } from "@/lib/estimate";
import { downscaleToDataUrl } from "@/lib/image";
import { dayKey, nowForInput, validateMeal } from "@/lib/meals";
import { checkPhotoFile } from "@/lib/photo";
import { addMeal } from "@/lib/useMeals";
import { addProgressPhoto } from "@/lib/useProgressPhotos";

interface Row { name: string; calories: string; protein: string; fats: string; carbs: string }
type Stage =
  | { name: "choose" }
  | { name: "reading" }
  | { name: "review"; isSample: boolean }
  | { name: "not-food" }
  | { name: "failed" };

const field = "w-full rounded-lg border border-gray-300 px-2 py-2 text-base";
const primary = "inline-flex min-h-12 flex-1 items-center justify-center rounded-xl bg-green-700 px-4 font-semibold text-white";
const secondary = "inline-flex min-h-12 flex-1 items-center justify-center rounded-xl bg-gray-200 px-4 font-semibold text-gray-900";

export default function PhotoFlow() {
  const router = useRouter();
  const [stage, setStage] = useState<Stage>({ name: "choose" });
  const [fileError, setFileError] = useState<string | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [rows, setRows] = useState<Row[]>([]);
  const [rowErrors, setRowErrors] = useState<Record<number, string>>({});
  const [formError, setFormError] = useState<string | null>(null);
  const [eatenAt, setEatenAt] = useState<string | null>(null);
  const defaultTime = useSyncExternalStore(() => () => {}, nowForInput, () => "");
  const urlRef = useRef<string | null>(null);

  useEffect(() => () => { if (urlRef.current) URL.revokeObjectURL(urlRef.current); }, []);

  function reset() {
    setStage({ name: "choose" });
    setFile(null);
    setFileError(null);
    setFormError(null);
    setRowErrors({});
    if (urlRef.current) URL.revokeObjectURL(urlRef.current);
    urlRef.current = null;
    setPreview(null);
  }

  async function onChoose(e: React.ChangeEvent<HTMLInputElement>) {
    const chosen = e.target.files?.[0];
    e.target.value = "";
    if (!chosen) return;
    const problem = checkPhotoFile(chosen); // S1-AC6: nothing is processed if the file is bad
    if (problem) {
      setFileError(problem);
      return;
    }
    setFileError(null);
    if (urlRef.current) URL.revokeObjectURL(urlRef.current);
    urlRef.current = URL.createObjectURL(chosen);
    setPreview(urlRef.current);
    setFile(chosen);
    setStage({ name: "reading" });
    let result;
    try {
      result = await estimateMeal(chosen);
    } catch {
      result = { kind: "error" as const };
    }
    if (result.kind === "meal") {
      setRows(result.foods.map((f) => ({ name: f.name, calories: String(f.calories), protein: String(f.protein), fats: String(f.fats), carbs: String(f.carbs) })));
      setStage({ name: "review", isSample: result.isSample });
    } else if (result.kind === "not-food") setStage({ name: "not-food" });
    else setStage({ name: "failed" });
  }

  const timeValue = eatenAt ?? defaultTime;
  const edit = (i: number, key: keyof Row, value: string) =>
    setRows((r) => r.map((row, idx) => (idx === i ? { ...row, [key]: value } : row)));

  function confirm() {
    if (rows.length === 0) {
      setFormError("Add at least one item, or cancel.");
      return;
    }
    const errs: Record<number, string> = {};
    let calories = 0, protein = 0, fats = 0, carbs = 0;
    let iso = "";
    rows.forEach((row, i) => {
      const r = validateMeal({ ...row, eatenAt: timeValue });
      if (!r.ok) errs[i] = r.errors.calories ?? r.errors.protein ?? r.errors.fats ?? r.errors.carbs ?? r.errors.eatenAt;
      else {
        calories += r.meal.calories; protein += r.meal.protein; fats += r.meal.fats; carbs += r.meal.carbs;
        iso = r.meal.eatenAt;
      }
    });
    setRowErrors(errs);
    if (Object.keys(errs).length > 0) { setFormError(null); return; }
    const name = rows.map((r) => r.name.trim()).filter(Boolean).join(", ") || "Meal";
    if (addMeal({ name, calories, protein, fats, carbs, eatenAt: iso, source: "photo" })) router.push("/"); // S1-AC4
    else setFormError("Could not save on this device. Check that your browser allows site storage.");
  }

  async function saveProgressPhoto() {
    if (!file) return;
    try {
      const image = await downscaleToDataUrl(file);
      if (addProgressPhoto({ date: dayKey(new Date()), image })) router.push("/progress-photos");
      else setFormError("Could not save that photo. Storage on this device may be full.");
    } catch {
      setFormError("Could not save that photo.");
    }
  }

  return (
    <div className="mx-auto max-w-sm space-y-4 p-4">
      <h1 className="text-xl font-semibold">Add a meal from a photo</h1>

      {stage.name === "choose" && (
        <section className="space-y-3">
          <p className="text-sm text-gray-600">Your meal photo is not saved. In this version the food estimate is a sample, not real recognition.</p>
          {fileError && <p role="alert" className="rounded-lg bg-red-50 p-3 text-sm text-red-800">{fileError}</p>}
          <label className="grid h-48 cursor-pointer place-items-center rounded-2xl border-2 border-dashed border-blue-400 bg-blue-50 text-center">
            <span className="text-base font-semibold">Take or choose a photo<br /><small className="font-normal text-gray-600">JPG or PNG, under 10 MB</small></span>
            <input type="file" accept="image/jpeg,image/png" className="sr-only" onChange={onChoose} aria-label="Choose a meal photo" />
          </label>
          <div className="flex gap-2">
            <Link href="/" className={secondary}>Cancel</Link>
            <Link href="/add-meal" className={secondary}>Add by hand</Link>
          </div>
        </section>
      )}

      {preview && stage.name !== "choose" && (
        // eslint-disable-next-line @next/next/no-img-element
        <img src={preview} alt="Your meal" className="h-40 w-full rounded-xl object-cover" />
      )}

      {stage.name === "reading" && <p role="status" className="text-sm text-gray-700">Reading your photo...</p>}

      {stage.name === "review" && (
        <section className="space-y-3">
          <h2 className="text-lg font-semibold">Is this right?</h2>
          {stage.isSample && (
            <p className="rounded-lg bg-yellow-50 p-2 text-sm text-yellow-900">Sample estimate, not real recognition yet. Please check and fix it.</p>
          )}
          {rows.map((row, i) => (
            <div key={i} className="space-y-1 rounded-xl border p-2">
              <input className={field} aria-label={`Food ${i + 1} name`} value={row.name} onChange={(e) => edit(i, "name", e.target.value)} />
              <div className="grid grid-cols-4 gap-1">
                {(["calories", "protein", "fats", "carbs"] as const).map((k) => (
                  <label key={k} className="text-xs text-gray-600">
                    {k === "calories" ? "kcal" : `${k} g`}
                    <input className={field} inputMode="decimal" aria-label={`Food ${i + 1} ${k}`} value={row[k]} onChange={(e) => edit(i, k, e.target.value)} />
                  </label>
                ))}
              </div>
              {rowErrors[i] && <p role="alert" className="text-sm text-red-700">{rowErrors[i]}</p>}
              <button type="button" className="text-sm text-red-700 underline" onClick={() => setRows((r) => r.filter((_, idx) => idx !== i))}>Remove</button>
            </div>
          ))}
          <button type="button" className="text-sm text-green-800 underline" onClick={() => setRows((r) => [...r, { name: "", calories: "", protein: "", fats: "", carbs: "" }])}>+ Add an item</button>
          <label className="block text-sm font-medium">
            When did you eat it?
            <input className={`${field} mt-1`} type="datetime-local" value={timeValue} onChange={(e) => setEatenAt(e.target.value)} />
          </label>
          {formError && <p role="alert" className="text-sm text-red-700">{formError}</p>}
          <div className="flex gap-2">
            <Link href="/" className={secondary}>Cancel</Link>
            <button type="button" className={primary} onClick={confirm}>Confirm meal</button>
          </div>
        </section>
      )}

      {stage.name === "not-food" && (
        <section className="space-y-3">
          <p className="text-base font-medium">Uh oh! I can&apos;t recognize your meal! Would you like me to add it to your progress photos?</p>
          {formError && <p role="alert" className="text-sm text-red-700">{formError}</p>}
          <div className="flex gap-2">
            <button type="button" className={secondary} onClick={() => router.push("/")}>Discard</button>
            <button type="button" className={primary} onClick={saveProgressPhoto}>Add to progress photos</button>
          </div>
        </section>
      )}

      {stage.name === "failed" && (
        <section className="space-y-3">
          <p role="alert" className="text-base font-medium">Could not read this photo.</p>
          <div className="flex flex-wrap gap-2">
            <button type="button" className={secondary} onClick={reset}>Try again</button>
            <Link href="/add-meal" className={primary}>Enter by hand</Link>
            <Link href="/" className={secondary}>Cancel</Link>
          </div>
        </section>
      )}
    </div>
  );
}
