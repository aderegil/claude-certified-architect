---
paths:
  - "**/*.test.py"
---

# Test File Conventions

- Use unittest.TestCase for all test classes
- Name test methods with test_ prefix describing the scenario: test_existing_product, test_empty_order
- One assertion per test method when possible
- Use setUp() for shared test fixtures, not repeated initialization
- Test both success and failure cases for every function
- Use assertIsNone for None checks, not assertEqual(result, None)
