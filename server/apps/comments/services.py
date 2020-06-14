from html import escape
from sqlite3 import Connection
from typing import List, Optional, Dict

from core.exceptions import BadRequest
from core.shortcuts import get_html
from server.db import get_connection, dict_row_factory


def get_comment_add_content(template_name: str) -> str:
    """
    Получение контента для формы добавления коменнтария
    """
    db: Connection = get_connection(row_factory=dict_row_factory)
    regions = db.execute("SELECT id, name FROM regions;").fetchall()
    db.close()

    option_regions = ''.join(
        ['<option value="%s">%s</option>' % (region['id'], region['name']) for region in regions]
    )

    content: str = get_html(template_name).format(option_regions=option_regions)

    return content


def check_validate_form_data(comment) -> Optional[bool]:
    """
    Проверка валидности полученных данных с формы
    """
    if any([
        not comment['last_name'][0].strip(),
        not comment['first_name'][0].strip(),
        not comment['comment'][0].strip()
    ]):
        raise BadRequest("Не заполнено обязательное поле")

    return True


def insert_comment(comment: Dict):
    """
    Добавление в таблицу `comments нового комментария  `comment
    """
    sql_insert_comment: str = """
    INSERT INTO comments(last_name, first_name, patronymic, city_id, phone, email, comment)
    VALUES(?, ?, ?, ?, ?, ?, ?);
    """

    last_name = comment['last_name'][0].strip()
    first_name = comment['first_name'][0].strip()
    patronymic = comment['patronymic'][0].strip() if "patronymic" in comment else ""

    raw_city: Optional[List[str]] = comment.get('city')
    try:
        city_id = int(raw_city[0])
    except (ValueError, IndexError):
        city_id = None

    phone = comment['phone'][0].strip() if "phone" in comment else ""
    email = comment['email'][0].strip() if "email" in comment else ""
    comment_text = comment['comment'][0].strip()

    raw_sql_params = [last_name, first_name, patronymic, city_id, phone, email, comment_text]
    parameters = [escape(param) if type(param) == str else param for param in raw_sql_params]

    db: Connection = get_connection()
    db.execute(sql_insert_comment, parameters)
    db.commit()
    db.close()


def get_statistic_content(template_name, region_id: int = None) -> str:
    """
    Получение контента со статистики по регионам для модуля статистики
    если указан `region_id получение контента статистики по городам региона
    """
    region_fields = ('region_link', 'count')
    city_fields = ("region_name", "name", "count")
    headers = ("Регион", "Количество")
    headers_city = ("Регион", "Город", "Количество")

    if region_id:
        db = get_connection(row_factory=dict_row_factory)
        cities: List[dict] = db.execute("""SELECT
                                               c.name as name,
                                               r.name AS region_name,
                                               COUNT(c.id) as count 
                                             FROM comments comm
                                             LEFT JOIN cities c ON c.id = comm.city_id
                                             LEFT JOIN regions r on r.id = c.region_id
                                             WHERE r.id = %s
                                             GROUP BY c.id
                                        """ % region_id
                                        ).fetchall()
        db.close()

        if cities:
            table_title = f"Статистика по городам"
            table_headers = "".join(["<th>%s</th>" % header for header in headers_city])
            table_body = "".join(["""<tr align="center" >%s</tr>""" % "".join(["<td>%s</td>" % city[field]
                                                                               for field in city_fields])
                                  for city in cities])
        else:
            table_title = f"Нет данных по городам"
            table_headers = ""
            table_body = ""

    else:
        db = get_connection(row_factory=dict_row_factory)
        regions: List[dict] = db.execute("""SELECT
                                               r.id as id,
                                               r.name AS name,
                                               COUNT(r.id) as count 
                                             FROM comments comm
                                             LEFT JOIN cities c ON c.id = comm.city_id
                                             LEFT JOIN regions r on r.id = c.region_id
                                             GROUP BY r.id
                                             HAVING COUNT(r.id) > 5"""
                                         ).fetchall()
        db.close()

        if regions:
            table_title = "Статистика по регионам"
            table_headers = "".join(["<th>%s</th>" % header for header in headers])

            for region in regions:
                region['region_link'] = '<a href="/stat?id=%s">%s</a>' % (region["id"], region['name'])

            table_body = "".join(["""<tr align="center" >%s</tr>""" % "".join(["<td>%s</td>" % region[field]
                                                                               for field in region_fields])
                                  for region in regions])
        else:
            table_title = "Нет данных для подсчета статистики"
            table_headers = ""
            table_body = ""

    content: str = get_html(template_name).format(table_title=table_title, table_headers=table_headers,
                                                  table_body=table_body)
    return content


def get_comment_view_content(template_name: str) -> str:
    """
    Получение контента для модуля просмотра списка комментариев
    """
    comment_fields = (
        'last_name',
        'first_name',
        'patronymic',
        'region',
        'city',
        'phone',
        'email',
        'comment',
        'delete_btn'
    )
    headers = (
        "Фамилия", "Имя", "Отчество", "Регион",
        "Город", "Телефон", "Эл. почта", "Комментарий", "Удалить"
    )

    db: Connection = get_connection(row_factory=dict_row_factory)
    comments: List[dict] = db.execute("""SELECT 
                                            comm.id as id,
                                            comm.first_name AS %s,
                                            comm.last_name AS %s,
                                            IFNULL (comm.patronymic, "") AS %s,
                                            IFNULL (r.name, "") AS %s,
                                            IFNULL (c.name, "") AS %s,
                                            IFNULL (comm.phone, "") AS %s,
                                            IFNULL (comm.email, "") AS %s,
                                            comm.comment AS %s
                                          FROM comments comm
                                          LEFT JOIN cities c ON comm.city_id = c.id
                                          LEFT JOIN regions r on c.region_id = r.id""" %
                                      comment_fields[:-1]).fetchall()
    db.close()

    if comments:

        table_title = "Комментарии"
        table_headers = "".join(["<th>%s</th>" % header for header in headers])

        for comment in comments:
            comment[
                "delete_btn"] = """<button name="btn_delete" comment_id="%s" onclick="comm_delete(this);">Удалить</button>""" % \
                                comment['id']
        table_body = ''.join(['<tr>%s</tr>' % ''.join(['<td>%s</td>' % comment[field] for field in comment_fields])
                              for comment in comments]
                             )

    else:
        table_title = """<h1 align="center" style="font-weight: bold">Нет комментариев для просмотра</h1>"""
        table_headers = ""
        table_body = ""

    content: str = get_html(template_name).format(table_title=table_title, table_headers=table_headers,
                                                  table_body=table_body)

    return content


def delete_comment(comment_id: str):
    """
    Удаляет комментарий из таблицы `comments с `id == `comment_id
    """
    try:
        id = int(comment_id)
    except ValueError:
        raise ValueError("Получен не верный формат!")
    try:
        db: Connection = get_connection()
        db.execute("""DELETE FROM comments WHERE id = %s;""" % comment_id)
        db.commit()
        db.close()
    except:
        return False

    return True


def get_cities(region_id: str):
    """
    Получение списка городов из таблицы `cities, где `сities.region_id == `region_id
    :return: json со списком городов
    """
    db: Connection = get_connection(row_factory=dict_row_factory)
    cities: List[dict] = db.execute("""SELECT 
                                            c.id,
                                            c.name
                                       FROM cities c
                                       WHERE c.region_id = %s;""" % region_id).fetchall()
    db.close()
    return [(city['id'], city['name']) for city in cities]
