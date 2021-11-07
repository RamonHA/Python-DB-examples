import pytest
from fastfood import *

@pytest.mark.parametrize(
    ("meal,price,qty"),
    [
        ("pizza", 1.1, 1),
        ("hamburguesa", 1000, 1),
        ("tacos", 5.5, 1.0)
    ]
)
def test_mea( meal, price, qty ):
    m = Meal( meal, price, qty )

@pytest.mark.parametrize(
    ("submeal,price,qty"),
    [
        ("pizza con pina", 1.1, 1),
        ("hamburguesa clasica", 1000, 1),
        ("tacos de trompo", 5.5, 1.0)
    ]
)
def test_mea( submeal, price, qty ):
    m = SubMeal( submeal, price, qty )
    
@pytest.mark.parametrize(
    ("arg"),
    [
        (Meal("pizza", 100, 1)),
        (SubMeal("pizza con pina", 100, 1)),
        ([SubMeal("pizza con pina", 100, 1), SubMeal("pizza de pepperoni", 100, 1)]),
        ([SubMeal("hamburguesa clasica", 100, 1), SubMeal("hamburguesa de pollo", 100, 1)]),        
    ]
)
def test_menu(arg):
    m = Menu( arg )

@pytest.mark.parametrize(
    ("arg"),
    [
        (Menu( Meal("pizza", 100, 1) )),
        (Menu( [SubMeal("pizza con pina", 100, 1), SubMeal("pizza de pepperoni", 100, 1)] ))
    ]
)
def test_order(arg):
    o = Order( menu = arg )

def test_payment():
    p = Payment(type="Debit/Credit card", auth="Email", pickup="Pick Up")
    p.debitcredit = 1234
    p.email = "rha@gmail"
    p.date = datetime(2021,1,1, 4) # Date of pick up
    p.pay()