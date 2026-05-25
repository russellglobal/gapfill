# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

{{project_name}} - AI-assisted development project.

## Development Principles

- Keep changes minimal and focused
- Do not add features beyond what was requested
- Verify before committing
- Follow existing patterns and conventions
- Do not use composite commands (`&&`, `;`, `||`) - run commands separately so each can be individually approved
- All documentation, comments, and commit messages should be in Chinese unless the project is public-facing

## Branch Workflow

- `main` is protected; do not push directly
- Develop all new features on `feature/<name>` branches
- Merge to `main` via pull request after tests pass

## Build Commands

Run each command separately. Do not chain.

- Git status: `git status`
- Git diff: `git diff`
- Git log: `git log --oneline -10`

## Security Rules

- Do not expose secrets, API keys, or credentials in code or comments
- Do not run destructive commands (`rm -rf`, `git reset --hard`) without explicit user confirmation
- Do not bypass git hooks (`--no-verify`, `--no-gpg-sign`)
