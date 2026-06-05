from calculator_agent.calculator_logic import (
    run_calculator_agent
)

if __name__ == "__main__":

    expression = input(
        "Enter arithmetic operation: "
    )

    run_calculator_agent(
        expression
    )