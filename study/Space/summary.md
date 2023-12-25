| Space | Elements | Operation | Space | Simple | Idempotent | Distributive | Distributive 2 | Commutative | Involution | Nilpotent | 
|-------|----------|-----------|-----:|-------:|-----------:|-------------:|--------:|------------:|-----------:|----------:|
| ap A | A:x for atomic x | Apply A to input atoms | Y | Y | Y | Y | Y | N | N | N | 
| bool | () or (:) | logical value | Y | Y | Y | N | Y | Y | N | N |
| collect | atoms | collect atoms with equal left sides | x | x | x | x | x | x | x | x |
| first | single atoms | get first | x | x | x | x | x | x | x | x | 
| has bin | bin atoms | select bin atoms | Y | Y | Y | Y | Y | N | N | N | 
| is 1 2 3 4 | sequences of 1 2 3 4 | filter | x | x | x | x | x | x | x | x | 
| pass | all data | do nothing | Y | Y | Y | Y | Y | N | Y | N | 
| null | () | empty | Y | Y | Y | Y | Y | Y | N | Y |
| rep \| | sequences of \|s | counting | Y | Y | Y | Y | Y | Y | N | N |
