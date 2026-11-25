# Fitness and Calorie Tracker (working name) v1, spec

> DRAFT for the student to check. The student confirmed all of Claude's earlier guesses on
> Nov 25.

## Intent

This is for college students who want to cut or bulk but find tracking food and workouts too slow
and scattered (see [discovery/requirements.md](../discovery/requirements.md)). The job it does:
log what you eat from a photo (or by hand) with almost no effort, record what you burn, and show
whether you are on track for a weekly calorie budget that comes from your cut or bulk goal. In
this demo version it is built for one user per account.

## Stories and acceptance criteria

All criteria live in [specs/user-stories.md](user-stories.md). v1 builds these:

| Story | In v1 | Not in v1 |
|---|---|---|
| S1 Log a meal from a photo | S1-AC1 to S1-AC10 | none |
| S2 Log a workout and calories burned | S2-AC1 (log a workout); calories burned entered by hand | S2-AC2 (estimating burn from an uploaded activity), S2-AC3 and S2-AC4 (health app sync and its fallback) |
| S3 Plan and progress | S3-AC1, S3-AC2, S3-AC3, S3-AC5, S3-AC6, S3-AC7, S3-AC8, S3-AC9, S3-AC10 | S3-AC4 as a full custom plan: in v1 the "plan" is the weekly budget with heavy and rest days |

Progress photos and progress numbers (the "Later" section) are not built, except the simple "save
with its date" that S1-AC3 offers for a photo that is not a meal. That saved photo is private to
the user and can be deleted (Later-AC4, Later-AC5).

## Screens and flow

- Flow: [design/flow.md](../design/flow.md) (S1, including every error and empty state).
- Chosen home screen: [Mockup C, dashboard first](../design/mockups/mockup-c-dashboard-first.html).
  Reasons are in [design/decision.md](../design/decision.md).
- Changes to Mockup C already decided: show "calories left this week" against the weekly budget
  instead of a single daily target.

Screens in v1:
1. **Set up** biometrics, goal, and heavy lifting days (S3-AC1 to S3-AC3, S3-AC8).
2. **Today (home)**: week budget, eaten, burned, left this week, chart, timeline of today's meals,
   "+ Photo" and "By hand" buttons.
3. **Add meal from photo**: upload, estimate, confirm or edit, Cancel.
4. **Add meal by hand**: name, calories, protein, fats, carbs, time eaten.
5. **Log workout**: exercise, weight lifted, calories burned.

## Data

**v1: stored in the browser** (local storage on the user's device). The Supabase database with
sign-in and per-user access rules (row-level security) comes in Lab 6; the fields below are the
same either way. Field names and types are for the build plan to settle.

| Thing | Fields |
|---|---|
| profile | user, sex, age, height, weight, training intensity |
| goal | user, direction (cut or bulk), target amount, target date |
| training_day | user, weekday, kind (heavy or rest) |
| meal | user, name, calories, protein, fats, carbs, eaten_at, source (photo or hand) |
| workout | user, date, exercise, weight lifted, calories burned (entered by hand) |
| progress_photo | user, image, saved date (only from S1-AC3 in v1; the user can delete it) |
| progress_entry (Later) | user, date, value such as weight |

Meal photos are sent to the AI for analysis and are **not stored**. Only the numbers are saved. Weekly budget
numbers are calculated, not stored.

## Decisions already made

- **Stack:** Next.js (TypeScript) with Tailwind, deployed to Vercel.
- **Database and sign-in: Supabase, but moved to Lab 6 (changed Nov 25).** The course says v1 can
  live in the browser and a real database comes in Lab 6, so v1 stores data in the browser. The
  reasoning below still holds for the later move.
  Original reasoning: Chosen over device-only storage because data kept only on a
  phone is lost if the user clears it or changes phones. This is a compromise: data is no longer
  only on the user's device (NFR-5 was rewritten, see `discovery/requirements.md`). Privacy comes
  from sign-in plus per-user access rules, and the user can delete their data. We may look at
  other storage later.
- **Photo to calories: v1 uses a labeled sample estimate (changed Nov 25).** Real recognition was
  skipped because Lab 4 does not require it. The Gemini plan below still holds for later; the
  screens already call one function (`estimateMeal`) that the Gemini code would replace.
  Original decision: Google Gemini free API key. It is called only from server code. The key
  is in `app/.env.local` and in Vercel's environment settings, never in the browser or on GitHub.
  The built-in "try again or enter by hand" path (S1-AC7) covers failures and quota limits.
- **Weekly budget, not a daily target.** The user sets a goal, picks heavy lifting days, and the
  system divides a weekly calorie budget across the week, giving heavy days more. Rough rule of
  thumb: about 3,500 calories per pound. The daily base comes from a standard formula
  (Mifflin-St Jeor) from sex, age, height, and weight, scaled by training intensity: light,
  moderate, or high. A smaller, lighter person therefore gets a lower budget than a larger,
  heavier one at the same intensity.
- **Home screen: Mockup C**, because it shows where you are today and does not assume you are
  eating when you open it.
- **Calories burned are entered by hand in v1** (no health-app sync).
- **"Burned" on the Today screen** is an estimate: the user's maintenance calories (from the
  budget formula) plus any workout calories they log. Known simplification: maintenance already
  includes the chosen training intensity, so logged workouts add on top of it. "Left this week" is
  the weekly budget minus calories eaten so far this week; the week runs Sunday to Saturday.
- **Cancel** is available at every step before Confirm (S1-AC8).
- **Unsafe goals:** the system shows a pop-up suggesting a smaller goal to start with and working
  up, and does not encourage starving (S3-AC10). Rule: more than 2 lb a week, or a daily budget
  under 1,200 calories (the floor).
- **Meal photos are not saved**, only the numbers.
- **Progress photos** are visible only to the user and can be deleted. Progress numbers (for
  example weight) are an option for users who do not want photos, and are planned for later.
- **Logging speed (NFR-3):** about 7 seconds when the estimate is accepted as is (aim for less),
  and about 20 to 30 seconds with corrections or hand entry. The usability test should time this.
- **Gemini free-key limits and terms:** not checked. Accepted as fine for a demo.

## Considered and rejected

- **Data stored only in the browser:** simplest, but loses data when cleared or on a new phone.
- **A fixed daily calorie target:** too repetitive, and the user does not know the right number
  for one day. Replaced by a weekly budget with heavy and rest days.
- **"Sign in with Claude or ChatGPT" to use the user's own subscription:** apps cannot do this
  as far as we know, so not planned.
- **Bring-your-own-key:** adds friction and means storing a user's secret.
- **A model running in the browser:** free and private, but large downloads, lower accuracy, and
  more work.
- **A paid vision API:** costs money for a demo.
- **A made-up "fake" estimate:** it cannot tell foods apart. A built-in food list is only a
  backup for failures.

## Out of scope for v1

- Apple Health sync and the Apple Watch (FR-11).
- Estimating calories burned from an uploaded activity (S2-AC2).
- A full AI-written fitness plan (S3-AC4 beyond the weekly budget).
- Comparing progress photos (the "Later" section).
- Next-workout suggestions, lagging muscle groups, reminders, rankings, body fat (FR-5, FR-6,
  FR-9, FR-10, FR-12 in `requirements.md`).
- Working with no internet. Manual entry means entering a meal by hand later (S1-AC9).

## Open questions

- Apple Health (future, not v1): the data would come from a native iPhone app. In v1 the user
  enters calories burned by hand.
- The Gemini free-key limits and data terms were not checked. Accepted for the demo. If the app
  goes beyond a class project, read them and update NFR-1.
- Progress numbers (weight updates) are later, not v1.
