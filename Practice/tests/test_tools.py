from app.tools.calculator import calculate


def test_calculator_correct_result():
    result = calculate.invoke(
        {
            "expression": "20% of 5000"
        }
    )

    assert "1000" in str(result)