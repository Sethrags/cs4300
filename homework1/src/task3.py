def classify_number(number):
    if number > 0:
        return "positive"
    elif number < 0:
        return "negative"
    else:
        return "zero"


def is_prime(number):
    if number < 2:
        return False

    for divisor in range(2, number):
        if number % divisor == 0:
            return False

    return True


def first_ten_primes():
    primes = []

    for number in range(2, 30):
        if is_prime(number):
            primes.append(number)

    return primes


def sum_one_to_one_hundred():
    total = 0
    number = 1

    while number <= 100:
        total += number
        number += 1

    return total


if __name__ == "__main__":
    for prime in first_ten_primes():
        print(prime)