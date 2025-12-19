# Legacy Refactor Prompt

Context:

- This is a legacy Django codebase.
- The goal is to improve readability, structure, and testability.
- No dependency upgrades unless explicitly requested.

Instructions:

- Keep behavior identical unless stated otherwise.
- Split large functions into smaller ones if it improves clarity.
- Rename variables/functions only if meaning is unclear.
- Remove dead code and obvious duplication.

Boundaries:

- Do NOT change public APIs.
- Do NOT change database schema unless asked.
- Do NOT introduce async code.

Output expectations:

- Clean, readable Python/Django code
- Minimal diff where possible
- Tests updated or added if logic changes
