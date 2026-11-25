# Flow: Log a meal from a photo (S1)

> DRAFT for the student to check. Covers S1-AC1 to S1-AC4 (see `specs/user-stories.md`).

The flow has two lanes: the **User** and the **System** (which includes the AI that reads the
photo). Every decision has an answer for both branches, including errors and empty states.

```mermaid
flowchart TD
  subgraph User
    U1[Open the app, Today screen]
    U2[Tap Add meal, choose a photo]
    U2b[Tap Add meal by hand]
    U3[Look at the estimate]
    U4[Edit items or amounts]
    U5[Tap Confirm]
    U6{Save as progress photo?}
    U7[Choose a different photo]
    U8[Fill in food, calories, macros, time eaten]
    UC[Tap Cancel]
  end

  subgraph System
    S1{Any meals logged today?}
    S2[Empty state: Take or upload a photo of your first meal]
    S3[Show meals and daily totals: calories, protein, fats, carbs]
    S4{Valid image file, small enough?}
    S5[Error: Use a JPG or PNG under 10 MB]
    S6[Read the photo, estimate foods, calories, macros]
    S7{Estimate worked?}
    S8[Error: Could not read this photo. Try again or enter the meal by hand]
    S9{Food on the plate?}
    S10[Uh oh! I can't recognize your meal! Add it to progress photos?]
    S11[Save photo with today's date, show it on the Progress photos page]
    S12[Discard photo, nothing logged]
    S13[Show estimate: each food, total calories and macros]
    S14[Recalculate totals]
    S15[Save meal with time eaten]
    S16[Update daily totals]
    S17[Today screen shows the new meal]
    S18{Calories a number?}
    S19[Error: Enter calories as a number, like 450]
    S20[Nothing logged, back to Today screen]
  end

  U1 --> S1
  S1 -- No --> S2
  S1 -- Yes --> S3
  S2 --> U2
  S2 --> U2b
  S3 --> U2
  S3 --> U2b
  U2 --> S4
  S4 -- No --> S5 --> U7 --> S4
  S4 -- Yes --> S6 --> S7
  S7 -- No --> S8
  S8 --> U2
  S8 --> U2b
  S7 -- Yes --> S9
  S9 -- No --> S10 --> U6
  U6 -- Yes --> S11 --> S1
  U6 -- No --> S12 --> S1
  S9 -- Yes --> S13 --> U3
  U3 -- Correct --> U5
  U3 -- Wrong --> U4 --> S14 --> U3
  U5 --> S15
  U2b --> U8 --> S18
  S18 -- No --> S19 --> U8
  S18 -- Yes --> S15
  S15 --> S16 --> S17
  U3 -.-> UC
  U8 -.-> UC
  U2 -.-> UC
  UC --> S20 --> S1
```

## Which story criterion each part satisfies

| Part of the flow | Criterion |
|---|---|
| Read the photo and estimate calories and nutrients | S1-AC1 |
| Look at the estimate, edit, then Confirm | S1-AC2 |
| Not a meal: "Uh oh!" message, save as progress photo or discard | S1-AC3 |
| Save meal with time, update daily totals | S1-AC4 |
| Empty state: invite first photo | S1-AC5 |
| Invalid or oversized file | S1-AC6 |
| Estimate failed: try again or enter by hand | S1-AC7 |
| Cancel before confirming, nothing logged (dotted lines) | S1-AC8 |
| Add meal by hand at any time, choose the time eaten | S1-AC9 |
| Calories missing or not a number | S1-AC10 |

## Decided

- "Enter the meal by hand" is both a fallback when the estimate fails and a button you can use
  any time (for example to log something you ate earlier).
- Cancel is available at every step before Confirm and returns to the Today screen with nothing
  logged.
- After discarding a non-meal photo, the user returns to the Today screen.
- "Offline" means manual: if you ate something and forgot to log it with a photo, you can still
  enter the calories by hand later (S1-AC9). Working with no internet connection is not in v1.
