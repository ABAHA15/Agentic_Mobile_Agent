def compute_reward(
        observed_text,
        expected
):

    observed_text = (
        observed_text.lower()
    )

    expected = (
        expected.lower()
    )

    if expected in observed_text:
        return 10

    return -5