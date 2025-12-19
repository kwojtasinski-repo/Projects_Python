# Copilot Instructions

This repository contains multiple Python projects:
- Django web applications
- Data processing and algorithmic code (e.g. k-NN, data analysis, experiments)

## High-level goals

- First: refactor and stabilize existing code
- Second: upgrade dependencies and framework versions
- Preserve existing behavior unless explicitly stated otherwise

## General constraints

- Python 3.11+
- Prefer standard library and well-known packages
- Avoid unnecessary abstractions
- No cloud-specific assumptions by default

## Django-specific constraints

- Django 5.x target
- Synchronous Django only (no async views, no DRF)
- SQLite for local development and tests
- Views should remain thin and readable

## Data processing / algorithmic code

- Focus on correctness and clarity over performance unless stated otherwise
- Prefer explicit implementations over overly optimized ones
- Avoid premature optimization
- Clearly separate data loading, processing, and evaluation

## Coding principles

- Prefer small, explicit changes
- Avoid speculative rewrites
- Avoid introducing new dependencies unless justified
- Keep logic readable and testable

## Testing

- Tests are mandatory for refactored code
- Django: use Django TestCase and unittest.mock
- Data/algorithms: use unittest or pytest-style assertions
- No external HTTP calls in tests

## Always do

- Respect existing architecture decisions
- Ask before large or cross-cutting refactors
- Explain *why* a change is needed, not only *what*
