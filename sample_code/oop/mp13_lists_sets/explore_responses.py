import json
from pathlib import Path

path = Path('responses.json')
contents = path.read_text()
responses = json.loads(contents)

num_responses = len(responses)
print(f"Found {num_responses:,} responses.")
