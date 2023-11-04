from config import config
from src.class_db_manager import DBManager
from src.utils import create_database, create_tables, fill_database, get_data
from pprint import pprint

if __name__ == '__main__':
    employers = [
        1740,  # Яндекс
        78638,  # Тинькофф
        3776,  # МТС
        2180,  # Озон
        49357,  # Магнит
        2748,  # Ростелеком
        4880,  # Детский мир
        2523,  # МВидео - Эльдорадо
        3127,  # Мегафон
        4934  # Билайн
    ]

    database_name = 'Введите название базы данных'
    params = config()

    create_database(database_name, params)
    create_tables(database_name, params)
    fill_database(get_data(employers), database_name, params)

    db = DBManager(database_name, params)
    # pprint(db.get_companies_and_vacancies_count())
    # pprint(db.get_all_vacancies())
    # pprint(db.get_avg_salary())
    # pprint(db.get_vacancies_with_higher_salary())
    # keyword = input('Введите слово для поиска: ')
    # pprint(db.get_vacancies_with_keyword(keyword))
