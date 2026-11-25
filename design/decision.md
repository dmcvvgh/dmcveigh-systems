# Design decision: the Today screen

> DRAFT written by Claude as a proposal. **You make this decision.** Edit the "Chosen" section so
> it is in your own words, or pick a different option.

## The three mockups

| | Mockup | Home screen is... | Best at |
|---|---|---|---|
| A | [list first](mockups/mockup-a-list-first.html) | Today's meals and totals, two buttons at the bottom | Seeing what you ate |
| B | [photo first](mockups/mockup-b-photo-first.html) | The camera, with the estimate check right under it | Logging a meal fast (S1) |
| C | [dashboard first](mockups/mockup-c-dashboard-first.html) | Eaten vs burned vs goal, a trend chart, a timeline | Knowing if you are on track (S3-AC6) |

## Proposal (Claude's suggestion, not yet your choice)

**Mockup B's photo capture and estimate check, with Mockup A's meal list underneath.**
For v1, S1 is the story the lab builds and tests, and your riskiest assumption in
`discovery/requirements.md` is that logging must take much less effort than the notes app. B
makes the photo the first thing you see. A's list keeps the day's totals and meals on the same
screen, so you do not need a second screen to see what you logged. C's chart and deficit are for
S3 and can come in a later sprint.

## Chosen

*(Student: write your choice and why, in your own words, here.)*

## Check against two of Nielsen's heuristics

1. **User control and freedom.** Cancel must be available at each step before Confirm (S1-AC8).
   B shows Cancel next to Confirm. A and C do not show the estimate step, so Cancel would need
   adding there.
2. **Visibility of system status.** The user should always see what the system understood. B
   shows the full estimate (each food, calories, macros) before anything is saved, which is S1-AC2.
   C shows running totals but not the estimate step.

*(Other heuristics you could use instead: error prevention, match between the system and the real
world, recognition rather than recall.)*

## What the three mockups do not cover yet

- The "Uh oh! I can't recognize your meal!" screen (S1-AC3).
- The empty state (S1-AC5) and the error messages (S1-AC6, S1-AC7, S1-AC10).
- The "Add meal by hand" form (S1-AC9). It is only a button in each mockup.
