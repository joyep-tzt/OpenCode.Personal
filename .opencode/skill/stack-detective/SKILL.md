---
name: stack-detective
description: Detect tech stack from configuration files with confidence scoring
license: MIT
compatibility: opencode
metadata:
  audience: developers
  workflow: testing
---

## What I Do

Detect the technology stack of TypeScript/JavaScript projects by analyzing configuration files. Provides confidence scores and detailed reasoning.

## Detection Rules (Priority Order)

**Next.js**: `next.config.js/ts/mjs` exists (Confidence 95-100%)
**Angular**: `angular.json` exists (Confidence 95-100%)
**Vue/Nuxt**: `nuxt.config.ts` or `src/App.vue` (Confidence 90-95%)
**React + Vite**: `vite.config.ts` with React plugin (Confidence 85-95%)
**Express**: `src/app.ts` or `src/server.ts` (Confidence 80-90%)
**Generic TypeScript**: Fallback (Confidence 60-75%)

## Output Format

```json
{
  "framework": "React",
  "version": "18.2.0",
  "buildTool": "Vite",
  "testFramework": "Playwright",
  "language": "TypeScript",
  "confidence": 95,
  "reasoning": ["Found vite.config.ts", "Found react in package.json"]
}
```

## Usage

Invoke this skill to detect the stack before loading specialist skills.
