def check_euclid_prime(yy):# is not working as expected. returns NameError
    """Check if a number is an Euclid prime."""
    global euclidPrimeCount, Euclid_Primes, nonprimes
    product = 1
    i = 2
    while product < yy:
        if not nonprimes[i]:
            product *= i
        if product + 1 == yy:
            if yy not in Euclid_Primes:
                euclidPrimeCount += 1
                Euclid_Primes.append(yy)
            return True
        i += 1
    return False
#example usage:
#check_euclid_prime(0)
# out: NameError: name 'nonprimes' is not defined
