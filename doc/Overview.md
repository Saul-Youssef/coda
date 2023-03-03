# Overview

   Coda is an axiomatic foundational framework attempting to capture mathematics and computing at once.  This 
is the natural endpoint of a line of thinking that I have pursued over a number of years and over several 
software implementations (particularly "egg" and "coda-classic").  This notebook is a tutorial introducing 
the basic concepts including an implementation of Coda in python.  

## Foundation 

Any system of reasoning must necessarily start with undefined terms which are understood before even a first definition. In Coda, we only assume that the concept of a **finite sequence** is understood without explanation. That is, we will freely speak of empty sequences, concatenation of sequences, pairs, and functions (thought of as a collection of pairs) without further explanation.

Note that we do not assume predicate logic as in standard foundations and we don't take "type" to be a foundational undefined term as with other foundations.  Coda, as we will see, has it's own internal logic and it has a naturally occuring internal concept 
of a "type" without the need to assume this in the foundations.

Given that finite sequences are understood, the foundational concepts of Coda are,

* A **data** is a finite sequence of **codas**;
* A **coda** is a pair of **data**.

Thus, the empty sequence "()" is a valid data, an, therefore, a pair of empty sequences "(:)" is a valid coda.  We indicate the pairing of of data to make a coda with the colon character.

Given data and coda as defined,

* A **definition** is a partial function from coda to data; 
* A **context** is a finite sequence of definitions with disjoint domains. 

Given a partial function f from coda to data, we can extend f to a function from data to data by defining 

* f(c<sub>1</sub> c<sub>2</sub>...c<sub>n</sub>) = f(c<sub>1</sub>)+f(c<sub>2</sub>)+...+f(c<sub>n</sub>) 

where c<sub>1</sub>...c<sub>n</sub> are codas, + is concatenation of data as sequences and where f(c) is taken to be the identity if c is not in the domain of f.  Given a context f<sub>1</sub>,f<sub>2</sub>,...,f<sub>n</sub>, we can define a corresponding equivalence relation 
on data by letting 

* A + B = f(A) + B = A + f(B)

where A and B are data and where f is any of f<sub>1</sub>,...,f<sub>n</sub>, extended to a function from data to data as indicated. 

Coda has only one axiom.  It is the axiom that defines what constitutes a valid definition.
>
>**Axiom of Definition**: Suppose f<sub>1</sub>,...,f<sub>n</sub> is a context and f is a partial function 
from coda to data.  If the domain of f is disjoint with the domain of each f<sub>1</sub>,...,f<sub>n</sub>, then f is called a *valid definition* and 
f<sub>1</sub>,...,f<sub>n</sub>,f is a *valid context*.
>

Note that since the partial functions of a context must have disjoint domains, any 
particular coda can be in the domain of at most one definition.  Codas where their 
corresponding definition is the identity are particularly important.  These are called 
**atoms**.  Data containing at least one atom in it's sequence is called **atomic**.  

Of course, codas may happen to have no corresponding definition in a particular context. Such codas are called **undecided**.  Undecided data function as the Coda version of 
"variables."

## Language 

  In standard foundations and predicate logic, recall that one needs to have 
syntax rules to exclude meaningless expressions like "&forall; x (y:z) &forall; &forall; &exist;". Given a syntax, one introduces axioms which are meant to capture the intuitive meaning of 
symbols like &forall;.  In Coda, the situation is quite different because the language itself 
is a definition like any other.  It is merely a partial function acting on codas of 
the form ({source code} A : B) where A and B are data as defined above.  This means that the 
syntax and meaning of Coda language expressions is already defined without foundational syntax 
rules or axioms defining valid operations.  The Coda language iself is quite simple.  Essentially, it is blank spaces (to indicate data concatenation), colons (to indicate forming 
coda from two data), and parenthesis to group operations. There is also no such thing as a 
syntax error.  The Coda language has the amusing property that every byte string is valid source code. 

