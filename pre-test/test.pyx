cpdef long long last_way(n):
    '''Last potential way to achive n'''
    way = ''
    for i in range(n):
        way += '1'
    return int(way)


cpdef long long initial_way(n):
    '''First potential way to achieve n'''
    way = ''
    six_steps = n // 6
    fillings = n % 6
    for six in range(six_steps):
        way += '6'
    if fillings is not 0: way += str(fillings)
    return int(way)


def calc_possible_ways(long long n):
    cdef long long way = initial_way(n)
    cdef long long ways = 0
    cdef long long i

    for i in range(last_way(n)):
        way += 1
        if sum(list(map(int, str(way)))) == n:
            if not any(number in str(way) for number in ['7', '8', '9', '0']):
                print(way)
                ways+=1

        if way == last_way(n):
            ways+=1
            break
    print('last_way: ', last_way(n))
    print('initial_way: ', initial_way(n))
    print('n: ', n)
    return ways
from itertools import count

cpdef long long counter(long long n):
    cdef long long way = initial_way(n)
    cdef long long ways = 0

    cdef long long i

    print('initial way: ', way)
    print('last way: ', last_way(n))

    for i in range(last_way(n)):
        way += 1
        print(way)
        ways += 1
        
        if way == last_way(n):
            print('last way reached', way)
            print(ways)
            break
    return ways


