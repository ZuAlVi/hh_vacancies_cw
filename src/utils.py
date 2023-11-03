import requests


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
