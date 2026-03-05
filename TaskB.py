# tax_calculator.py
# Indian Income Tax - New Regime FY 2024-25
# Progressive / slab-wise calculation (not a flat rate)

# Tax slabs under the new regime
# Each entry: (slab ceiling, rate)
# A ceiling of None means "everything above the previous slab"
SLABS = [
    (300_000,  0.00),
    (700_000,  0.05),
    (1_000_000, 0.10),
    (1_200_000, 0.15),
    (1_500_000, 0.20),
    (None,      0.30),
]

STANDARD_DEDUCTION = 75_000


def calculate_tax(taxable_income):
    """
    Walk through each slab and tax only the portion of income that falls in it.
    Returns a list of (slab_label, income_in_slab, tax_for_slab) and total tax.
    """
    breakdown = []
    tax_total  = 0
    prev_limit = 0

    for ceiling, rate in SLABS:
        if taxable_income <= prev_limit:
            # income is fully covered by earlier slabs
            break

        if ceiling is None:
            # last slab - everything remaining
            income_in_slab = taxable_income - prev_limit
            label = f"Above {prev_limit // 100_000}L"
        else:
            income_in_slab = min(taxable_income, ceiling) - prev_limit
            if prev_limit == 0:
                label = f"0 - {ceiling // 100_000}L"
            else:
                label = f"{prev_limit // 100_000}L - {ceiling // 100_000}L"

        slab_tax = income_in_slab * rate
        tax_total += slab_tax
        breakdown.append((label, income_in_slab, rate * 100, slab_tax))

        if ceiling is not None:
            prev_limit = ceiling

    return breakdown, tax_total


def main():
    print("Income Tax Calculator - New Regime FY 2024-25")
    print("-" * 48)

    while True:
        try:
            gross_income = float(input("Annual income (Rs): "))
            if gross_income < 0:
                print("  Income cannot be negative.")
                continue
            break
        except ValueError:
            print("  Enter a valid number.")

    taxable_income = max(0, gross_income - STANDARD_DEDUCTION)

    print(f"\nGross Income        : Rs {gross_income:>12,.0f}")
    print(f"Standard Deduction  : Rs {STANDARD_DEDUCTION:>12,.0f}")
    print(f"Taxable Income      : Rs {taxable_income:>12,.0f}")

    # no tax below 3 lakh even before deduction, just clarify
    breakdown, total_tax = calculate_tax(taxable_income)

    print("\nSlab-wise Breakdown:")
    print(f"  {'Slab':<20} {'Income in Slab':>15} {'Rate':>6} {'Tax':>12}")
    print("  " + "-" * 57)

    for label, income, rate, tax in breakdown:
        print(f"  {label:<20} Rs {income:>12,.0f} {rate:>5.0f}%  Rs {tax:>10,.0f}")

    print("  " + "-" * 57)
    print(f"  {'Total Tax':<20}                        Rs {total_tax:>10,.0f}")

    if gross_income > 0:
        effective_rate = (total_tax / gross_income) * 100
        print(f"\nEffective Tax Rate  : {effective_rate:.2f}%")
    else:
        print("\nEffective Tax Rate  : 0.00%")

    monthly_takehome = (gross_income - total_tax) / 12
    print(f"Monthly Take-Home   : Rs {monthly_takehome:>12,.0f}")


if __name__ == "__main__":
    main()
