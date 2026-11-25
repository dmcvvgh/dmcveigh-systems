# Usability test 1

Written from the student's account of the test on Nov 25. Anything they did not say is marked
**Not noted** so it is not guessed.

## Setup

- **Who:** one of the student's roommates, who had not seen the app. (No name recorded.)
- **Device:** the student's own phone, which is small.
- **Task given:** enter a meal and your fitness goals.
- **Instructions given:** none beyond showing the app.

## What happened

- **Did they finish?** They were able to use the app as intended without any real instruction,
  and completed the task: entering a meal and setting fitness goals.
- **Where they hesitated:**
  1. When entering the number of days they stay active (the heavy lifting days part of set-up).
  2. On the home page, where it was hard to see some of the information.
- **What they said:** their first thought on logging a meal was that it is a lot of things to plug
  in at one time. The student thinks that may be hard to streamline without the photo API
  integration (real photo recognition, which was skipped for Lab 4).
- **What they clicked that did nothing:** **Not noted.**
- **How fast was logging a meal?** Pretty fast, in the student's words. **Not timed**, so there is
  no number for NFR-3 (about 7 seconds with no edits, 20 to 30 seconds with edits).

## What the student saw

1. **Dark mode:** when the computer or phone is in dark mode, some of the text does not show up
   properly.
2. **Misaligned buttons:** a couple of buttons were misaligned on the student's phone,
   specifically where you select how many days you want to be active (the heavy lifting days).
   The student's phone is small, so it could be the screen size, or the buttons could just need
   realigning so they are all in order.
3. **Look:** the student thinks more could be done to make the app more visually appealing.
4. **What worked:** the root purpose of the app is all there, and the student likes the graph.

**Possible links between what they saw and what the roommate did** (Claude's reading, not
confirmed): the hard-to-see home page information may have been the dark-mode text problem. The
hesitation on "days staying active" may be partly the misaligned buttons, and partly the label:
the set-up asks you to pick which days are "Heavy lifting days", not a number of days, so the
wording may not match how the roommate thought about it.

## Top two changes

1. **Fix the dark-mode text.**
2. **Fix the heavy-day button alignment on small phones.**

(Making the app look nicer is a good later change, but it is not in the top two.)

## Changes made

Both top changes were made on Nov 25 and checked in a browser at 375 and 320 pixels wide, with
the browser set to dark mode.

- **Dark mode:** the cause was that the starter template turns the page text near-white in dark
  mode, while the app's boxes are white, so the text vanished. The app is now locked to its light
  look (`app/src/app/globals.css`). A real dark theme is a possible later change.
- **Heavy-day buttons:** the seven day buttons used a wrapping layout, so on a narrow screen they
  broke across rows unevenly. They are now an even single row of seven
  (`app/src/app/setup/SetupForm.tsx`).
