# Future Language Notes

## what i want:
- static types
- robust error messaging showing the line number and where the syntax error is
- compiled language
- type deduction 

## advice:
- when dealing with errors you should probably make an error class ErrorReporter or something like that
- some token implementations store the location as two numbers: the offset from the beginning of the source file to the beginning f the lexeme, and the length of the lexeme. The scanner needs to know these anyway, so there's no overhead to calculate them. this offset can be converted to line and column positions later by looking back at the source file and counting the preceding newlines. we only do this when we need to actually display a line and column to the user which is slow but again only done a hand full of times

