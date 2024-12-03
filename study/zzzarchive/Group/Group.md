
As an example of some mathematical structure, consider groups.  A group, $G$, is a set with an associative binary operation containing an identity ($e$), and with inverses so that for each $g\in G$ that $g^{-1}g=gg^{-1}=e$.  

Let's see how this concept works when defined as data instead of as a ZFC set.

### Group

A **group** $G$ is a type with associative product (`prod G`), identity (`id:G`) and with an inverse (`inv G`), satisfying

- `Type : G`
- `Associative : prod G`
- `Identity (id:G) : prod G`
- `Inverse (inv G) : prod G`

for `type G:g?`
```
this is some code
```
