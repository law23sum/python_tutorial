# Put mysay.py in the same folder as this script
import pathlib

from mysay import print_say

# Open the file, and read the content of the text file
myfile = pathlib.Path.cwd() / 'files' / 'storm.txt'
with open(myfile, 'r') as f:
    content = f.read()
# Let Python speak the text in the file   
print_say(content)
