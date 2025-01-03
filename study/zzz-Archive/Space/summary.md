| Space | Elements | Operation | Space | Simple | Idempotent | Dist. | Dist2 | Commutative | Involution | Nilpotent | Semilattice |
|-------|----------|-----------|-----:|-------:|-----------:|-------------:|--------:|------------:|-----------:|----------:|-------:|
| pass | all data | do nothing | Y | Y | Y | Y | Y | N | Y | N | N |
| null | () | empty | Y | Y | Y | Y | Y | Y | N | Y | Y |
| bool | () or (:) | logical value | Y | Y | Y | N | Y | Y | N | N | Y |
| collect | atoms | collect atoms with equal left sides | Y | Y | Y | N | Y | N | N | N | N |
| first | single atoms | get the first atom | Y | Y | Y | N | Y | N | N | N | Y |
| has bin | bin atoms | select bin atoms | Y | Y | Y | Y | Y | N | N | N | N |
| is 1 2 3 4 | sequences of 1 2 3 4 | filter | Y | Y | Y | Y | Y | Y | N | N | N |
| rep \| | sequences of \|s | counting | Y | Y | Y | Y | Y | Y | N | N | N |
| nats | natural sequences | filter | Y | Y | Y | Y | Y | N | N | N | N |
| is 1 2 | sequences of 1 or 2 | filter | Y | Y | Y | Y | Y | N | N | N | N |
| once * nats | natural sequences | filter | Y | Y | Y | N | Y | Y | N | N | Y |
| once * is 1 2 3 | sequences of 1 2 3 at most once each | filter | Y | Y | Y | N | Y | Y | N | N | Y |
|n.type| naturals | make | Y | Y | Y | Y | Y | N | N | N | N |
|n.sum| natural | sum | Y | Y | Y | N | Y | Y | N | N | N | 
|n.prod| natural | product | Y | Y | Y | N | Y | Y | N | N | N | 
|n.sort| ordered naturals | sort | Y | Y | Y | N | Y | Y | N | N | N | 
|n.ring| natural | prod and sum | Y | N | Y | N | Y | Y | N | N | N | 
|m.type| alt naturals | make | Y | Y | Y | Y | Y | N | N | N | N |
|m.sum| alt natural | sum | Y | Y | Y | N | Y | Y | N | N | N | 
|m.prod| alt natural | product | Y | Y | Y | N | Y | Y | N | N | N | 
|m.sort| alt ordered naturals | sort | Y | Y | Y | N | Y | Y | N | N | N | 
|m.ring| alt natural | prod and sum | Y | N | Y | N | Y | Y | N | N | N | 

