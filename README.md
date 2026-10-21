# Jerison_Lang

My own take on Lox, the language from Robert Nystrom's
[Crafting Interpreters](https://craftinginterpreters.com/), built in Python.
It's a tree-walking interpreter based on the book's Java version, jlox.

## About the project

### What is an interpreter?

An interpreter is a program that runs source code directly, reading and
executing it on the fly instead of compiling it to machine code first.

A **tree-walking interpreter** parses the source into a tree that represents
the program's structure, then walks that tree node by node and evaluates
each piece as it goes.

### Goals

- Build the core interpreter: scanner, parser, and evaluator.
- Add language features step by step once the core works.
- Learn testing and CI along the way.

## How it works

The interpreter runs source code in three stages.

### 1. Scanning

Reads the source file and breaks it into **tokens**, the smallest meaningful
pieces of the language, such as numbers, names, operators, and keywords.

### 2. Parsing

Takes the stream of tokens and arranges them into a **syntax tree** that
shows how the pieces of code fit together, for example which operations
happen first.

### 3. Evaluating

Walks the syntax tree and executes each node, all at runtime. This is where
the program actually does things: calculating values, storing variables,
and printing output.

## Language features

Features will be added gradually once the core stages are working.

- [ ] Expressions and arithmetic
- [ ] Variables
- [ ] Control flow (`if`, `while`, `for`)
- [ ] Functions
- [ ] Classes

## Getting started

## Progress log
