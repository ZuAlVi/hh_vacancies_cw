import psycopg2


class DBManager:

    def __init__(self, db_name: str, params: dict):
        self.database_name = db_name
        self.params = params

    def get_companies_and_vacancies_count(self) -> list[tuple] or str:
        """Метод для получения компаний и количества вакансий у компании."""

        try:
            conn = psycopg2.connect(database=self.database_name, **self.params)
            with conn.cursor() as cur:
                cur.execute('SELECT company_name, COUNT(vacancy_id) '
                            'FROM companies '
                            'JOIN vacancies USING (company_id) '
                            'GROUP BY company_name '
                            'ORDER BY company_name')
                result = cur.fetchall()

        except (Exception, psycopg2.DatabaseError) as e:
            return e

        conn.close()
        return result

    def get_all_vacancies(self) -> list[tuple] or str:
        """Метод для получения всех вакансий."""

        try:
            conn = psycopg2.connect(database=self.database_name, **self.params)
            with conn.cursor() as cur:
                cur.execute('SELECT title_vacancy, company_name, salary, vacancies.link '
                            'FROM vacancies '
                            'JOIN companies USING (company_id);')

                result = cur.fetchall()

        except (Exception, psycopg2.DatabaseError) as e:
            return e

        conn.close()
        return result

    def get_avg_salary(self) -> list[tuple] or str:
        """Метод для получения средней зарплаты по всем вакансиям у каждой компании."""

        try:
            conn = psycopg2.connect(database=self.database_name, **self.params)
            with conn.cursor() as cur:
                cur.execute('SELECT company_name, round(AVG(salary)) AS average_salary '
                            'FROM companies '
                            'JOIN vacancies USING (company_id) '
                            'GROUP BY company_name;')

                result = cur.fetchall()

        except (Exception, psycopg2.DatabaseError) as e:
            return e

        conn.close()
        return result

    def get_vacancies_with_higher_salary(self) -> list[tuple] or str:
        """Метод для получения вакансий, у которых зарплата выше среднего значения."""

        try:
            conn = psycopg2.connect(database=self.database_name, **self.params)
            with conn.cursor() as cur:
                cur.execute('SELECT * FROM vacancies '
                            'WHERE salary > (SELECT AVG(salary) FROM vacancies);')

                result = cur.fetchall()

        except (Exception, psycopg2.DatabaseError) as e:
            return e

        conn.close()
        return result

    def get_vacancies_with_keyword(self, keyword: str) -> list[tuple] or str:
        """Метод возвращает вакансии, где keyword есть в названии вакансии."""

        try:
            conn = psycopg2.connect(database=self.database_name, **self.params)
            with conn.cursor() as cur:
                cur.execute(f"""
                SELECT * 
                FROM vacancies
                WHERE lower(title_vacancy) LIKE '%{keyword}%'
                OR lower(title_vacancy) LIKE '%{keyword}'
                OR lower(title_vacancy) LIKE '{keyword}%'""")

                result = cur.fetchall()

        except (Exception, psycopg2.DatabaseError) as e:
            return e

        conn.close()
        return result
