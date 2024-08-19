import pytest
from app.calculations import subtract

@pytest.mark.parametrize("num1, num2, result", [(3, 2, 5), (7, 1, 6)])
def test_add(num1, num2, result):
    print("testing function")
    assert subtract(num1, num2) == result