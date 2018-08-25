
# from functools import reduce
#
# L = [3, 5, 7, 9]
# def fn(n):
#     return n
# def fx(x, y):
#     return x * y
# def prod():
#     return reduce(fx, map(fn, [3, 5, 6, 7]))
# print(prod())

# from functools import reduce
#
# CHAR_TO_FLOAT = {
#     '0': 0,
#     '1': 1,
#     '2': 2,
#     '3': 3,
#     '4': 4,
#     '5': 5,
#     '6': 6,
#     '7': 7,
#     '8': 8,
#     '9': 9,
#     '.': -1
# }
# def str2int(s):
#     ints = map(lambda ch : CHAR_TO_FLOAT[ch], s)
#     return reduce(lambda x, y: x * 10 + y, ints)
# def str2float(s):
#     nums = map(lambda ch : CHAR_TO_FLOAT[ch], s)
#     point = 0
#     def to_float(f, n):
#         nonlocal point
#         if n == -1:
#             point = 1
#             return f
#         if point == 0:
#             return f * 10 + n
#         else:
#             point *= 10
#             return f + n / point
#     return reduce(to_float, nums, 0.0)
#
# print(str2int('12345'))
# print(str2float('123.45'))

# def is_odd(n):
#     return n % 2 == 1
#
# print(list(filter(is_odd, [1, 2, 3, 4, 5, 6, 7])))

# def not_empty(s):
#     return s and s.strip()
# print(list(filter(not_empty, ['A', '', 'B', ' ', 'C'])))

