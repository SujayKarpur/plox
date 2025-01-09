# plox
python implementation of the [Lox](https://craftinginterpreters.com/the-lox-language.html) programming language 

## usage
```sh
$ plox [script]
```

## About 
Lox (from the book Crafting Interpreters) is a dynamically typed scripting language designed to be easy to understand and implement.  

This project is a treewalk interpreter for Lox, with a handcrafted lexer and recursive descent parser.  

## References
[Crafting Interpreters](https://craftinginterpreters.com/)  
[Compilers Principles, Techniques, and Tools](https://www.amazon.in/Compilers-2e-Aho/dp/9332518661/ref=sr_1_1?crid=102BX5D3670H2&dib=eyJ2IjoiMSJ9.sZDFB1B_6Fylm6ggOLMgeQ.kPJtxpRyr7W0IIaa4tEUHgAa2MJPrf35HMjO2Ald03I&dib_tag=se&keywords=compileres&qid=1735748598&sprefix=compil%2Caps%2C737&sr=8-1)  
[PLY documentation](https://www.dabeaz.com/ply/ply.html)  

## Current Status
plox takes in input from the user (either line by line or as a single script) and prints the array of tokens produced after lexing, along with any lexer errors.
If the program consists of only an expression, the expression is parsed and evaluated.

## To Do
- [ ] Improve Lexer error handling (print line containing error and show column)
- [ ] Handle syntax errors
- [ ] Handle runtime errors
- [ ] Add support for ternary operator
- [ ] Add support for non-expression statements
- [ ] Add documentation and usage instructions
- [ ] Add constructs for functions and classes
