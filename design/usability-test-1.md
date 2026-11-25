# Usability test 1

Written from the student's account of the test on Nov 25. Anything they did not say is marked
**Not noted** so it is not guessed. The student can fill those in.

## Setup

- **Who:** one of the student's roommates, who had not seen the app. (No name recorded.)
- **Device:** the student's own phone, which is small.
- **Task given:** **Not noted.**
- **Instructions given:** none beyond showing the app.

## What happened

- **Did they finish?** They were able to use the app as intended without any real instruction.
  **Not noted:** which task or tasks they completed, and how long logging a meal took (the
  NFR-3 check was not timed).
- **Where they hesitated:** **Not noted.** The student's impression was that it was pretty
  intuitive, because the buttons are clearly labeled.
- **What they said:** **Not noted.**
- **What they clicked that did nothing:** **Not noted.**

## What the student saw

1. **Dark mode:** when the computer or phone is in dark mode, some of the text does not show up
   properly.
2. **Misaligned buttons:** a couple of buttons were misaligned on the student's phone,
   specifically where you select how many days you want to be active (the heavy lifting days).
   The student's phone is small, so it could be the screen size, or the buttons could just need
   realigning so they are all in order.
3. **Look:** the student thinks more could be done to make the app more visually appealing.
4. **What worked:** the root purpose of the app is all there, and the student likes the graph.

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
