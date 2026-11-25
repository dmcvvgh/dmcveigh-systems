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
- [ ] **Task 2: Browser storage and set-up screen.** Biometrics with confirmation and
  missing-item errors, goal, heavy days, unsafe-goal pop-up, recompute on change.
  (S3-AC1, AC2, AC3, AC5, AC8, AC10)
- [ ] **Task 3: Add meal by hand.** Validation, Cancel, daily totals. (S1-AC4, AC8, AC9, AC10)
- [ ] **Task 4: Today screen (Mockup C).** Budget, eaten, burned, left this week, timeline, empty
  state, chart. (S1-AC5, S3-AC6, AC8)
- [ ] **Task 5: Log a workout.** Calories burned entered by hand. (S2-AC1)
- [ ] **Task 6: Photo flow with a stand-in estimate.** Upload with file checks, confirm and edit,
  not-food screen with save or discard, failure screen with try again or enter by hand.
  (S1-AC1 partly, AC2, AC3, AC6, AC7, AC8, Later-AC4, AC5)
- [ ] **Task 7: Real photo recognition (Gemini).** Server route behind `estimateMeal()`; needs your
  free key in `app/.env.local`. (S1-AC1)
- [ ] **Task 8: Polish and deploy.** Phone check, timing (NFR-3), Vercel, URL in README.
  (NFR-3, NFR-4)

## Acceptance check

Filled in after the build. Mark each criterion pass or fail in the running app.

| Criterion | Pass? | Notes |
|---|---|---|
