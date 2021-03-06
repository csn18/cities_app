import math
import time
from os import environ as env

import mysql.connector
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/task1')
def index1():
    return render_page(request.path)


@app.route('/task2')
def index2():
    return render_page(request.path)


@app.route('/task3')
def index3():
    return render_page(request.path)


@app.route('/task4')
def index4():
    return render_page(request.path)


@app.route('/task5')
def index5():
    return render_page(request.path)


@app.route('/task6')
def index6():
    return render_page(request.path)


@app.route('/task7')
def index7():
    return render_page(request.path)


@app.route('/ajaxFunction')
def page():
    page_id = request.args.get('pageId', 1)
    search_box = request.args.get('text', '')
    if search_box:
        country = query_db(f"SELECT id FROM countries WHERE country LIKE '{search_box}%' ORDER BY country")[0]
    else:
        country = request.args.get('countryId', 1)
        country = query_db(f"SELECT id FROM countries WHERE id LIKE '{country}%' ORDER BY country")[0]
    pages_and_cities = pagination(page_id, country)
    result = {'pageCount': pages_and_cities['pages_count'], 'cities': pages_and_cities['id_cities_db'],
              'countryId': country}
    return jsonify(result)


def pagination(page_id, country):
    cities_count = query_db(f'SELECT COUNT(*) FROM cities WHERE country_id = {country}')[0]
    page_split = 5
    limit_page = (page_split * (int(page_id) - 1), 5)
    pages_count = math.ceil(cities_count / page_split)

    id_cities_db = query_db(
        f'SELECT city FROM cities WHERE country_id = {country} LIMIT {limit_page[0]}, {limit_page[1]}')

    result = {'id_cities_db': id_cities_db, 'pages_count': pages_count}
    return result


def render_page(html_template):
    countries = query_db('SELECT country FROM countries')
    id_countries_db = query_db('SELECT id, country FROM countries')
    country = int(request.args.get('countries_id', 1))
    query = request.args.get("q")
    if query:
        country = \
            query_db(f'SELECT id FROM countries WHERE LOWER(country) LIKE "{query}%" ORDER BY country')[0]
    page_id = int(request.args.get('page', 1))
    pages_and_cities = pagination(page_id, country)

    return render_template(f"main{html_template}.html",
                           countries=countries,
                           id_countries=id_countries_db,
                           id_cities=pages_and_cities['id_cities_db'],
                           page=page_id,
                           country=country,
                           pages_count=pages_and_cities['pages_count'],
                           q=query
                           )


def db_connect():
    retry_count = int(env.get('DB_RETRY_COUNT', 5))
    for i in range(retry_count):
        try:
            return mysql.connector.connect(
                user=env.get('DB_USER', 'root'),
                password=env.get('DB_PASSWORD', 'root'),
                host=env.get('DB_HOST', '127.0.0.1'),
                database=env.get('DB_DATABASE', 'cities_app')
            )
        except mysql.connector.errors.InterfaceError:
            time.sleep(4)
    raise mysql.connector.errors.InterfaceError(msg='Database start timeout exceeded')


def query_db(query):
    cursor = mydb.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    result = [i[0] if len(i) == 1 else i for i in result]
    return result


if __name__ == '__main__':
    mydb = db_connect()
    app.run(debug=env.get('DEBUG', 'True'),
            host=env.get('SERVER_HOST', '0.0.0.0'),
            port=env.get('SERVER_PORT', '5000'))
