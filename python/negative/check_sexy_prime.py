
def check_sexy_prime(yy, max_value):# did not really work as expected. returns TypeError and the 'sexy' definition makes no sence
    """Check if a number is a sexy prime."""
    global sexyPrimeCount, nonprimes
    if (yy + 6 <= max_value and not nonprimes[yy] and not nonprimes[yy + 6]):
        sexyPrimeCount += 1
#example usage:
#check_sexy_prime(1)
# out: TypeError: check_sexy_prime() missing 1 required positional argument: 'max_value'
