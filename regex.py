import re

text = input("Enter a text string: ")

pattern = r'\b\d{2}-\d{2}-\d{4}\b'

dates = re.findall(pattern, text)

print("Dates found:", dates)
