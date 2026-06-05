# ============================================
# CALCULATOR PLAN GENERATOR
# ============================================

def create_plan(expression):

    plan = []

    for char in expression:

        if char.strip() == "":
            continue

        plan.append(

            {
                "action": "tap",
                "target": char
            }
        )

    # ============================================
    # PRESS EQUALS
    # ============================================

    if "=" not in expression:

        plan.append(

            {
                "action": "tap",
                "target": "="
            }
        )

    return plan