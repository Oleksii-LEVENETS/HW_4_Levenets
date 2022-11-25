"""
Task1.
У прикладених файлах до ДЗ, є два файли users_db.json, company_db.json. Для виконання завдань вам потрібно прочитати
дані файли, використовуючи модуль json.
В json ключ пари -- це ід відповідного об'єкта (user_id, company_id).
В прикладених файлах також є файл exception.py. Імпортуйте ексепшини з цього файлу.
1. Реалізуйте функцію для отримання міста, в якому зареєстрована компанія:
def get_company_city(company_id):
    pass
Якщо компанії по такому ід не існує, згенеруйте відповідний ексепшин.
2. Реалізуйте декоратор, для get_company_city, який буде приймати додатковий параметр user_id і перевіряти
чи має юзер доступ до компанії. Юзер має доступ до компанії якщо ід компанії записаний в його поле companies.
Без декоратора виклик функції відбувався з передачею одного аргумента get_company_city(company_id)
Після додавання декоратора виклик повинен виглядати таким чином get_company_city(user_id, company_id)
Якщо юзера не існує — згенеруйте відповідний ексепшин.
Якщо юзер не має доступу до компанії — згенеруйте відповідний ексепшин.
3. Реалізуйте декоратор exception_handler. Даний декоратор повинен подавити всі ексепшини які генеруються
(декоратор повинен також опрацьовувати ексепшини, які генеруються іншими декораторами).
4. Реалізуйте декоратор по підрахунку часу виконання функції.
Огорніть всіма написаними раніше декораторами функцію get_company_city.
Використовуючи модуль logging, додайте логування ексепшинів, логування старту роботи основної функції,
а також логування часу виконання функції.

"""
from exceptions import NotFound, NoAccess
import json
import logging
import time

with open("users_db.json") as users_file:
    users_dict = json.load(users_file)
# print("users_dict: ", users_dict)

with open("company_db.json") as company_file:
    company_dict = json.load(company_file)
# print("company_dict: ", company_dict)

FORMAT_MESSAGE = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG)
logger = logging.Logger(__name__)
s_handler = logging.StreamHandler()
s_handler.setLevel(logging.DEBUG)
s_handler.setFormatter(logging.Formatter(FORMAT_MESSAGE))
logger.addHandler(s_handler)

f_handler = logging.FileHandler("logs.log", mode="w")
f_handler.setLevel(logging.ERROR)
f_handler.setFormatter(logging.Formatter(FORMAT_MESSAGE))
logger.addHandler(f_handler)


def timer_counter(func):
    def wrap_timer_counter(*args, **kwargs):
        t1 = time.time()  # or perf_counter_ns()
        func_res = func(*args, **kwargs)
        t2 = time.time()  # or time.perf_counter_ns()
        time_execution = t2 - t1
        logger.debug(f"Time execution is {round(time_execution, 7)}s")
        return func_res
    return wrap_timer_counter


def exception_handler(func):
    def wrap_exception_handler(*args, **kwargs):
        try:
            func_res = func(*args, **kwargs)
            return func_res
        except (NotFound, NoAccess, Exception) as e:
            logger.exception("Exception occurred.")
    return wrap_exception_handler


def decor_user_id(func):
    def wrap_decor_user_id(user_id=None, company_id=None):
        func_res = func(company_id)
        if user_id not in users_dict:
            raise NotFound
        
        list_user_companies = (users_dict.get(user_id)).get("companies")
        if int(company_id) not in list_user_companies:
            raise NoAccess
        return func_res
    return wrap_decor_user_id


@timer_counter  # execution time of a decorator-wrapped main function and logging their ALL execution time
@exception_handler
@decor_user_id
def get_company_city(company_id):
    """To get the city in which the company is registered.
    
    The value must be string-number, like '9'."""
    logger.info("Execution 'get_company_city()' starts")
    if company_id in company_dict:
        company_city = (company_dict.get(company_id)).get("city")
        return company_city
    else:
        raise NotFound


print(get_company_city(user_id='1', company_id='1'))
