# Flow: Log a meal from a photo (S1)

> DRAFT for the student to check. Covers S1-AC1 to S1-AC4 (see `specs/user-stories.md`).
> Boxes marked **(new)** are not in a story yet; keep them or cut them.

The flow has two lanes: the **User** and the **System** (which includes the AI that reads the
photo). Every decision has an answer for both branches, including errors and empty states.

```mermaid
flowchart TD
  subgraph User
    U1[Open the app, Today screen]
    U2[Tap Add meal, choose a photo]
    U3[Look at the estimate]
    U4[Edit items or amounts]
    U5[Tap Confirm]
    U6{Save as progress photo?}
    U7[Choose a different photo]
  end

  subgraph System
    S1{Any meals logged today?}
    S2[Empty state: Take or upload a photo of your first meal]
    S3[Show meals and daily totals: calories, protein, fats, carbs]
    S4{Valid image file, small enough?}
    S5[Error: Use a JPG or PNG under 10 MB]
    S6[Read the photo, estimate foods, calories, macros]
    S7{Estimate worked?}
    S8[Error: Could not read this photo. Try again or enter the meal by hand - new]
    S9{Food on the plate?}
    S10[Uh oh! I can't recognize your meal! Add it to progress photos?]
    S11[Save photo with today's date]
    S12[Discard photo, nothing logged]
    S13[Show estimate: each food, total calories and macros]
    S14[Recalculate totals]
    S15[Save meal with time eaten]
    S16[Update daily totals]
    S17[Today screen shows the new meal]
  end

  U1 --> S1
  S1 -- No --> S2 --> U2
  S1 -- Yes --> S3 --> U2
  U2 --> S4
  S4 -- No --> S5 --> U7 --> S4
  S4 -- Yes --> S6 --> S7
  S7 -- No --> S8 --> U2
  S7 -- Yes --> S9
  S9 -- No --> S10 --> U6
  U6 -- Yes --> S11 --> S1
  U6 -- No --> S12 --> S1
  S9 -- Yes --> S13 --> U3
  U3 -- Correct --> U5
  U3 -- Wrong --> U4 --> S14 --> U3
  U5 --> S15 --> S16 --> S17
```

## Which story criterion each part satisfies

| Part of the flow | Criterion |
|---|---|
| Read the photo and estimate calories and nutrients | S1-AC1 |
| Look at the estimate, edit, then Confirm | S1-AC2 |
| Not a meal: "Uh oh!" message, save as progress photo or discard | S1-AC3 |
| Save meal with time, update daily totals | S1-AC4 |
| Empty state, invalid file, estimate failed | Not in a story yet (see below) |

## Questions to check

1. The empty state, the invalid-file error, and the "estimate failed, enter by hand" box are not
   in any story. Do you want criteria for them? The lab asks for error and empty states in the
   flow, so I would add them to S1.
2. "Enter the meal by hand" matches your Lab 3 requirement FR-1 (typing in calories and macros).
   Keep it as the fallback, or leave it out of v1?
3. After "Discard", the user lands on the Today screen. Is that what you would expect?
4. Is the user ever able to cancel in the middle, for example after choosing a photo but before
   Confirm? The flow has no cancel path yet.
