# Reduction and Morphism Explorer

# 1. Define the Alphabet and Rewriting Rules
alphabet = {'a', 'b'}
rewrite_rules = {
    'ab': '',
    'ba': ''
}

# 2. Word Reduction Function
def reduce_word(word: str, rules: dict[str, str]) -> str:
    changed = True
    while changed:
        changed = False
        for lhs, rhs in rules.items():
            if lhs in word:
                word = word.replace(lhs, rhs)
                changed = True
    return word

# 3. Morphism Definition
def morphism(word: str, gen_map: dict[str, str]) -> str:
    return ''.join(gen_map[c] for c in word)

# 4. Commutation Check
def commutes_with_reduction(gen_map, rules, test_words):
    for w in test_words:
        f_r = reduce_word(morphism(w, gen_map), rules)
        r_f = morphism(reduce_word(w, rules), gen_map)
        if reduce_word(f_r, rules) != reduce_word(r_f, rules):
            return False
    return True

# 5. Sample Words Generator
def generate_test_words(alphabet, max_length=4):
    from itertools import product
    return [''.join(p) for l in range(1, max_length+1) for p in product(alphabet, repeat=l)]

# 6. Example Morphisms to Test
def example_morphisms():
    return [
        {'a': 'a', 'b': 'b'},           # identity
        {'a': 'b', 'b': 'a'},           # swap
        {'a': 'aa', 'b': 'bb'},         # duplicate
        {'a': 'ab', 'b': 'ba'},         # mixed
        {'a': '', 'b': ''}              # null morphism
    ]

# 7. Isomorphism Check (basic)
def is_isomorphism(gen_map):
    # A morphism is an isomorphism if the generator images are permutations and invertible
    values = set(gen_map.values())
    if len(values) != len(gen_map):
        return False
    inv_map = {v: k for k, v in gen_map.items()}
    return all(inv_map.get(gen_map[c], None) == c for c in gen_map)

# 8. Compute Centralizer of G
# G = {identity, swap}, so we require f to commute with swap: f(a) == swap(f(b)), etc.
def tau(word):
    return ''.join('b' if c == 'a' else 'a' if c == 'b' else c for c in word)

def in_centralizer(gen_map):
    return gen_map.get('a') == tau(gen_map.get('b', ''))

# 9. Run Tests on Morphisms
words = generate_test_words(alphabet)
morphs = example_morphisms()

for i, f in enumerate(morphs):
    print(f"Morphism {i+1}: {f}")
    print("  Commutes with reduction:", commutes_with_reduction(f, rewrite_rules, words))
    print("  Is isomorphism:", is_isomorphism(f))
    print("  In centralizer:", in_centralizer(f))
    print()

# 10. Extendable Section: Add visualizations, algebraic classifications, or dynamic input handling
