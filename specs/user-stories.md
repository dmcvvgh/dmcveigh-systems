# User stories

IDs in brackets, like FR-1, are requirement IDs from `discovery/requirements.md` (Lab 3).
Each criterion is written as "WHEN ... THE SYSTEM SHALL ...". A story is done when every one of
its criteria passes in the running app. Each story has at least one going-wrong criterion.

> DRAFT for the student to check. Lines marked **(new)** were added by Claude to cover a
> requirement or your sprint plan; everything else is your wording.

| Story | Cites | Requirement text (from Lab 3) | Priority in Lab 3 |
|---|---|---|---|
| S1 | FR-1, FR-2, FR-3 | log a food entry with calories and macros; record its time; show daily totals | Must |
| S2 | FR-4 | log a workout (exercise and weight lifted) | Must |
| S2 | FR-11 | pull calories burned from Apple Health / Apple Watch | Could |
| S3 | FR-7 | support a cut or bulk goal using food tracking | Should |

Privacy requirements NFR-1, NFR-2 and NFR-5 apply to all three stories (body data).

## S1 (FR-1, FR-2, FR-3): Log a meal from a photo

As an active person, I want to track all the calories I am consuming so that I can more
effectively cut or bulk weight.

- **S1-AC1:** WHEN the user uploads an image of a meal THE SYSTEM SHALL understand what is on the
  plate and turn it into a lump sum of calories and nutrients.
- **S1-AC2:** AS A CHECK, the user SHALL be able to confirm whether the system got the plate
  correct and edit any options before the meal is catalogued on their plan.
- **S1-AC3 (going wrong):** WHEN the uploaded image is not a meal THE SYSTEM SHALL NOT log it as
  food, and SHALL display a message such as "Uh oh! I can't recognize your meal! Would you like
  me to add it to your progress photos?" with a choice to save it to progress photos (a simple
  save with the date, no comparing in v1) or discard it.
- **S1-AC4 (new):** WHEN the user confirms a meal THE SYSTEM SHALL record the time it was eaten and
  update the day's totals of calories and each macro (protein, fats, carbs).
- **S1-AC5 (going wrong, new):** WHEN the user has no meals logged today THE SYSTEM SHALL show an
  empty state that invites them to upload a photo of their first meal.
- **S1-AC6 (going wrong, new):** IF the uploaded file is not a supported image or is too large THE
  SYSTEM SHALL NOT process it, and SHALL show "Use a JPG or PNG under 10 MB" so the user can choose
  a different photo. (The 10 MB limit is a placeholder; change it if you want.)
- **S1-AC7 (going wrong, new):** IF the system cannot estimate the meal from the photo THE SYSTEM
  SHALL tell the user it could not read the photo and let them try again or enter the meal by hand
  (food name, calories, protein, fats, carbs). A meal entered by hand SHALL be saved the same way
  as one from a photo (S1-AC4).
- **S1-AC8 (new):** WHEN the user taps Cancel at any step before confirming (choosing a photo,
  reading the estimate, or entering a meal by hand) THE SYSTEM SHALL return to the Today screen and
  log nothing.
- **S1-AC9 (new):** WHEN the user taps "Add meal by hand" at any time, with or without a photo, THE
  SYSTEM SHALL let them enter the food name, calories, protein, fats, carbs, and the time it was
  eaten (defaulting to now), so a meal eaten earlier can be logged later.
- **S1-AC10 (going wrong, new):** IF the calories are empty or not a number when saving a meal by
  hand THE SYSTEM SHALL NOT save it and SHALL show "Enter calories as a number, like 450".

## S2 (FR-4, FR-11): Log a workout and calories burned

As an active person, I want my workouts and calories burned recorded so that my plan reflects what
I actually do each day.

- **S2-AC1 (new):** WHEN the user logs a workout (exercise and weight lifted) THE SYSTEM SHALL
  save it to that day.
- **S2-AC2:** WHEN the user uploads an exercise activity THE SYSTEM SHALL estimate the calories
  burned based on the activity and the user's profile, so that the same activity can burn more
  for a larger person.
- **S2-AC3 (not in v1; health app is Apple Health):** WHEN the user connects Apple Health THE SYSTEM SHALL synchronize total steps,
  calories, and related data and include them in the user's daily totals.
- **S2-AC4 (going wrong):** IF the health app sync fails THE SYSTEM SHALL tell the user the sync
  did not work and let them enter or upload their activity manually, so their daily totals are
  still complete.

## S3 (FR-7): Get a personalized plan and see my progress

