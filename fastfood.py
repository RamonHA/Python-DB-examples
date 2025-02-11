from abc import abstractmethod, ABCMeta
from datetime import date, datetime

import psycopg2


def menu():
    with psycopg2.connect( "dbname=ramon_hinojosa_d user=ramon_hinojosa password=ramon_hinojosa123*" ) as conexion:
        with conexion.cursor() as cur:
            print("\nMain dishes:")
            cur.execute(
                "select dish, price from rha_dish;"
            )
            for d, p in cur.fetchall():
                print("{} ... ${}".format(d, p))

            print("\nIngredients:")
            cur.execute(
                "select ingredient, price from rha_ingredients;"
            )
            for d, p in cur.fetchall():
                print("{} ... ${}".format(d, p))


class Meal():
    def __init__(self, meal = None, price = 0, qty = 0):
        self.price = price
        self.qty = qty
        self.name = meal

    def __str__(self):
        return self.name

    def ensure_meal(self):
        with psycopg2.connect( "dbname=ramon_hinojosa_d user=ramon_hinojosa password=ramon_hinojosa123*" ) as conexion:
            with conexion.cursor() as cur:
                cur.execute(
                    "select dish from rha_dish;"
                )
                for d, in cur.fetchall():
                    if d.strip() == self.name: return True
                
                return False

    def add_meal(self):
        if self.ensure_meal(): 
            print("Meal already on database, not updated")
            return None

        with psycopg2.connect( "dbname=ramon_hinojosa_d user=ramon_hinojosa password=ramon_hinojosa123*" ) as conexion:
            with conexion.cursor() as cur:
                cur.execute(
                    "INSERT INTO rha_dish ( dish, price ) VALUES ( '{}', {} );".format(self.name, self.price)
                )
                conexion.commit()

        print("Dish Database successfully updated with {} at {}!".format(self.name, self.price))

    def add_ingredient(self):
        if self.ensure_ingredients():
            print("Ingredient already on database, not updated")
            return None

        with psycopg2.connect( "dbname=ramon_hinojosa_d user=ramon_hinojosa password=ramon_hinojosa123*" ) as conexion:
            with conexion.cursor() as cur:

                cur.execute(
                    "INSERT INTO rha_ingredients ( ingredient, price ) VALUES ( '{}', {} );".format(self.name, self.price)
                )
                conexion.commit()

        print("Ingredients Database successfully updated with {} at {}!".format(self.name, self.price))

    def ensure_ingredients(self):
        with psycopg2.connect( "dbname=ramon_hinojosa_d user=ramon_hinojosa password=ramon_hinojosa123*" ) as conexion:
            with conexion.cursor() as cur:
                cur.execute(
                    "select ingredient from rha_ingredients;"
                )
                for d, in cur.fetchall():
                    if d.strip() == self.name: return True
                
                return False

class Food(Meal):
    def __init__(self, submeal, price = 0, qty = 0):
        Meal.__init__( self, meal = submeal, price = price, qty = qty )
        self.name = submeal
        self.ingredients = submeal.replace("and", "").replace("with", "").split(" ")[1:]

        if price == 0:
            self.price = self.get_price()

    def get_price(self):
        return self.get_meal() + self.get_ingredients()
    
    def get_meal(self):
        with psycopg2.connect( "dbname=ramon_hinojosa_d user=ramon_hinojosa password=ramon_hinojosa123*" ) as conexion:
            with conexion.cursor() as cur:
                cur.execute(
                    "select dish, price from rha_dish;"
                )
                for d, p in cur.fetchall():
                    if d.strip() == self.name.split(" ")[0]: return p

        raise ValueError("Meal not in Database")

    def get_ingredients(self):
        return sum([self.get_ingredients_indv(i) for i in self.ingredients])

    def get_ingredients_indv(self, value):
        with psycopg2.connect( "dbname=ramon_hinojosa_d user=ramon_hinojosa password=ramon_hinojosa123*" ) as conexion:
            with conexion.cursor() as cur:
                cur.execute(
                    "select ingredient, price from rha_ingredients;"
                )
                for d, p in cur.fetchall():
                    if d.strip() == value: return p

        raise ValueError("Ingredient not in Database")

class Menu:
    def __init__(self, meal = None, submeal = None):
        self.__meals = []
        self.__total = 0

        if meal is not None:
            self.meals(meal)
        
        if submeal is not None:
            self.meals(submeal)

    def meals(self, value):
        if isinstance(value, Meal) or isinstance(value , Food):
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
    def __init__(self, menu = None, date = datetime.today()):
        self.__menu = []
        self.__total = 0

        self.date = date

        self.order_id = str(datetime.timestamp(date))

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

    def update_db(self):
        for i in self.__menu:
            self.update_df_inv( i )

    def update_df_inv(self, i):
        conexion = psycopg2.connect( "dbname=ramon_hinojosa_d user=ramon_hinojosa password=ramon_hinojosa123*" )

        cur = conexion.cursor()
        s = "INSERT INTO rha_orders( order_id, date, dish, price_uni, qty, price_t,  payment_type, auth, pickup) VALUES "
        for m in i.get_meals():
            s += "('{}', '{}', '{}', {}, {}, {}, '{}', '{}', '{}'), ".format( 
                            self.order_id, 
                            self.date, 
                            m.name, 
                            m.price, 
                            m.qty, 
                            m.qty*m.price,
                            self.payment.type,
                            self.payment.auth,
                            self.payment.pickup
                            )
        
        s = s[:-2] + ";"

        cur.execute(s)
        conexion.commit()

        cur.close()
        conexion.close()

        print("Database successfully updated.")

    def ticket(self):
        print(self)

    def pay(self, payment):
        assert isinstance(payment, Payment), "Payment is not type Payment"
        self.payment = payment
        self.payment.pay()
        self.update_db()
    
class Payment:
    def __init__(self, type = None, auth = None, pickup = None):
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

    def pay_excp(self):
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

    def pay(self):
        self.pay_excp()
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

    # Add Meals to Menu available
    Meal("pizza", 100).add_meal()
    Meal("pina", 10).add_ingredient()
    Meal("hamburguesa", 70).add_meal()
    Meal("arrachera", 20).add_ingredient()

    menu()


    m = Menu()
    m.meals( Food("pizza pina", qty=  1) )
    m.meals( Food("hamburguesa arrachera", qty = 2) )

    print(m)


    o = Order( m )

    print(o)

    p = Payment(type="Debit/Credit card", auth="Email", pickup="Pick Up")
    p.debitcredit = 1234
    p.email = "rha@gmail"
    p.date = datetime(2021,1,1, 4) # Date of pick up
    
    o.pay(p)

    




