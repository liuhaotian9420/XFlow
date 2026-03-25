# Reporting Format

This file indexes the reporting guidance already described in `SKILL.md`.

## Result reporting

Always report results by **severity** and by **validation layer**.

### Severity levels
- **fatal**: the skill is unusable or unverifiable in a meaningful way
- **major**: the skill behavior contradicts its description or fails the main contract
- **minor**: non-blocking structural or clarity problems
- **warning**: reduced confidence, skipped checks, fallback to generated fixtures, or environment limitations

### Required report sections
For each skill, report:

1. **Structural validation**
2. **Smoke validation**
3. **Contract validation**
4. **Negative-path validation**
5. **Fixture/mocking notes**
6. **Skipped checks and why**

### Output style
Separate:
- must-fix errors
- warnings
- skipped items
- confidence notes

Do not collapse everything into a single PASS/FAIL unless the user explicitly wants a terse summary.

## Confidence model

Use confidence language based on how strong the verification really was.

### High confidence
Use when:
- the skill provided concrete fixtures or tests
- the verifier executed a real minimal path
- outputs were verified
- at least one negative-path test was checked

### Medium confidence
Use when:
- the skill ran successfully
- some fixtures were auto-generated
- outputs were partly checked
- some behaviors were inferred rather than explicit

### Low confidence
Use when:
- only structural checks ran
- runtime checks were skipped
- the skill was too vague to construct a meaningful contract
- live dependency boundaries prevented testing
