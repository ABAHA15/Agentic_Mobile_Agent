def compute_reward(

    search_success,

    typed_correctly,

    search_button_detected,

    wrong_navigation

):

    reward = 0

    # ---------------------------------
    # TYPING
    # ---------------------------------

    if typed_correctly:

        reward += 3

    else:

        reward -= 2

    # ---------------------------------
    # SEARCH BUTTON
    # ---------------------------------

    if search_button_detected:

        reward += 2

    else:

        reward -= 2

    # ---------------------------------
    # FINAL SUCCESS
    # ---------------------------------

    if search_success:

        reward += 10

    else:

        reward -= 5

    # ---------------------------------
    # WRONG PAGE
    # ---------------------------------

    if wrong_navigation:

        reward -= 8

    return reward