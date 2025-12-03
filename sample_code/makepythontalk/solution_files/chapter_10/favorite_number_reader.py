import json
from pathlib import Path

path = Path('favorite_number.json')
contents = path.read_text()
number = json.loads(contents)

print(f"I know your favorite number! It's {number}.")
