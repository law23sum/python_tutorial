favorite_languages = {
    'jen': ['sample_code', 'rust'],
    'sarah': ['c'],
    'edward': ['rust', 'go'],
    'phil': ['sample_code', 'haskell'],
}

for name, languages in favorite_languages.items():
    print(f"\n{name.title()}'s favorite languages are:")
    for language in languages:
        print(f"\t{language.title()}")