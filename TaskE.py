# transaction_validator.py
# Rule-based fraud detection engine
# BLOCK rules override everything - check those first

# category spending limits (normal user)
CATEGORY_LIMITS = {
    "food":        5_000,
    "travel":      float("inf"),   # no specific limit mentioned
    "electronics": 30_000,
    "other":       float("inf"),
}

SINGLE_TXN_LIMIT = 50_000
DAILY_LIMIT      = 100_000


def get_limits(is_vip):
    # VIP doubles all limits - ternary operator to set them dynamically
    multiplier = 2 if is_vip else 1
    return {
        "single":     SINGLE_TXN_LIMIT * multiplier,
        "daily":      DAILY_LIMIT * multiplier,
        "food":       CATEGORY_LIMITS["food"] * multiplier,
        "electronics": CATEGORY_LIMITS["electronics"] * multiplier,
    }


def validate_transaction(amount, category, hour, daily_spent, is_vip=False):
    limits = get_limits(is_vip)
    vip_tag = " (VIP limits applied)" if is_vip else ""

    # --- BLOCK rules - checked first, nothing overrides these ---
    if amount > limits["single"]:
        return "BLOCKED", f"Exceeds single transaction limit of Rs {limits['single']:,.0f}{vip_tag}"

    if daily_spent + amount > limits["daily"]:
        projected = daily_spent + amount
        return "BLOCKED", f"Would exceed daily limit of Rs {limits['daily']:,.0f} (projected: Rs {projected:,.0f}){vip_tag}"

    # --- FLAG rules ---
    if hour < 6 or hour > 23:
        return "FLAGGED", f"Unusual transaction time ({hour}:00 - outside 6AM-11PM window)"

    if category == "food" and amount >= limits["food"]:
        return "FLAGGED", f"Food transaction Rs {amount:,.0f} meets or exceeds limit of Rs {limits['food']:,.0f}{vip_tag}"

    if category == "electronics" and amount >= limits["electronics"]:
        return "FLAGGED", f"Electronics transaction Rs {amount:,.0f} meets or exceeds limit of Rs {limits['electronics']:,.0f}{vip_tag}"

    return "APPROVED", "Transaction looks fine"


def main():
    print("Transaction Validator - Fraud Detection")
    print("-" * 42)

    # --- collect inputs ---
    while True:
        try:
            amount = float(input("Transaction amount (Rs): "))
            if amount <= 0:
                print("  Amount must be positive.")
                continue
            break
        except ValueError:
            print("  Enter a valid number.")

    category = input("Category (food/travel/electronics/other): ").strip().lower()
    if category not in CATEGORY_LIMITS:
        print(f"  Unknown category, treating as 'other'.")
        category = "other"

    while True:
        try:
            hour = int(input("Hour of transaction (0-23): "))
            if 0 <= hour <= 23:
                break
            print("  Hour must be 0 to 23.")
        except ValueError:
            print("  Enter a whole number.")

    while True:
        try:
            daily_spent = float(input("Amount already spent today (Rs): "))
            if daily_spent >= 0:
                break
            print("  Cannot be negative.")
        except ValueError:
            print("  Enter a valid number.")

    vip_input = input("VIP account? (yes/no): ").strip().lower()
    is_vip = vip_input == "yes"

    # --- run validation ---
    status, reason = validate_transaction(amount, category, hour, daily_spent, is_vip)

    print(f"\nTransaction: Rs {amount:,.0f} | {category} | {hour:02d}:00")
    print(f"Decision   : {status}")
    print(f"Reason     : {reason}")


if __name__ == "__main__":
    main()
