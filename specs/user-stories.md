# User stories

IDs in brackets, like FR-1, are requirement IDs from `discovery/requirements.md` (Lab 3).

| Story | Cites | Requirement text (from Lab 3) | Priority in Lab 3 |
|---|---|---|---|
| S1 | FR-1 | log a food entry with calories, protein, fats, and carbs | Must |
| S1 | FR-3 | show daily totals of calories and each macro | Must |
| S2 | FR-7 | support a cut or bulk goal using food tracking | Should |
| S3 | FR-4 | log a workout (exercise and weight lifted) | Must |
| S3 | FR-11 | pull calories burned from the Apple Health app and Apple Watch | Could |
| S4 | FR-8 | store and compare progress photos over time | Could |

Privacy requirements NFR-1, NFR-2 and NFR-5 apply to S4 (body photos) and to S2 (body data).

**Not yet covered by a story:** FR-2 (record the time of each food entry) and the weight-lifted
part of FR-4.

Each story has acceptance criteria written as "WHEN ... THE SYSTEM SHALL ...". A feature is done
when every criterion for its story passes in the running app.

## S1 (FR-1, FR-3): Log a meal from a photo

As an active person, I want to track all the calories I am burning and consuming so that I can
more effectively cut or bulk weight.

**Acceptance criteria**

- **S1-AC1:** WHEN the user uploads an image of a meal THE SYSTEM SHALL understand what is on the
  plate and turn it into a lump sum of calories and nutrients.
- **S1-AC2:** AS A CHECK, the user SHALL be able to confirm whether the system got the plate
  correct and edit any options before the meal is catalogued on their plan.
- **S1-AC3:** WHEN the uploaded image is not a meal THE SYSTEM SHALL NOT log it as food, and SHALL
  display a message such as "Uh oh! I can't recognize your meal! Would you like me to add it to
  your progress photos?" with a choice to add it to progress photos or discard it.

## S2 (FR-7): Get a personalized fitness plan

As an active person, I want a plan made for my fitness journey so that I can cut or bulk weight
in a way that fits my body and goals.

**Acceptance criteria**

- **S2-AC1:** WHEN the user enrolls in the program THE SYSTEM SHALL collect their sex, age,
  height, weight, and desired training intensity, as part of setting their goals.
- **S2-AC2:** WHEN the user sets a goal THE SYSTEM SHALL accept a direction (cut weight or bulk
  weight), a target amount, and a target date.
- **S2-AC3:** WHEN the user requests a plan be made for their fitness journey THE SYSTEM SHALL
  create a customized plan based on all their biometrics and goals.
- **S2-AC5 (going wrong):** IF any required biometric (sex, age, height, weight, or training
  intensity) is missing THE SYSTEM SHALL NOT create the plan, and SHALL show which items are
  missing. WHEN all biometrics are entered THE SYSTEM SHALL show them back to the user to confirm
  before the goal is set.
- **S2-AC4:** WHEN the user changes their goal (amount or target date) or their biometrics change
  THE SYSTEM SHALL adjust the plan accordingly.

## S3 (FR-4, FR-11): Track calories burned (draft)

As an active person, I want my calories burned estimated for me so that my plan reflects what I
actually do each day.

**Acceptance criteria**

- **S3-AC1:** WHEN the user uploads an exercise activity THE SYSTEM SHALL estimate the calories
  burned based on the activity and the user's profile, so that the same activity can burn more
  for a larger person.
- **S3-AC2:** WHEN the user connects a health app THE SYSTEM SHALL synchronize total steps,
  calories, and related data and include them in the user's daily totals.
- **S3-AC3 (going wrong):** IF the health app sync fails THE SYSTEM SHALL tell the user the sync
  did not work and let them enter or upload their activity manually, so their daily totals are
  still complete.

## S4 (FR-8): Keep progress photos (draft)

As an active person, I want to store photos of my body over time so that I can compare and
analyze my progress.

**Acceptance criteria**

- **S4-AC1:** WHEN the user adds a photo to their progress photos (from S1-AC3 or directly) THE
  SYSTEM SHALL save it with its date.
- **S4-AC2:** WHEN the user views their progress photos THE SYSTEM SHALL let them compare photos
  from different dates.
- **S4-AC3 (going wrong):** IF the user has fewer than two progress photos THE SYSTEM SHALL NOT
  require a comparison, and SHALL show a message that a second photo is needed to compare.
  Progress photos SHALL be optional; the user can use the rest of the system without adding any.

*Your answer said the feature lets users "compare and analyze" progress. I only wrote the saving
and comparing parts. "Analyze" is not specified yet; see the open questions.*

## Open questions (for the student to answer)

- Which health app(s) will sync (Apple Health, Google Fit, others)? This affects S3-AC2.
- What are the training intensity levels (for example light, moderate, high)?
- What should happen if a goal is unrealistic or unsafe (for example a large loss in a few days)?
  S2-AC2 accepts any amount and date right now.
- What does "analyze" mean for progress photos: just side-by-side comparison, or does the AI
  describe changes? That decides whether S4 needs another criterion.
- Progress photos are sensitive body images. Who can see them, and can the user delete them?
- Are S3 and S4 part of the first version, or later? Lab 04 may only need S1 and S2.
