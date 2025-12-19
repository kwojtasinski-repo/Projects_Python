# Testing Strategy Prompt

Context:

- Django project with legacy roots.
- Tests are used as a safety net for refactors and upgrades.

Testing rules:

- Use Django TestCase for DB-related tests.
- Use unittest.mock.patch for HTTP and external services.
- No real network calls in tests.
- Prefer explicit assertions over clever ones.

Focus on:

- Scrapers
- Views
- Model behavior
- Edge cases (empty input, errors)

Avoid:

- Over-mocking internals
- Snapshot-style tests
- Testing Django internals
