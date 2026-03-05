# pan_validator.py
# Part D - AI-Augmented Task
# PAN format: 5 uppercase letters, 4 digits, 1 uppercase letter (e.g., ABCDE1234F)
# The 4th character indicates taxpayer type

# =============================================================================
# EXACT PROMPT USED:
# "Write a Python program that validates an Indian PAN card number format
#  using if-else conditions. PAN format: 5 uppercase letters, 4 digits,
#  1 uppercase letter (e.g., ABCDE1234F). The 4th character indicates
#  the type of taxpayer."
# =============================================================================

# --- AI-generated output (reproduced for submission) ---

# def validate_pan(pan):
#     if len(pan) != 10:
#         return False, "Invalid length"
#     for i in range(5):
#         if not pan[i].isupper() or not pan[i].isalpha():
#             return False, f"Position {i+1} must be uppercase letter"
#     for i in range(5, 9):
#         if not pan[i].isdigit():
#             return False, f"Position {i+1} must be a digit"
#     if not pan[9].isupper() or not pan[9].isalpha():
#         return False, "Last character must be uppercase letter"
#     taxpayer_types = {
#         'P': 'Individual', 'C': 'Company', 'H': 'HUF',
#         'F': 'Firm', 'A': 'AOP', 'T': 'Trust', 'B': 'BOI',
#         'L': 'Local Authority', 'J': 'Artificial Juridical Person', 'G': 'Government'
#     }
#     fourth_char = pan[3]
#     if fourth_char in taxpayer_types:
#         entity = taxpayer_types[fourth_char]
#     else:
#         entity = "Unknown entity type"
#     return True, f"Valid PAN - {entity}"

# =============================================================================
# CRITICAL EVALUATION:
#
# Position validation: Correct. Checks all 10 positions explicitly.
#   Characters 1-5 as uppercase alpha, 6-9 as digits, 10 as uppercase alpha.
#
# The check `pan[i].isupper() and pan[i].isalpha()` is slightly redundant -
#   isupper() already implies the character is alphabetic in Python. Either
#   check is sufficient on its own. Not wrong, just noisy.
#
# Edge cases: No check for empty string or None input. If pan is empty,
#   len(pan) == 0 catches it, but passing None would crash with a TypeError.
#
# The 4th character check is correct - pan[3] is index 3 (0-based), which
#   is the 4th character. This is a common off-by-one trap and the AI got it right.
#
# Approach: Character-by-character is fine for a teaching context. In production
#   you would use a single regex like r'^[A-Z]{5}[0-9]{4}[A-Z]$' which is
#   more concise and less likely to have off-by-one issues. But the assignment
#   asks for if-else, so this is appropriate here.
#
# Pythonic quality: Using a dictionary for taxpayer types is good. The loop
#   for checking characters is clean. The function returns a tuple (bool, msg)
#   which is a reasonable pattern. Overall decent quality.
#
# What I improved:
#   - Added a None/empty guard at the top
#   - Removed redundant isalpha() call alongside isupper()
#   - Added .strip().upper() so minor formatting issues do not cause rejection
#   - Separated format validation from entity lookup for clarity
#   - Added a character-by-character explanation in output
# =============================================================================

TAXPAYER_TYPES = {
    "P": "Individual",
    "C": "Company",
    "H": "HUF (Hindu Undivided Family)",
    "F": "Firm",
    "A": "AOP (Association of Persons)",
    "T": "Trust",
    "B": "BOI (Body of Individuals)",
    "L": "Local Authority",
    "J": "Artificial Juridical Person",
    "G": "Government",
}


def validate_pan(pan):
    # handle None or blank input before anything else
    if not pan:
        return False, "PAN cannot be empty"

    pan = pan.strip().upper()

    if len(pan) != 10:
        return False, f"PAN must be exactly 10 characters (got {len(pan)})"

    # first 5 must be uppercase letters
    for i in range(5):
        if not pan[i].isupper():
            return False, f"Character {i+1} must be an uppercase letter (got '{pan[i]}')"

    # next 4 must be digits
    for i in range(5, 9):
        if not pan[i].isdigit():
            return False, f"Character {i+1} must be a digit (got '{pan[i]}')"

    # last character must be an uppercase letter
    if not pan[9].isupper():
        return False, f"Character 10 must be an uppercase letter (got '{pan[9]}')"

    # 4th character indicates entity type - pan[3] is index 3
    fourth = pan[3]
    entity = TAXPAYER_TYPES.get(fourth, f"Unknown entity code '{fourth}'")

    return True, f"Valid PAN  |  Taxpayer type: {entity}"


def main():
    print("PAN Card Validator")
    print("-" * 30)

    test_inputs = [
        "ABCDE1234F",   # valid individual - typical example
        "AABC12345F",   # invalid - 4th char not a known entity code (still valid format)
        "ABCDE123",     # too short
        "abcde1234f",   # lowercase - should still work after .upper()
        "ABCDE1234",    # missing last letter
        "ABC1E1234F",   # digit in wrong position
        "",             # empty
        "ABCPH1234K",   # valid HUF
    ]

    for pan in test_inputs:
        valid, message = validate_pan(pan)
        status = "VALID  " if valid else "INVALID"
        print(f"  {status}  |  input: {repr(pan):<15}  |  {message}")


if __name__ == "__main__":
    main()
