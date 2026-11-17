# Plan: add a "status" field and a status filter

Final plan for Lab 2 Part C. Everything stays in `problem-tracker/index.html`, with no libraries
and localStorage only, as the project's CLAUDE.md requires.

## Goal

Each problem has a status of **open**, **in progress**, or **solved**, and the page can be
filtered to show only one status.

## Change requested to the first draft

The first draft filtered only the list view. Requested change: **the status filter must also
apply to the corkboard view**, hiding sticky notes that do not match.

## Steps

1. **Data.** Every new problem is saved with `status: "open"`. Problems saved before this change
   have no status, so a small helper, `getStatus(problem)`, treats a missing or unknown status as
   "open". Old saved data is never rewritten or lost.

2. **Changing a status.** Each problem gets a small dropdown (Open / In progress / Solved):
   - in the list view, on each problem card;
   - in the corkboard view, at the bottom of each sticky note. Clicking the dropdown must not
     start dragging the note.
   Choosing a value saves it to localStorage straight away and redraws the page.

3. **Filtering.** A "Show" dropdown is added to the toolbar: All / Open / In progress / Solved.
   - The filter is applied once, in `render()`, together with the existing title search, so a
     problem is shown only if it matches both.
   - The filtered result is passed to both the list and the corkboard (the requested change).
   - On the corkboard, filtering only hides notes. Saved note positions are not changed.
   - The filter is not remembered between visits, so problems never look "missing" on the next
     visit.

4. **Empty results.** If problems exist but none match the search and filter, show a message
   instead of a blank area.

5. **Phone check.** The new dropdowns must wrap onto their own line on a narrow screen (about
   375px) and be large enough to tap.

## How to check it

1. Add three problems. Each should start as "Open".
2. Change one to "In progress" and one to "Solved". Refresh the page: the statuses are kept.
3. Set "Show" to "Solved": only the solved problem appears in the list.
4. Switch to Corkboard with the filter still on: only the solved sticky note appears.
5. Set "Show" back to "All": every note returns to where it was.
6. On the corkboard, change a status with the note's dropdown, and drag a note. Both still work.
7. Narrow the window to phone width and repeat steps 3 and 4.
