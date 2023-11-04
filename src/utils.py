import psycopg2
import requests

from config import config


def get_employers_and_vacancies(data: list) -> list:
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


def create_database(name: str, params: dict) -> None:
    """Функция создает базу двнных.
    Если база данных с таким названием уже существует,
    то удаляет ее.
    Принимает на вход название базы данных и параметры для подключения."""
    conn = psycopg2.connect(database='postgres', **params)
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute('select * from pg_database')
        all_databases = cur.fetchall()
        for item in all_databases:
            if item[1] == name:
                cur.execute(f'DROP DATABASE {name}')
                break
        cur.execute(f'CREATE DATABASE {name}')

    conn.close()
