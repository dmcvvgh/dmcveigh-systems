# v1 build checklist

Each task is 10 to 30 minutes. After each one: run the app (`npm run dev` in `app/`), check the
criteria named for that task, run `npm test`, tick the box, and commit. Criteria IDs are in
[user-stories.md](user-stories.md). The plan these came from is approved; the design is in
[v1-spec.md](v1-spec.md).

- [x] **Task 0: Set up.** Next.js + Tailwind + Vitest in `app/`, a hello page, one passing test.
- [ ] **Task 1: Supabase and sign-in.** Create the project, write `architecture/schema.sql` and
  `policies.sql`, add email sign-in and sign-out. (NFR-1, NFR-2, NFR-5)
- [ ] **Task 2: Budget rules with tests.** Weekly budget, heavy and rest days, even split with no
  heavy days, unsafe-goal check. (S3-AC7, AC8, AC9, AC10 rules)
- [ ] **Task 3: Set-up screen.** Biometrics with confirmation and missing-item errors, goal, heavy
  days. (S3-AC1, AC2, AC3, AC8)
- [ ] **Task 4: Unsafe-goal pop-up and recompute.** (S3-AC10, AC5)
- [ ] **Task 5: Add meal by hand.** Validation, Cancel, daily totals. (S1-AC4, AC8, AC9, AC10)
- [ ] **Task 6: Today screen (Mockup C).** Budget, eaten, burned, left this week, timeline, empty
  state, chart. (S1-AC5, S3-AC6, AC8)
- [ ] **Task 7: Log a workout.** Calories burned entered by hand. (S2-AC1)
- [ ] **Task 8: Photo upload and Gemini route.** File checks, `estimateMeal()` server function.
  (S1-AC1, AC6)
- [ ] **Task 9: Confirm, edit, not-food, and failure screens.** (S1-AC2, AC3, AC7, AC8, AC4,
  Later-AC4, AC5)
- [ ] **Task 10: Polish and deploy.** Phone check, timing (NFR-3), Vercel, URL in README.
  (NFR-3, NFR-4)

## Acceptance check

Filled in after the build. Mark each criterion pass or fail in the running app.

| Criterion | Pass? | Notes |
|---|---|---|
