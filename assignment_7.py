import re

EMAIL_PATTERN = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+'

def find_emails(text):
    """Returns a list of every email-shaped substring found in `text`."""
    return re.findall(EMAIL_PATTERN, text)


def is_valid_email(candidate):
    """Returns True only if the ENTIRE string is a valid email address."""
    return re.fullmatch(EMAIL_PATTERN, candidate) is not None


if __name__ == "__main__":

    sample_text = """
    Please contact us for support:
    - General queries: support@examplecorp.com
    - Sales team: sales.team@business-hub.co.in
    - Personal note from Rahul (rahul_23@gmail.com) sent yesterday.
    - Invalid mentions: not-an-email, @missing-local.com, plain.text@
    - Newsletter sign-up: newsletter+promo@my-site.org
    """

    print("Original text:")
    print(sample_text)

    found = find_emails(sample_text)
    print(f"Found {len(found)} email address(es) in the text:")
    for email in found:
        print(f"  - {email}")

    print("\nValidating individual strings with is_valid_email():")
    test_cases = [
        "john.doe@example.com",
        "invalid-email",
        "user@site",
        "user@site.com",
        "plain.text@",
        "a.b-c_d+e@sub.domain.co.in",
    ]
    for candidate in test_cases:
        result = "VALID" if is_valid_email(candidate) else "INVALID"
        print(f"  {candidate:30s} -> {result}")