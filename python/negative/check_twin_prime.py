def check_twin_prime(yy, max_value):# is not working as expected. returns NameError: name 'nonprimes' is not defined
    """Check if a number is a twin prime."""
    global twinPrimeCount, nonprimes
    if (yy + 2 <= max_value and not nonprimes[yy] and not nonprimes[yy + 2]):
        twinPrimeCount += 1
#example usage:
#check_twin_prime(1,10)
 
