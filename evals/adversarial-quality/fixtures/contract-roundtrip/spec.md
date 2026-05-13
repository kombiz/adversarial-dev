# Recipe Box — Product Spec

## Product Overview

Recipe Box is a single-user recipe manager for home cooks. It lets users save recipes they've collected, search them by ingredient, and rate dishes after cooking. The product is warm, unfussy, and built for daily use — not a social network, not a cooking school.

**Who it's for:** people who cook 3-5 times a week and have recipes scattered across screenshots, bookmarks, and printouts.

**Core value:** one place that remembers what you cook and helps you find it again.

## Tech Stack

- React + Vite + TypeScript frontend
- Python + FastAPI backend
- SQLite database
- Tailwind CSS for styling

## Design Language

- **Palette:** warm cream background, deep terracotta accent, olive-green for ratings.
- **Typography:** a single serif for headings (Lora), a single sans for body (Inter).
- **Spacing:** generous — recipes breathe; this is not a dashboard.
- **Mood:** kitchen counter, not control panel. Photos, when present, are large.

## Feature List

- **Recipe capture** — paste a URL or type a recipe by hand. (Sprint 1)
  - As a user, I want to save a recipe so I don't lose it.
- **Recipe browse** — see all saved recipes as cards. (Sprint 1)
  - As a user, I want to scroll through what I've saved.
- **Ingredient search** — find recipes that use a specific ingredient. (Sprint 2)
  - As a user, I want to know what to make with the chicken I bought.
- **Rating** — rate a recipe 1-5 stars after cooking it. (Sprint 2)
  - As a user, I want to remember which recipes are keepers.
- **Cook count** — track how many times I've made each recipe. (Sprint 3)
  - As a user, I want to see my weeknight regulars surface.

## Sprint Plan

### Sprint 1 — Capture and Browse
Build the data model and the two-screen MVP: save a recipe, see the list.

### Sprint 2 — Find and Rate
Make recipes useful: search by ingredient, rate after cooking.

### Sprint 3 — Memory
Track cook counts and surface frequently-made recipes.