## Data, Logic, Godel phenomena

   As we will see in other tutorials, familiar concepts such as functions, variables, categories, morphisms, theorems and proofs naturally simply as data with special properties.  For instance, data C is a **category** if C : (X Y) = C : (C:X) (C:Y) for all data X, Y, and data M is a **morphism in category C** if M commutes with C in the sense that C:M:X = M:C:X for all X.  Since the foundational concept of Coda is a sequence, it is typically easier to define familiar structures via equivalent sequential versions.  So, rather than thinking of an abelian group G as a set with a binary operator, one has data (G:X) where sum G:X Y = sum G:Y X.  Similarly, a partially ordered set P is more conveniently defined as data (P:X) with a sort operation, rather than as a set with a partial order relation.  

   One of the roles of classical Logic is to provide a coarse but useful classification of all classical propositions: all propositions are meant to be either **true** or **false**.  In Coda, however, notice that since everything is data, all questions are, roughly speaking, of the form "Is data A equal to data B?"  But, since equality as defined above is also just another definition in context, both questions, and the answers to questions are data.  This means that the analogue of "Logic" in Coda should be the coarsest useful classification of data.  There indeed is such a classification because of the built-in duality between data and coda, where () is the prototype for "true data" and the atom (:) is the prototype for false data. In general, data is either

* Empty if it is data equal to the empty sequence).
* Atomic data (as defined above).
* Undecided data (data which is neither empty nor atomic).

This gives a multi-valued logic where empty/atomic/undecided data is
defined to be true/false/undecided respectively.  It is easy 
to show that this classifies data in the sense that true data cannot be equal to 
false data and true data remains true independent of adding new definitions to 
context and false data remains false independent of new definitions.  Undecided data,
on the other hand, may become true or may become false when new definitions are 
added.  In that sense, "true" and "false" are permanent properties of data.  

   The Coda view of logic may seem disorienting at first, but it is easy to get used to and it comes with perhaps unexpected benefits.  The simplest form of "undecided" data is simply data like (foo:bar) which is, in effect, a place-holder for a future possible definition.  It is, in other words, a "variable."  More generally, if you want to know 
if data A and B are equal, the data A=B gives the "obstruction."  It tells you what prevents A and B from being equal.  In that sense, the author is hoping that this kind of logic will bring insights that would otherwise be obscure if the answer was, instead, just "false."  Also, we will interestingly show that some undecided data remains undecided no matter what future definitions are made.  This data is called **undecidable**.  This is beneficial in that it is an easy way to create and understand the meaning of Godel's two theorems.

## Finite sequences are not a limitation

Coda contains only finite sequences, so, for example, Coda has a definition mapping a coda (nat:n) to the data n (nat:n+1) where n is an integer.  This means that (nat:0) = 0 1 2 3 4 5 (nat:6), etc.  In other words, (nat:0) fully represents the natural numbers even 
though sequences in Coda are always finite.  

## Proof and Computation

In Coda, the only valid operations in a given context are replacing one data with another data which are equal in the equivalence relation above.  This means, for instance, that a sequence A=D<sub>1</sub>=D<sub>2</sub>=...=D<sub>n</sub>=B, constitutes a proof that A and B are equal.  Similarly, a computation is just a sequence A=D<sub>1</sub>=D<sub>2</sub>=...=D<sub>n</sub>=B where A is given and B is "flattened" down to bytes which can be displayed at a terminal.  It is well know that programs and proofs are analogous (see "The Curry-Howard Correspondence").  In Coda, the situation is simpler:  Every computation is a proof and every proof is a computation.  Also, Coda definitions are proper partial functions in the sense that they must always return 
a value in a finite time.  Since every step in a sequence like A=D<sub>1</sub>=D<sub>2</sub>=...=D<sub>n</sub>=B is a single definition application or a single translation, no single step can loop forever, even though, of course the sequence as a whole may go on forever, as with (nat:0).  

## Types appear naturally

In recent years, there has been lots of interest in foundations of mathematics based on type theory where **type** enters as an undefined term at the beginning (see dependent type theory, homotopy type theory, Coq, Lean and others).  In Coda, on the other hand, data T is a **type** if T is idempotent (T:T:X = T:X) and distributive (T:X Y = (T:X) (T:Y)).  Intuitively if T is a type, T:X is a property of X. 

## The software that runs Coda is small enough to comprehend

Since Coda is meant to be acceptable as mathematics, it is important that the software be tiny enough for a human to fully comprehend.  I would claim that this is true both for the Coda core system (the implementation of data, coda, definitions is approximately 120 lines of python code) and for the Coda language (the compiler and parser are approximately 100 lines of python code).   
