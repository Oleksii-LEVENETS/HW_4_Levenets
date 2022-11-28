"""
На лекції ми робили декоратор, який перевіряв тип даних аргументів, які подавались в функцію.
В лекції був декоратор зі строго заданою кількістю аргументів. Хто бажає на додаткові бали, доробіть декоратор,
щоб він не залежав від кількості аргументів, що приймає функція. Додайте його в ДЗ в папку Task2.
"""

# Option with zip


def validate(*v_args):
    def decorator(func):
        def wrap(*f_args):
            zip_lists = zip(list(v_args), list(f_args))
            for i in zip_lists:
                if not isinstance(i[1], i[0]):
                    raise TypeError(f"type {i[1]}, the {int(list(f_args).index(i[1]) + 1)}-s "
                                    f"argument in function '{func.__name__}', expected {i[0]}, but got {type(i[1])}.")
            try:
                return func(*f_args)
            except TypeError as ex:
                print("Error!", ex)
        return wrap
    return decorator


@validate((int, float), (list, tuple))
def func_1(a, b):
    pass


@validate((list, tuple), (list, tuple), (int, float), (int, float), (int, float))
def func_2(a, b, c, d, e):
    pass


func_1(3, [8])
func_2((6,), [4], 8, 1, [0])

# # Option #1
# def validate(*args):
#     def decorator(func):
#         def wrap(*ar):
#             list_validate_arg = list(args)
#             list_func_arg = list(ar)
#             if len(list_validate_arg) != len(list_func_arg):
#                 raise ValueError("Check number of @validate()'s and/or number of function()'s arguments.")
#
#             for i in range(len(list_validate_arg)):
#                 val_i = list_validate_arg[i]
#                 func_i = list_func_arg[i]
#                 if not isinstance(func_i, val_i):  # noinspection PyTypeHints
#                     raise TypeError(f"""type {func_i}, the {int(list_func_arg.index(func_i) + 1)}-s \
# argument in function '{func.__name__}', expected {val_i}, but got {type(func_i)}.""")
#             return func(*ar)
#         return wrap
#     return decorator
#
#
# @validate((int, float), (list, tuple))
# def func_1(a, b):
#     pass
#
#
# @validate((list, tuple), (list, tuple), (int, float), (int, float), (int, float))
# def func_2(a, b, c, d, e):
#     pass
#
#
# func_1(3, (8,))
# func_2((6,), [4], 8, 1, (0,))
