# CLAUDE.md

## Project overview

A personal problem tracker: a place to jot down problems noticed during the day, rate how often
they happen, and look at them as a list or as sticky notes on a corkboard. Built for Lab 2 of a
Systems Analysis and Design course and deployed as a static site on Vercel.

## Tech stack

- Plain HTML, CSS, and JavaScript in one file: `index.html`
- Data saved in the browser's localStorage
- Hosted on Vercel as a static site (no server code)

## Development Notes

- No frameworks and no build step: everything stays in index.html.
- Never store data on a server; localStorage only.
- Every feature must work on a phone. Check layouts at a narrow width (about 375px) and make sure
  controls can be used by touch, not only with a mouse.
