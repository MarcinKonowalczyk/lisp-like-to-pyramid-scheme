# psll-lang

[![Build Status](https://travis-ci.org/MarcinKonowalczyk/psll-lang.svg?branch=master)](https://travis-ci.org/MarcinKonowalczyk/psll-lang) [![Coverage Status](https://coveralls.io/repos/github/MarcinKonowalczyk/psll-lang/badge.svg?branch=master)](https://coveralls.io/github/MarcinKonowalczyk/psll-lang?branch=master)

A lisp-like language which compiles to [pyramid scheme](https://github.com/ConorOBrien-Foxx/Pyramid-Scheme) (**p**yramid **s**cheme **l**isp-**l**ike syntax, aka `psll`).

## Installation

Make  `ll2pyra` executable:

```
chmod u+x ll2pyra.py
```
or use the `psll` bash script (which you might want to edit to make it point to the correct files) which compiles and runs a program.

## Use

Read the help:
```
./ll2pyra.py -h
```

Verbose output and save to the file:
```
./ll2pyra.py  array_sum_golf.psll -v -o
```

## Examples

The following is an example lisp-like pyramid scheme which counts the number of input arguments it gets, and then prints it out to the command line. The syntax supports `//` comments and newlines, as well as (almost) random additions of whitespace.

N.b. C# highlighting seems to look fine for most intensions and purposes (at lest in vscode). Lisp-highlighting somehow looks worse in my opinion.

```cs
// Count the number of input arguments

(set nil (arg 99)) // Make nil

// Count the number of input arguments - n
(set nargin 0)
(do
    cond
    (
        (set nargin (+ nargin 1))
        (set cond (! (= (arg nargin) nil)))
    )
)
(set nargin (- nargin 1))

// Print 'nargin: #'
((out (chr 110) (chr 97)) (out (chr 114) (chr 103)))
((out (chr 105) (chr 110)) (out (chr 58) (chr 32)))
(out nargin)
```

It can be compiled and run as follows:

```
./ll2pyra.py nargin_counter.psll -o -f
ruby ./Pyramid-Scheme/pyra.rb nargin_counter.pyra 4 3 5 2 4
```
The output is `nargin: 5`

## Finer points

### Bracket expansion
Psll supports a few bits of syntactic sugar, to make writing pyramid schemes easier. A bracket with multiple subtrees will get automatically split into multiple size-2 subtrees which will, in turn, get prepended with the empty string, as described above. Hence, the following psll code:

```cs
(
  (out 1) (out 2) (out 3) (out 4) (out 5)
)
```

will get interpreted as:

```cs
(
  (
    ( // First pair
      (out 1) (out 2)
    )
    ( // Second pair
      (out 3) (out 4)
    )
  ) // One left
  (out 5)
)
```
The elements are taken from the list pairwise, and put into sub-lists recursively, until the root list has length of 2 or less. Because of order of subtree evaluation in pyramid scheme, this preserves the execution order. Note that arbitrary indentation, and mid-line comments are allowed.

This feature is useful, for example, for keeping tidy the body of a for-loop:

```cs
(set N 100)
(set j 0)
(loop (! (= j N)) (
  // Do dome work...
  (out j (chr 10))
  // Do some more work...
(set (j (+ j 1)))
))
```

### Strings

In pyramid scheme, the strings have to be built manually such that the string hello is:

```cs
(set a (+ (+ (+ (+ (chr 72) (chr 101)) (chr 108)) (chr 108)) (chr 111)))
```

Psll expands a string literal into such construct, so its enough to write:

```cs
(set a "Hello")
```

## ToDo's

This is not a real-purpose language. In this section the 'optimisation' refers to obtaining nicer-looking and more compact pyramids, *not* not efficient code.

- [ ] More compiler optimisations
  - [x] Subtree packing <s><- !!! (work on this next!)</s>
  - [ ] Left/right subnode packing
    - [ ] Support for left/right singleton children
  - [ ] Packing with null-tree snakes
  - [ ] Variable name optimisation
    - [ ] Automatic shortening
    - [x] Packing into the upper parts of the triangles too
- [ ] Pre-compile code optimisations?? <s>Not sure what that would be though, tbh.</s>
  - [x] Move string expansion to pre-proc
  - [ ] Move binary bracket expansion to pre-proc
  - [ ] Move null-trees to pre-proc <s><- (work on this next, because it's broken...)</s>
- [x] Syntactic sugar?
  - [x] Simpler writing of strings
  - [x] Simpler writing of nested nil pyramids
- [x] Compiler optimisation takes a long time
- [ ] Easier to use installation. Maybe a make-script which makes a symlink in the correct place...?
- [ ] Improve test coverage
  - [x] Make the coverage count only the tests for that file

## Bugs
- [x] `compact` option breaks when `N`th triangle is wider than all the `1..N-1`s.
  - [ ] `compact` option does nothing
- [ ] Strings do not support escape characters (And maybe they never will! Ha! They're just sugar anyway...)
