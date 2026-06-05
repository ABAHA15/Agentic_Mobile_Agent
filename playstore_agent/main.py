from playstore_agent.playstore_logic import (
    run_playstore_agent
)

# ============================================
# MAIN ENTRY
# ============================================

if __name__ == "__main__":

    app_name = input(
        "\nEnter App Name To Install: "
    )

    run_playstore_agent(
        app_name
    )