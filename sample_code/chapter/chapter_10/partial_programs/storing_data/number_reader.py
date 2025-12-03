import json
from pathlib import Path

path = Path('numbers.json')
contents = path.read_text()
numbers = json.loads(contents)

print(numbers)
