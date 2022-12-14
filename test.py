import math


# def shrink_to_prime(x):
#     prime_factorization = []
#     while x % 2 == 0:
#         x //= 2
#         prime_factorization.append(2)

#     i = 3
#     while i < math.ceil(math.sqrt(x)):
#         if x % i == 0:
#             x //= i
#             prime_factorization.append(i)
#         else:
#             i += 2
        
#     return x, prime_factorization + [x]

def factors(x):
    f = {1, x}
    for i in range(2, math.ceil(math.sqrt(x))):
        if x % i == 0:
            f.add(i)
            f.add(x//i)
    return f


def commonfactors(x, y):
    fx = factors(x)
    fy = factors(y)

    cf = list(fx & fy)
    cf.sort() 
    return cf

print(commonfactors(24, 128))