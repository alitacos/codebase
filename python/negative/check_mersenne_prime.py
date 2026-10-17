def check_mersenne_prime(yy):# is not working as expected. returns NameError
    """Check if a number is a Mersenne prime."""
    global mersennePrimeCount, Mersenne_Primes
    if log2(yy + 1) == log2(yy + 1) // 1:
        trial_factor = 2
        is_Mersenne = True
        while trial_factor < log2(yy + 1):
            if log2(yy + 1) % trial_factor == 0:
                is_Mersenne = False
                break
            trial_factor += 1
        if is_Mersenne:
            if yy not in Mersenne_Primes:
                Mersenne_Primes.append(yy)
                mersennePrimeCount += 1
#example usage:
#check_mersenne_prime(1)
# out: NameError: name 'log2' is not defined
