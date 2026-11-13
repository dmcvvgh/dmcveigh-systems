-- Bulldog Bash: where the app saves scores, refs, brackets and stats.
-- Run once in Supabase: Dashboard > SQL Editor > New query > paste > Run.

-- One row holds the whole tournament as JSON (the same shape data.json had).
create table if not exists public.bulldog_bash (
  id         text primary key,                 -- the app uses '2026'
  data       jsonb not null default '{}'::jsonb,
  updated_at timestamptz not null default now()
);

-- Row Level Security on, with no policies: nobody can read or write this table
-- from a browser. Only the Streamlit server can, because it uses the secret key,
-- which bypasses RLS. The key lives in Streamlit secrets, never in the code.
alter table public.bulldog_bash enable row level security;
