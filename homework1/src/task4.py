def calculate_discount(price, discount):
    try:
        if price < 0:
            raise ValueError("Price cannot be negative")

        if discount < 0 or discount > 100:
            raise ValueError("Discount must be between 0 and 100")

        return price - (price * discount / 100)

    except TypeError:
        raise TypeError("Price and discount must be numbers")