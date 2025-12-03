favorite_languages = {
    'jen': 'sample_code',
    'sarah': 'c',
    'edward': 'rust',
    'phil': 'sample_code',
}

print("The following languages have been mentioned:")
for language in set(favorite_languages.values()):
    print(language.title())