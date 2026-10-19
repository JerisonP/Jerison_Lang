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
- [2026-10-18 — Scanner First Pass](#2026-10-18--scanner-first-pass)
- [2026-10-19 — Scanner First Pass](#2026-10-19--finishing-the-scanner)

Writing

# 2026-10-19 — Finishing the Scanner

> \[\!NOTE\] **Focus:** Finished identifier and keyword scanning, wrote tests, and refactored the test suite to share a common base class.

## What I Worked On

- Finished identifier scanning and keyword recognition.
- Converted Bob's Java `keywords` HashMap into a Python dictionary mapping keywords to their `TokenType`.
- Added tests for keywords and identifiers, covering singles, pairs, sequences, and edge cases.
- Created a shared `BaseScannerTest` class with four test methods, allowing each token group to provide its own test cases.
- Used `pytest_generate_tests` to generate tests from each subclass's `cases` dictionary.

## What I Learned

### Pytest and Test Organization

- **Base test classes:** Pytest doesn't collect a class whose name doesn't start with `Test` on its own. However, its test methods are inherited and run by subclasses whose names start with `Test`.
- **Why****`@pytest.mark.parametrize`****can't use subclass-specific data:** The decorator runs when the base class is defined, before any subclasses exist. It therefore can't access their test arrays.
- **The****`pytest_generate_tests`****hook:** This module-level function lets pytest generate test cases dynamically during collection, before any tests execute.
- **The****`metafunc`****object:** Pytest passes this object to the hook. `metafunc.cls` identifies the class being collected, while `metafunc.function.__name__` gives the test method's name. Calling `metafunc.parametrize()` creates a separate test for each case.
- **Test collection:** Pytest first discovers tests and generates all parameterized cases, then runs them.
- **Class-specific fixtures:** A fixture can use `request.cls` to access attributes on the test class it's serving. This provides another way to give inherited tests class-specific data.
- **Readable test IDs:** Parameterized test IDs include the case name, making failures easier to identify. For example, `TestKeywordTokens::test_single[orchid-expected0]` tells me which test group, method, and case failed.

### Scanner Behavior

- **Maximal munch:** The scanner reads the entire word before checking whether it's a keyword. For example, `orchid` becomes one identifier, not `or` followed by `chid`.
- **Case-sensitive keywords:** `And` and `TRUE` are identifiers, not keywords, because keyword matching is case-sensitive.
- **Keyword lookup with a default:** Using `keywords.get(text, T.IDENTIFIER)` means that words not found in the keyword dictionary automatically become identifiers.

## Decisions

> \[\!IMPORTANT\] These decisions affect both the scanner and the design of my future language.

- **Test structure:** Keep one `BaseScannerTest` with four shared test methods and a `cases` dictionary for each token group.

## Next Steps

- [ ]Investigate the error-handling flow.
- [ ]Start the _Representing Code_ chapter of _Crafting Interpreters_.

---

# 2026-10-18 — Scanner First Pass

> [!NOTE]
> **Focus:** Build the first functional scanner and a comprehensive pytest suite covering single-character tokens, operators, comments, whitespace, strings, and numbers.

## What I Worked On

- Restructured the scanner following *Crafting Interpreters*: `scan_tokens()` → `scan_token()` → `add_token()`.
- Added scanning helpers: `advance()`, `peek()`, `peek_next()`, and `match()`.
- Implemented single-character tokens, paired operators (`!=`, `==`, `<=`, `>=`), comments, whitespace, strings, and numbers.
- Expanded tests to compare complete `Token(...)` objects, including lexemes, literals, and line numbers.
- Grouped tests by token family, covering individual tokens, pairs, sequences, and edge cases.
- Moved `run()`, `run_file()`, and `run_prompt()` into `runners.py` and separated error reporting into its own module.

## What I Learned

### Python and Object Behavior

- **`__eq__()` and list comparison:** Python compares lists element by element using each element's `__eq__()` method. Without a suitable implementation, two tokens with identical fields won't necessarily compare as equal.
- **`__str__()` vs. `__repr__()`:** `print(token)` uses `__str__()`, while printing a list uses `__repr__()` for each element.
- **Default arguments replace overloading:** Bob overloads `addToken()` in Java because Java doesn't support default arguments in the same way Python does. In Python, `literal: object = None` provides the same convenience.
- **Explicit instance access:** Python methods use `self.` to access instance attributes and other methods. Helpers that don't need instance state can be defined at the module level.
- **Read-only collection interfaces:** `Mapping`, `Sequence`, and `Set` from `collections.abc` describe the interfaces a function expects. They communicate intended usage to callers and type checkers but don't prevent modifications at runtime.

### Scanner Behavior

- **Lox strings have no escape sequences:** `\n` inside a string represents two literal characters, not a newline. Actual line breaks are allowed inside strings and must increment the line counter.
- **EOF sentinel:** Bob uses `'\0'` to represent the end of the source. Returning `"\0"` from `peek()` at the end prevents out-of-bounds reads and simplifies loops for comments, strings, and numbers.

### Error Handling

- **Separate detection from reporting:** The code that detects an error and the code that reports it should have separate responsibilities. Keeping functions focused makes the code easier to understand and maintain.

## Decisions

> [!IMPORTANT]
> These decisions define the scanner's behavior and testing approach.

- **Token types use enums** for readable names and to help catch invalid token types instead of relying on string comparisons.
- **`peek()` returns `"\0"` at EOF** instead of raising `IndexError`, centralizing boundary handling.
- **Number syntax follows Lox:** `.123` and `123.` are not valid number literals.
- **All numeric literals are floats** because Lox has a single number type.
- **Tests compare complete tokens**, including type, lexeme, literal, and line number, so line tracking is tested too.

## Issues to Investigate

> [!WARNING]
> A few bugs remain, and the error-handling flow needs further investigation.

- The end-to-end error-handling flow is still unclear, and some leftover error code will matter later.

## Next Steps

- [x] Add identifiers, keywords, and the missing `TRUE` token type.
- [x] Extract repeated test-method logic into a shared helper.
- [ ] Investigate the error-handling flow.
- [x] Change `peek()` (and `peek_next()`) to return `None` at end of file instead of `"\0"`. It's more Pythonic, and there's no Java `charAt` constraint forcing a zero char. Update the return type to `str | None`.

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

- []Implement the tree-walking interpreter.
- [x]Decide how scanner errors should be recorded and reported.
- Expand the interpreter as new language features are added.

---