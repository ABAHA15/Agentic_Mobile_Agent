from youtube_agent.youtube_logic import (
    run_youtube_agent
)

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    query = input(
        "\nEnter YouTube Search Query: "
    )

    run_youtube_agent(
        query=query
    )