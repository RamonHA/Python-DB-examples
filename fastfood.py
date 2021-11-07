from abc import abstractmethod, ABCMeta
from datetime import date, datetime

class Meal():
    def __init__(self, meal, price = 0, qty = 0):
        self.price = price
        self.meal = meal
        self.qty = qty
        self.name = meal

    def __str__(self):
        return self.name


class SubMeal(Meal):
    def __init__(self, submeal, price = 0, qty = 0):
        Meal.__init__( self, submeal.split(" ")[0], price, qty )
        self.name = submeal

class Menu:
    def __init__(self, meal = None, submeal = None):
        self.__meals = []
        self.__total = 0

        if meal is not None:
            self.meals(meal)
        
        if submeal is not None:
            self.meals(submeal)

    def meals(self, value):
        if isinstance(value, Meal) or isinstance(value , SubMeal):
            self.__meals.append( value )
            self.__total += ( value.price*value.qty )
        elif isinstance(value, list):
            for i in value:
                self.meals( i )
        else:
            raise ValueError("Meal must be a Meal Object")            

    def total(self):
        assert sum([i.price*i.qty for i in self.__meals]) == self.__total, "There was an error when log in meals."
        return self.__total

    def __str__(self):
        s = "#"*54 + "\n"
        s += "#"*20 + "  RESTAURANT  " + "#"*20 + "\n" 
        s += "\n Product\t  Price c/u\tQty\tPrice\n"
        for i in self.__meals:
            if len(i.name) > 14:
                s += " {}\t{}\t{}\t{}\n".format( 
                        i.name,
                        i.price,
                        i.qty,
                        i.price*i.qty
                    )
            else:
                s += " {}\t\t{}\t{}\t{}\n".format( 
                        i.name,
                        i.price,
                        i.qty,
                        i.price*i.qty
                    )
        
        s += "\n\t\t\t\tTotal: $ {} MXN\n".format( self.total() )

        return s

    def ticket(self):
        print(self)

    def get_meals(self):
        return self.__meals

class Order:
    def __init__(self, menu = None, date = date.today()):
        self.__menu = []
        self.__total = 0

        self.date = date

        if menu is not None:
            self.menu(menu)
    
    def __str__(self):
        s = "#"*54 + "\n"
        s += "#"*20 + "  RESTAURANT  " + "#"*20 + "\n" 
        s += " Breakdown of Menus for {}.\n".format(self.date)

        v = 1
        for m in self.__menu:
            s += " Menu #{}\n".format( v)
            v += 1
            s += "\n Product\t  Price c/u\tQty\tPrice\n"
            for i in m.get_meals():
                if len(i.name) > 14:
                    s += " {}\t{}\t{}\t{}\n".format( 
                            i.name,
                            i.price,
                            i.qty,
                            i.price*i.qty
                        )
                else:
                    s += " {}\t\t{}\t{}\t{}\n".format( 
                            i.name,
                            i.price,
                            i.qty,
                            i.price*i.qty
                        )
            
            s += "\n\t\t\t\tTotal: $ {} MXN\n\n".format( m.total() )

        s += "\n\t\t\t General Total: $ {} MXN\n".format( self.total() )
        
        return s

    def total(self):
        return sum( [ i.total() for i in self.__menu ] )

    def menu(self, value):
        if isinstance(value, Menu):
            self.__menu.append(value)
            self.__total += 0
        elif isinstance(value, list):
            for i in value:
                self.menu(i)
        else:
            raise ValueError( "The Menu must be a type Menu" )

    def ticket(self):
        print(self)

    def payment_methods(self):
        return [
            "Debit/Credit card",
            "DAI",
            "Paypal",
            "Taquitos"
        ]

    def auth_methods(self):
        return [
            "DNI",
            "Email",
            "SMS"
        ]
    
    def form_of_pickup(self):
        return [
            "In Place",
            "Delivery",
            "Pick Up"
        ]

    # def pay(self, method = "Debid/Credit card", auth = "DNI", pickup = "Delivery"):
    #     # Check for emails, dni, numbers, etc.

    #     assert method in self.payment_methods(), "Payment method wrong"
    #     assert auth in self.auth_methods(), "Auth method wrong"
    #     assert pickup in self.form_of_pickup(), "Pick Up method wrong"

    #     print("Total will be: $ {} MXN".format(self.total()))
    #     print("Payment with {} method, auth {}, and will be {}.".format(method, auth, pickup))
    #     print("Confirm payment!")
    #     print("Come back soon!!")

    #     print("RESTAURANT")

    def pay(self, payment):
        assert isinstance(payment, Payment), "Payment is not type Payment"
        payment.pay()
    
class Payment:
    def __init__(self, type, auth, pickup):
        self.type = type
        self.auth = auth
        self.pickup = pickup

        self.__address = None
        self.__email = None
        self.__date = None
        self.__debitcredit = None
        
    def payment_methods(self):
        return [
            "Debit/Credit card",
            "DAI",
            "Paypal",
            "Taquitos"
        ]

    def auth_methods(self):
        return [
            "DNI",
            "Email",
            "SMS"
        ]
    
    def form_of_pickup(self):
        return [
            "In Place",
            "Delivery",
            "Pick Up"
        ]

    def pay(self):
        try: 
            {
                "Debit/Credit card":self.debitcredit
            }.get(self.type, True)
        except:
            raise Exception("Payment method not filled")

        try: 
            {
                "Email":self.email
            }.get(self.auth, True)
        except:
            raise Exception("Auth method not filled")

        try: 
            {
                "Delivery":self.address,
                "Pick Up":self.date
            }.get(self.pickup, True)
        except:
            raise Exception("Pick Up method not filled")

        print("Payment with {} method, auth {}, and will be {}.".format(self.type, self.auth, self.pickup))
        print("Confirm payment!")
        print("Come back soon!!")

    @property
    def debitcredit(self):
        return self.__debitcredit
    
    @debitcredit.setter
    def debitcredit(self, value):
        self.__debitcredit = value

    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, value):
        assert isinstance(value, str), "Email is not valid"
        self.__email = value

    @property
    def address(self):
        return self.__address
    
    @address.setter
    def address(self, value):
        assert isinstance(value, str), "Addres is not valid"
        self.__address = value
    
    @property
    def date(self):
        return self.__date
    
    @date.setter
    def date(self, value):
        assert isinstance(value, datetime), "Date is no datetime"
        self.__date = value


if __name__ == "__main__":
    m = Menu()
    m.meals( SubMeal("pizza hawaiana", 100, 1) )
    m.meals( SubMeal("hamburguesa normal", 70, 2) )

    print(m)

    m2 = Menu( 
        submeal= [
            SubMeal("tacos de pastor", 10, 5),
            SubMeal("suchi frito", 70, 1)
        ] 
    )

    print(m2)

    o = Order( [m, m2] )

    print(o)

    p = Payment(type="Debit/Credit card", auth="Email", pickup="Pick Up")
    p.debitcredit = 1234
    p.email = "rha@gmail"
    p.date = datetime(2021,1,1, 4) # Date of pick up
    
    o.pay(p)
