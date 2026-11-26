
import re

passwords = ["Python@123", "python123"]

pattern = r"^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$"

for password in passwords:
    if re.match(pattern, password):
        print(password, "- Valid password")
    else:
        print(password, "- Invalid password")
