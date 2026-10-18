# Future Language Notes

## What I Want
- Static types
- Type deduction (inference)
- Compiled language
- Robust error messages that show the line number and exactly where the syntax error is

## Advice
- **Error reporting:** Make a dedicated error class (something like `ErrorReporter`) instead of loose functions, so error state and reporting live in one place.
- **Token locations:** Some implementations store a token's location as two numbers: the offset from the start of the source file to the start of the lexeme, and the lexeme's length. The scanner already tracks both, so there's no extra cost. The offset can be turned into a line and column later by looking back at the source and counting the newlines before it. That's slow, but it only happens when an error actually needs to be shown, which is rare.

