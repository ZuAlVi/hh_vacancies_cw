import psycopg2
import requests


def get_data(data: list) -> list:
    """Функция принимает на вход список ID компаний с HH.RU.
    Возвращает список словарей"""
    result = []
    for item in data:
        url = f'https://api.hh.ru/employers/{item}'
        response_employer = requests.get(url).json()
        response_vacancies = requests.get(response_employer['vacancies_url']).json()
        result.append({
            'employer': response_employer,
            'vacancies': response_vacancies['items']
        })

    return result


def create_database(db_name: str, params: dict) -> None:
    """Функция создает базу данных.
    Если база данных с таким названием уже существует,
    то удаляет ее.
    Принимает на вход название базы данных и параметры для подключения."""
    conn = psycopg2.connect(database='postgres', **params)
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute('select * from pg_database')
        all_databases = cur.fetchall()
        for item in all_databases:
            if item[1] == db_name:
                cur.execute(f'DROP DATABASE {db_name}')
                break
        cur.execute(f'CREATE DATABASE {db_name}')

    conn.close()


def create_tables(db_name: str, params: dict) -> None:
    """
    Функция для создания таблиц в базе данных.
    Принимает в качестве аргументов имя базы данных и параметры для подключения.
    """
    conn = psycopg2.connect(database=db_name, **params)

    with conn.cursor() as cur:
        cur.execute('CREATE TABLE companies('
                    'company_id serial PRIMARY KEY,'
                    'company_name varchar(50) NOT NULL,'
                    'link varchar(200) NOT NULL)')

        cur.execute('CREATE TABLE vacancies('
                    'vacancy_id serial PRIMARY KEY,'
                    'company_id int REFERENCES companies (company_id) NOT NULL,'
                    'title_vacancy varchar(200) NOT NULL,'
                    'salary int,'
                    'link varchar(200) NOT NULL,'
                    'description text)')

    conn.commit()
    conn.close()


def format_salary(value):
    if value is not None:
        if value['from'] is not None and value['to'] is not None:
            return round((value['from'] + value['to']) / 2)
        elif value['from'] is not None:
            return value['from']
        elif value['to'] is not None:
            return value['to']


def fill_database(data: list, db_name: str, params: dict) -> None:
    """
    Функция для заполнения таблиц данными.
    Принимает в качестве аргументов список словарей,
    имя базы данных и параметры для подключения
    """
    conn = psycopg2.connect(database=db_name, **params)

    with conn.cursor() as cur:
        for item in data:
            cur.execute('INSERT INTO companies (company_name, link)'
                        'VALUES (%s, %s)'
                        'returning company_id',
                        (item['employer'].get("name"),
                         item['employer'].get("alternate_url")))

            company_id = cur.fetchone()[0]

            for part in item['vacancies']:
                salary = format_salary(part["salary"])
                cur.execute('INSERT INTO vacancies'
                            '(company_id, title_vacancy, salary, link, description)'
                            'VALUES (%s, %s, %s, %s, %s)',
                            (company_id,
                             part["name"],
                             salary,
                             part["alternate_url"],
                             part["snippet"].get("responsibility")))
    conn.commit()
    conn.close()

