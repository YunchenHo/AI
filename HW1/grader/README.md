# Grader

## Released Grading

```shell
uv run grader/grade.py
```

## Notes

- The grader is driven by `grader/spec.py`.
- The released repo includes only the public checks.
- The released grader should be interpreted as a **public-only local checker**. It is useful for catching import errors, interface errors, and public-case mistakes before submission.
- Hidden private tests are not included in this repository, so the local grader output is **not** your final implementation score.
- TA-only private cases and expected values should stay outside the student-facing `grader/` directory.
