# User stories

Each story has acceptance criteria written as "WHEN ... THE SYSTEM SHALL ...". A feature is done
when every criterion for its story passes in the running app.

## S1 (FR-1): Log a meal from a photo

As an active person, I want to track all the calories I am burning and consuming so that I can
more effectively cut or bulk weight.

**Acceptance criteria**

- **S1-AC1:** WHEN the user uploads an image of a meal THE SYSTEM SHALL understand what is on the
  plate and turn it into a lump sum of calories and nutrients.
- **S1-AC2:** AS A CHECK, the user SHALL be able to confirm whether the system got the plate
  correct and edit any options before the meal is catalogued on their plan.

## S2 (FR-2): Get a personalized fitness plan

As an active person, I want a plan made for my fitness journey so that I can cut or bulk weight
in a way that fits my body and goals.

**Acceptance criteria**

- **S2-AC1:** WHEN the user requests a plan be made for their fitness journey THE SYSTEM SHALL
  create a customized plan based on all biometrics and goals.

## Open questions (for the student to answer)

These are gaps I noticed. None are decided yet.

- Which biometrics count as "all biometrics" (for example age, height, weight, sex, activity
  level)? S2-AC1 can't be tested until this list is fixed.
- What do the goals look like (cut, bulk, maintain, target weight, date)?
- "Calories I am burning": does the system estimate this from the plan and biometrics, or does the
  user enter workouts? Neither story covers it yet.
- What happens if the photo is not a meal, or the system is unsure? (S1-AC2 covers wrong guesses
  but not "no food found".)
