# v1 build checklist

Each task is 10 to 30 minutes. After each one: run the app (`npm run dev` in `app/`), check the
criteria named for that task, run `npm test`, tick the box, and commit. Criteria IDs are in
[user-stories.md](user-stories.md). The plan these came from is approved; the design is in
[v1-spec.md](v1-spec.md).

> Trimmed on Nov 25 to fit Lab 4: data is stored in the browser (the database and sign-in are
> Lab 6), and the food estimate is a clearly labeled stand-in unless a Gemini key is added.

- [x] **Task 0: Set up.** Next.js + Tailwind + Vitest in `app/`, a hello page, one passing test.
- [x] **Task 1: Budget rules with tests.** Weekly budget, heavy and rest days, even split with no
  heavy days, unsafe-goal check and safer-goal suggestion. (S3-AC7, AC8, AC9, AC10 rules)
- [x] **Task 2: Browser storage and set-up screen.** Biometrics with confirmation and
  missing-item errors, goal, heavy days, unsafe-goal pop-up, recompute on change.
  (S3-AC1, AC2, AC3, AC5, AC8, AC10)
- [x] **Task 3: Add meal by hand.** Validation, Cancel, daily totals. (S1-AC4, AC8, AC9, AC10)
- [x] **Task 4: Today screen (Mockup C).** Budget, eaten, burned, left this week, timeline, empty
  state, chart. (S1-AC5, S3-AC6, AC8)
- [x] **Task 5: Log a workout.** Calories burned entered by hand. (S2-AC1)
- [x] **Task 6: Photo flow with a stand-in estimate.** Upload with file checks, confirm and edit,
  not-food screen with save or discard, failure screen with try again or enter by hand.
  (S1-AC1 partly, AC2, AC3, AC6, AC7, AC8, Later-AC4, AC5)
- [ ] **Task 7: Real photo recognition (Gemini). SKIPPED for Lab 4 (not required); the stand-in estimate stays.** Server route behind `estimateMeal()`; needs your
  free key in `app/.env.local`. (S1-AC1)
- [ ] **Task 8: Polish and deploy.** Phone check (done), timing (NFR-3, measured in the usability
  test), Vercel, URL in README. (NFR-3, NFR-4)

## Acceptance check

Checked on Nov 25 by Claude, using unit tests and a headless browser at phone width. **The
student should still confirm each one in the running app** (the definition of done in CLAUDE.md).

| Criterion | Result | How it was checked |
|---|---|---|
| S1-AC1 photo to calories | **Partial** | A sample estimate is shown and labeled as a sample. Real recognition was skipped (Task 7). |
| S1-AC2 confirm or edit | Pass | Browser: edit, remove, add items; bad number shows an error |
| S1-AC3 not a meal | Pass | Browser: "Uh oh!" message, save to progress photos or discard |
| S1-AC4 time and daily totals | Pass | Unit tests and browser (totals matched by hand) |
| S1-AC5 empty state | Pass | Browser |
| S1-AC6 bad file | Pass | Browser: a PDF and an 11 MB file both rejected with the message |
| S1-AC7 could not read | Pass | Browser: try again, enter by hand, cancel |
| S1-AC8 cancel | Pass | Browser: from the photo chooser, the review screen, and the by-hand form |
| S1-AC9 add by hand, any time | Pass | Browser: time can be set to earlier |
| S1-AC10 calories error | Pass | Unit tests and browser |
| S2-AC1 log a workout | Pass | Unit tests and browser; burned today goes up |
| S2-AC2, AC3, AC4 | Not in v1 | Estimating burn, health sync and its fallback are later |
| S3-AC1 collect biometrics | Pass | Browser |
| S3-AC2 missing items and confirm | Pass | Unit tests and browser |
| S3-AC3 goal | Pass | Unit tests and browser |
| S3-AC4 customized plan | **Partial** | The plan is the weekly budget with heavy and rest days, as decided in the spec |
| S3-AC5 adjusts when the goal changes | Pass | Browser: budget changed from 17,486 to 15,386 after editing the goal |
| S3-AC6 weekly chart | Pass | Browser |
| S3-AC7 weekly budget from biometrics | Pass | Unit tests |
| S3-AC8 heavy days get more, left this week | Pass | Unit tests and browser |
| S3-AC9 no heavy days: even split | Pass | Unit tests and browser |
| S3-AC10 unsafe goal pop-up | Pass | Unit tests and browser |
| Later-AC4, AC5 (saved photo private, deletable) | Pass | Browser. Private because it is stored only on this device. |
| NFR-4 usable on a phone | Pass | All six screens fit at 375 and 320 pixels with no sideways scrolling |
| NFR-3 logging speed | **Not measured yet** | To be timed in the usability test (Part F) |
