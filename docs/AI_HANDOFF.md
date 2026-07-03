# AROS AI Handoff

This file allows ChatGPT, Claude, Gemini, Cursor or any future AI assistant to resume AROS development consistently.

## Project

AROS — AI Research Operating System

AROS is an AI-native research platform for academic research, finance, economics, public policy, corporate governance and knowledge management.

## Architecture Rule

Do not redesign the architecture unless explicitly instructed.

Preserve:

Source
↓
Connector
↓
Knowledge Object
↓
Repository
↓
Future AI Layer

## Current Verified Baseline

5eb694b Add OpenAlex academic connector

## Latest Completed Milestone

The first complete local PDF research pipeline was built and verified.

Pipeline:

Local PDF
↓
Reader
↓
Knowledge Object
↓
SQLite Repository

## Important Development Preference

Documentation must be updated alongside meaningful code milestones so that any AI platform can continue from the same project state.

## Cross-AI Continuity Principle

AROS itself, through the Research-OS repository and docs folder, should be the authoritative source of project knowledge.

Do not rely only on memory inside ChatGPT, Claude or Gemini.

## Next Objective

OpenAlex academic connector verified. Next objective is connector intelligence improvement while preserving the Knowledge Object and Repository flow.

Do not over-engineer.
Do not rewrite verified modules.
Audit before changing existing code.
