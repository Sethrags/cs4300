"""Task 3: Control structures."""


def classify_number(number):
    """Return whether a number is positive, negative, or zero."""
    if number > 0:
        return "positive"
    elif number < 0:
        return "negative"
    else:
        return "zero"


def is_prime(number):
    """Return True when a number is prime."""
    if number < 2:
        return False

    for divisor in range(2, number):
        if number % divisor == 0:
            return False

    return True


def first_ten_primes():
    """Return the first ten prime numbers."""
    primes = []
    number = 2

    while len(primes) < 10:
        if is_prime(number):
            primes.append(number)

        number += 1

    return primes


def sum_one_to_one_hundred():
    """Return the sum of all numbers from 1 through 100."""
    total = 0
    number = 1

    while number <= 100:
        total += number
        number += 1

    return total


if __name__ == "__main__":
    for prime in first_ten_primes():
        print(prime)