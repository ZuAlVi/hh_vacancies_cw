# Данный проект является парсером вакансий с сайта `headhunter.ru` с помощью API.
# Данные сохраняются в базу данных `PostgreSQL`.

# Для запуска необходимо:
# 1.Клонировать проект. Для этого терминале ввести команду:
```
git clone git@github.com:ZuAlVi/hh_vacancies_cw.git
```
# 2. Установить Poetry. Для этого в терминале ввести команду:
```
pip install poetry
```
# 3. Активировать Poetry. Для этого в терминале ввести команду:
```
poetry shell
```
# 4. Установить зависимости. Для этого в терминале ввести команду:
```
poetry install
```

## В модуле database.ini, в секции postgresql ввести свои данные

  1) host
    
     Ввести свой host, по умолчанию является localhost.
  2) user
     
     Ввести имя пользователя, используемого в СУБД.
  3) password
  
     Ввести пароль у пользователя в СУБД.
  4) port
 
     Ввести свой port, по умолчанию 5432. 


# В модуле main.py переменной `database_name` необходимо задать имя базы данных.

# Для работы с базой данных создан класс DBManager.

Методы класса DBManager:

* `get_companies_and_vacancies_count`

    Метод для получения компаний и количества вакансий у каждой компании.

* `get_all_vacancies`

    Метод для получения названия компании, названии вакансии, зарплату и ссылку на вакансию.

* `get_avg_salary`
 
    Метод для получения названия компании и средней зарплаты у компании по всем вакансиям.

* `get_vacancies_wth_highest_salary`
 
    Метод для получения всех вакансий, у которых зарплата выше средней.

* `get_vacancies_with_keyword`
 
    Метод для получения вакансий, по используемому ключевому слову в названии вакансии.