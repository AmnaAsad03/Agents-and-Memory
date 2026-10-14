import re

from langchain_core.tools import tool


@tool
def calculate(expression: str) -> str:
    """Calculate mathematical expressions, including percentage expressions such as '20% of 500'."""

    try:
        expression = expression.strip()

        percentage_match = re.fullmatch(
            r"(\d+(?:\.\d+)?)%\s+of\s+(\d+(?:\.\d+)?)",
            expression,
            re.IGNORECASE,
        )

        if percentage_match:
            percentage = float(percentage_match.group(1))
            number = float(percentage_match.group(2))

            result = (percentage / 100) * number

            if result.is_integer():
                return str(int(result))

            return str(result)

        result = eval(
            expression,
            {"__builtins__": {}},
            {},
        )

        return str(result)

    except ZeroDivisionError:
        return "Calculation failed: division by zero."

    except (SyntaxError, ValueError, TypeError):
        return "Calculation failed: invalid mathematical expression."

    except Exception as error:
        return f"Calculation failed: unexpected error: {error}"