favorite_languages = {
    'jen': 'sample_code',
    'sarah': 'c',
    'edward': 'rust',
    'phil': 'sample_code',
}

friends = ['phil', 'sarah']
for name in favorite_languages.keys():
    print(f"Hi {name.title()}.")

    if name in friends:
        language = favorite_languages[name].title()
        print(f"\t{name.title()}, I see you love {language}!")