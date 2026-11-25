# Design decision: the Today screen

> The choice and its reasons are the student's, recorded from their message on Nov 25. Claude
> drafted the mockups, the proposal below, and the heuristic checks. Please edit anything that
> is not how you would say it.

## The three mockups

| | Mockup | Home screen is... | Best at |
|---|---|---|---|
| A | [list first](mockups/mockup-a-list-first.html) | Today's meals and totals, two buttons at the bottom | Seeing what you ate |
| B | [photo first](mockups/mockup-b-photo-first.html) | The camera, with the estimate check right under it | Logging a meal fast (S1) |
| C | [dashboard first](mockups/mockup-c-dashboard-first.html) | Eaten vs burned vs goal, a trend chart, a timeline | Knowing if you are on track (S3-AC6) |

## Claude's original proposal (not chosen)

**Mockup B's photo capture and estimate check, with Mockup A's meal list underneath.**
For v1, S1 is the story the lab builds and tests, and your riskiest assumption in
`discovery/requirements.md` is that logging must take much less effort than the notes app. B
makes the photo the first thing you see. A's list keeps the day's totals and meals on the same
screen, so you do not need a second screen to see what you logged. C's chart and deficit are for
S3 and can come in a later sprint.

## Chosen: C, dashboard first

I picked the dashboard because it makes it easier to understand where you are during the day,
and it shows an exact chart of calories eaten versus calories burned so you can stay on top of
things. I think starting with a list or a photo first is a bit too in your face and not very
intuitive, because it expects you to be eating something whenever you open the app, and that is
not always the main purpose of opening it.

## Check against two of Nielsen's heuristics

1. **Visibility of system status.** C answers "where am I right now?" on the first screen: eaten,
   burned, and deficit, plus a 7-day trend. This fits your reason for choosing it.
2. **User control and freedom.** C only has two buttons ("+ Photo" and "By hand"), so every flow
   they start must let the user back out. This is S1-AC8: Cancel at every step before Confirm.
   The mockup does not show the Cancel button yet, because it only shows the home screen.

*(You can swap either heuristic for another: error prevention, match between the system and the
real world, recognition rather than recall.)*

## What this choice means for the build

- The home screen needs the goal and a calories-burned figure, which come from S3 (the plan and
  chart, S3-AC6) and S2 (calories burned). In the earlier proposal I had left those for later.
  Choosing C pulls a simple version of them into v1. Decide how simple: for example, a fixed
  daily target typed in by the user, and a burned figure typed in by hand, with no health sync
  yet.
- S1 (logging a meal) is still the story the build starts with, since it feeds the "eaten" number.

## What the three mockups do not cover yet

- The "Uh oh! I can't recognize your meal!" screen (S1-AC3).
- The empty state (S1-AC5) and the error messages (S1-AC6, S1-AC7, S1-AC10).
- The "Add meal by hand" form (S1-AC9). It is only a button in each mockup.