As an active person, I want a plan made for my fitness journey so that I can cut or bulk weight
in a way that fits my body and goals.

- **S3-AC1:** WHEN the user enrolls in the program THE SYSTEM SHALL collect their sex, age,
  height, weight, and desired training intensity (light, moderate, or high), as part of setting
  their goals.
- **S3-AC2 (going wrong):** IF any required biometric (sex, age, height, weight, or training
  intensity) is missing THE SYSTEM SHALL NOT create the plan, and SHALL show which items are
  missing. WHEN all biometrics are entered THE SYSTEM SHALL show them back to the user to confirm
  before the goal is set.
- **S3-AC3:** WHEN the user sets a goal THE SYSTEM SHALL accept a direction (cut weight or bulk
  weight), a target amount, and a target date.
- **S3-AC4:** WHEN the user requests a plan be made for their fitness journey THE SYSTEM SHALL
  create a customized plan based on all their biometrics and goals.
- **S3-AC5:** WHEN the user changes their goal (amount or target date) or their biometrics change
  THE SYSTEM SHALL adjust the plan accordingly.
- **S3-AC6 (new, from your sprint plan):** WHEN the user views their progress THE SYSTEM SHALL
  show a chart of calories eaten against calories burned for the week, against their weekly
  budget.
- **S3-AC7 (new):** WHEN the user sets a goal THE SYSTEM SHALL turn it into a weekly calorie
  budget (a rough rule of thumb is about 3,500 calories per pound), rather than a fixed daily
  target. The budget SHALL depend on the user's biometrics and training intensity, so a smaller,
  lighter person gets a different budget from a larger, heavier one.
- **S3-AC8 (new):** WHEN the user picks their heavy lifting days and their rest days THE SYSTEM
  SHALL give heavy lifting days a larger share, and rest days a smaller share, of the week's
  calories, and show how many calories are left this week.
- **S3-AC10 (going wrong, new):** IF the goal would mean losing weight unsafely fast (more than 2 lb
  a week, or a daily budget under 1,200 calories, which is the floor) THE SYSTEM SHALL show a
  pop-up suggesting a smaller goal to start with, and let the user work up to the larger goal
  later. The system SHALL NOT encourage starving. The pop-up SHALL NOT silently change the goal.
- **S3-AC9 (going wrong, new):** IF the user has not picked any heavy lifting days THE SYSTEM
  SHALL split the weekly budget evenly across the days and tell the user it did so.

## Later (not in v1)

Progress photos and progress numbers (cites FR-8, Could). Kept here so the idea is not lost, but
outside the MVP scope in `requirements.md`. Later-AC4 and Later-AC5 also apply in v1 to the simple
photo save from S1-AC3.

- **Later-AC1:** WHEN the user adds a photo to their progress photos (from S1-AC3 or directly)
  THE SYSTEM SHALL save it with its date.
- **Later-AC2:** WHEN the user views their progress photos THE SYSTEM SHALL let them compare
  photos from different dates.
- **Later-AC3 (going wrong):** IF the user has fewer than two progress photos THE SYSTEM SHALL
  NOT require a comparison, and SHALL show a message that a second photo is needed to compare.
  Progress photos SHALL be optional.
- **Later-AC4 (privacy, new):** THE SYSTEM SHALL show a progress photo only to the user who saved
  it.
- **Later-AC5 (new):** WHEN the user deletes a progress photo THE SYSTEM SHALL remove it
  permanently.
- **Later-AC6 (new):** WHEN the user enters a progress number (for example their weight) with a
  date THE SYSTEM SHALL save it, so a user who does not want to use photos can still track
  progress.
- **Later-AC7 (going wrong, new):** IF a progress number is empty or not a number THE SYSTEM SHALL
  NOT save it and SHALL show "Enter a number, like 165".

## Open questions

- "Analyze" progress photos: only side-by-side comparison, or should the AI describe changes?
- Apple Health (future, not v1): data would come from a native iPhone app. In v1 the user enters
  calories burned by hand.

## Decided

- Calorie rule of thumb (about 3,500 per pound) and the weekly budget are fine for the demo.
- Training intensity levels are light, moderate, and high.
- Meal photos are not saved, only the numbers.
- Progress photos are visible only to the user and can be deleted.
- Unsafe goal rule: more than 2 lb a week, or a daily budget under 1,200 calories (the floor).
- Progress numbers are later, not v1.
- Health app is Apple Health. The Gemini free-key limits are not checked for the demo.
