def check_pythagorean_prime(yy):# missing import pythagoreanPrimeCount returns NameError
    """Check if a number is a Pythagorean prime."""
    global pythagoreanPrimeCount
    if (yy - 1) / 4 == ((yy - 1) / 4) // 1:
        pythagoreanPrimeCount += 1
#example usage:
#check_pythagorean_prime(1)
# out: NameError: name 'pythagoreanPrimeCount' is not defined
