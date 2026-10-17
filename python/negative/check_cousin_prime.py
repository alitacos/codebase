def check_cousin_prime(yy, max_value):# did not really work as expected. returns TypeError
    """Check if a number is a cousin prime."""
    global cousinPrimeCount, nonprimes
    if (yy + 4 <= max_value and not nonprimes[yy] and not nonprimes[yy + 4]):
        cousinPrimeCount += 1
#example usage:
#check_cousin_prime(1)
# out: TypeError: check_cousin_prime() missing 1 required positional argument: 'max_value'
