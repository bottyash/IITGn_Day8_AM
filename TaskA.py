# admission_system.py
# University admission screening tool
# Evaluates students based on academic + non-academic criteria

def get_float_input(prompt, min_val, max_val):
    # keep asking until we get a valid number in range
    while True:
        try:
            val = float(input(prompt))
            if min_val <= val <= max_val:
                return val
            print(f"  Enter a value between {min_val} and {max_val}.")
        except ValueError:
            print("  That's not a valid number. Try again.")


def get_choice_input(prompt, valid_choices):
    while True:
        val = input(prompt).strip().lower()
        if val in valid_choices:
            return val
        print(f"  Valid options are: {', '.join(valid_choices)}")


def main():
    print("University Admission Screening System")
    print("-" * 40)

    # --- collect inputs ---
    entrance_score = get_float_input("Entrance Score (0-100): ", 0, 100)
    gpa            = get_float_input("GPA (0-10): ", 0, 10)
    recommendation = get_choice_input("Recommendation letter? (yes/no): ", ["yes", "no"])
    category       = get_choice_input("Category (general/obc/sc_st): ", ["general", "obc", "sc_st"])
    extra_score    = get_float_input("Extracurricular Score (0-10): ", 0, 10)

    # --- auto-admit on very high score, no other checks needed ---
    if entrance_score >= 95:
        print("\nResult: ADMITTED (Scholarship)")
        print("Reason: Entrance score >= 95 qualifies for automatic scholarship admission.")
        return

    # --- apply bonus points ---
    bonus = 0
    bonus_notes = []

    if recommendation == "yes":
        bonus += 5
        bonus_notes.append("+5 (recommendation)")

    if extra_score > 8:
        bonus += 3
        bonus_notes.append("+3 (extracurricular)")

    effective_score = entrance_score + bonus

    if bonus_notes:
        print(f"\nBonus Applied: {' '.join(bonus_notes)}")
    print(f"Effective Score: {effective_score}")

    # --- category cutoffs ---
    cutoffs = {
        "general": 75,
        "obc": 65,
        "sc_st": 55,
    }
    min_score = cutoffs[category]
    min_gpa   = 7.0

    # --- decision logic ---
    score_ok = effective_score >= min_score
    gpa_ok   = gpa >= min_gpa

    print("\nResult:")

    if score_ok and gpa_ok:
        print("ADMITTED (Regular)")
        print(f"Reason: Meets {category.upper()} cutoff ({effective_score} >= {min_score}) and GPA requirement ({gpa} >= {min_gpa})")

    elif score_ok and not gpa_ok:
        # score is fine but GPA drags them down - waitlist is reasonable
        print("WAITLISTED")
        print(f"Reason: Score is acceptable ({effective_score} >= {min_score}) but GPA is below minimum ({gpa} < {min_gpa})")

    elif not score_ok and gpa_ok:
        # close to the mark - worth a waitlist spot
        if effective_score >= min_score - 5:
            print("WAITLISTED")
            print(f"Reason: Score narrowly misses {category.upper()} cutoff ({effective_score} vs {min_score} required)")
        else:
            print("REJECTED")
            print(f"Reason: Effective score {effective_score} is below the {category.upper()} cutoff of {min_score}")

    else:
        print("REJECTED")
        print(f"Reason: Effective score {effective_score} below {category.upper()} cutoff ({min_score}) and GPA {gpa} below minimum ({min_gpa})")


if __name__ == "__main__":
    main()
