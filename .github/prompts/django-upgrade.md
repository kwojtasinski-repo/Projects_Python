# Django Upgrade Prompt

Context:

- The codebase has already been refactored and stabilized.
- Tests are present and passing.

Goal:

- Upgrade Django and related dependencies safely.

Instructions:

- Upgrade incrementally (major versions step by step if needed).
- Follow official Django deprecation paths.
- Update settings.py according to modern Django best practices.
- Fix warnings before moving forward.

Boundaries:

- Do NOT rewrite architecture.
- Do NOT replace Django with other frameworks.
- Do NOT remove features unless required by breaking changes.

Output expectations:

- Clear explanation of breaking changes
- Updated code with passing tests
- Notes on deprecated patterns that were replaced
