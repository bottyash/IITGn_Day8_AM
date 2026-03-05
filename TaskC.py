# interview_ready.py
# Part C answers - conceptual, coding, and debug

# =============================================================================
# Q1 - elif vs multiple if statements
# =============================================================================

# The key difference: elif is part of a chain - once one branch is true,
# the rest are skipped. Multiple if statements are independent checks,
# so ALL of them can execute if their conditions are true.

score = 85

print("Multiple if result:")
grade = "F"
if score >= 60:
    grade = "D"
if score >= 70:
    grade = "C"
if score >= 80:
    grade = "B"
if score >= 90:
    grade = "A"
print(f"  score={score}, grade={grade}")

print("elif result:")
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"
print(f"  score={score}, grade={grade}")

# Concrete case where outputs actually diverge:
x = 15
print("\nWhere outputs actually differ (x=15):")
print("  Multiple if:")
if x > 5:
    print("    x is greater than 5")
if x > 10:
    print("    x is greater than 10")

print("  elif:")
if x > 10:
    print("    x is greater than 10")
elif x > 5:
    print("    x is greater than 5")


# =============================================================================
# Q2 - Triangle classifier
# =============================================================================

def classify_triangle(a, b, c):
    # reject zero or negative values before anything else
    if a <= 0 or b <= 0 or c <= 0:
        return "Invalid: sides must be positive"

    # the triangle inequality - sum of any two sides must strictly exceed the third
    if a >= b + c or b >= a + c or c >= a + b:
        return "Not a triangle"

    if a == b == c:
        return "Equilateral"
    elif a == b or b == c or a == c:
        return "Isosceles"
    else:
        return "Scalene"


print("\nTriangle classifier:")
test_cases = [
    (5, 5, 5),
    (5, 5, 3),
    (3, 4, 5),
    (1, 2, 3),
    (0, 4, 5),
    (-1, 4, 5),
]
for a, b, c in test_cases:
    print(f"  ({a}, {b}, {c}) -> {classify_triangle(a, b, c)}")


# =============================================================================
# Q3 - Debug the grade code
# =============================================================================

# Bug: all four checks are separate if statements, not elif.
# For score=85, conditions >= 60, >= 70, and >= 80 all fire in sequence.
# Each one overwrites grade, so the final value is the last match.
# It looks correct for many inputs but that is coincidence, not correctness.
# If someone reorders the checks or the logic gets more complex, this breaks.
#
# Fix: order from highest threshold down and use elif.
# Only one branch runs, and the intent is obvious.

score = 85
if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"\nFixed grade for {score}: {grade}")
