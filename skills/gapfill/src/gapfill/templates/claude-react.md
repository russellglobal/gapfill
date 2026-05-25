# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Tech Stack

- React 19 + TypeScript (strict mode)
- Build tool: Vite
- State management: React Server Components preferred; useState/useReducer for client state
- Data validation: Zod
- Testing: Vitest + React Testing Library
- Styling: Tailwind CSS (no CSS Modules or styled-components)

## Component Conventions

- Use functional components only; never class components
- Default to Server Components; use "use client" only when interactivity is required
- Props defined with TypeScript interfaces, not type aliases
- Naming: PascalCase file names (UserProfile.tsx), camelCase export names
- Use named exports by default; reserved files (page.tsx, layout.tsx) use default exports
- Co-locate tests with components

## Data Fetching

- Use async Server Components for data loading; never use useEffect for data fetching
- Use Next.js fetch() with cache/revalidation options
- Do NOT use getServerSideProps or getStaticProps
- use() hook requires stable promise references; do NOT create inline (e.g., use(fetch('/api')))

## Build Commands

Run each command separately. Do not chain.

- Dev: `npm run dev`
- Build: `npm run build`
- Type check: `npx tsc --noEmit`
- Lint: `npm run lint`
- Test: `npm run test`
- Run single test: `npx vitest run -t "test name"`

## Security Rules

- Do NOT store secrets, API keys, or tokens in client-side code
- Do NOT use dangerouslySetInnerHTML
- Sanitize all user input before rendering

## Anti-Patterns

- Do NOT use useState/useEffect/useRef in Server Components
- Do NOT use inline styles; use Tailwind classes
- Do NOT manipulate the DOM directly; use refs
- Do NOT use `any` type; enable strict mode and fix type errors
- Do NOT create promises inline to pass to use()
- Do NOT skip type checking before committing
