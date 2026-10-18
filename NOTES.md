# Jerison_Lang — Notes & Journal

Personal working notes for Jerison_Lang. This is where I document what I learn, decisions I make, problems I encounter, and ideas to revisit.

## How to Use

- Add a new entry for each work session, newest first.
- Keep entries concise, except when explaining concepts worth understanding in depth.
- Record useful explanations, decisions, mistakes, and unresolved questions.
- Add every new entry to the table of contents.
- Use alerts when they add value, not just to decorate the journal.

## Alert Guide

GitHub supports colored alerts that help important information stand out. Use them consistently throughout the journal.

| Alert | Color | When to Use It |
|---|---|---|
| `NOTE` | Blue | Useful context, background information, or the focus of a session. |
| `TIP` | Green | Helpful techniques, shortcuts, and good practices. |
| `IMPORTANT` | Purple | Major lessons, architectural decisions, and important breakthroughs. |
| `WARNING` | Yellow | Unresolved bugs, confusing behavior, and potential problems that need investigation. |
| `CAUTION` | Red | Serious risks, such as destructive operations or potential data loss. |

### Alert Guidelines

- Don't force all five alerts into every entry. Use only the ones that are relevant.
- Keep alerts short and focused on the information that deserves attention.
- Use colors consistently so they retain their meaning as the journal grows.
- Reserve `CAUTION` for serious risks, not ordinary bugs or questions.
- Use `IMPORTANT` sparingly so major takeaways stand out.

## Entry Template

Copy this template for each new work session. Remove sections you don't need.

    ---

    # YYYY-MM-DD — Topic

    > [!NOTE]
    > **Focus:** Brief description of what you worked on.

    ## What I Worked On
    - 

    ## What I Learned
    - **Concept:** Explanation in your own words, with examples when useful.

    ## Decisions
    - 

    ## Next Steps
    - 

    ---

## Table of Contents

- [2026-10-17 — Project Kickoff](#2026-10-17--project-kickoff)

---

# 2026-10-17 — Project Kickoff

> [!NOTE]
> **Focus:** Setting up the development workflow and building the initial Python CLI harness.

## What I Worked On

- Set up Git, tests, linting, and CI.
- Drafted the main README and project roadmap.
- Built the Python CLI harness with argument validation, file checks, and error handling.
- Added modules for shared constants and exit codes.
- Implemented binary file reading with explicit UTF-8 decoding.

## What I Learned

- **Interpreter vs. compiler:** An interpreter executes code, while a compiler translates it into another form before execution. Some implementations combine both approaches.
- **First-class functions:** Functions can be stored in variables, passed as arguments, and returned from other functions, just like other values.
- **JIT compilation:** Just-in-time compilation translates code into machine code at runtime, often to improve performance.
- **Bytes vs. strings:** `str(b'hi')` produces `"b'hi'"`, not `"hi"`. Use `.decode()` to convert bytes into text.
- **Python's byte representation:** The `b` prefix and escape sequences show Python's representation of byte data, not necessarily the literal characters in the original file.
- **Exit codes:** The `sysexits.h` conventions define `64` for command-line usage errors and `66` for input errors.
- **`sys.exit()`:** Raises `SystemExit` and stops normal execution, so no additional `return` is needed afterward.
- **Error handling:** The entry point should validate command-line arguments and input files. Internal functions should focus on their own responsibilities.
- **File reading:** Reading bytes and decoding explicitly with UTF-8 strict mode gives control over invalid text.

> [!IMPORTANT]
> The CLI harness should translate expected input errors into clear messages and exit codes rather than exposing raw Python tracebacks.

> [!TIP]
> Read source files as bytes and decode explicitly when you need predictable control over character encoding.

## Decisions

- Keep the development journal separate from the main README.
- Use named exit-code constants: `64` for usage errors and `66` for input errors.
- Read source files as bytes and decode explicitly using UTF-8 strict mode.
- Check file existence before validating the file extension.
- Keep internal functions focused and assume input has already been validated.

> [!WARNING]
> Scanner error handling is not finalized. Decide how errors should be recorded and reported before expanding the scanner.

## Next Steps

- Implement the tree-walking interpreter.
- Decide how scanner errors should be recorded and reported.
- Expand the interpreter as new language features are added.

---