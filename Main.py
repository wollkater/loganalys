
import json
import psycopg2

config_file = open("config.json").read()
config_json = json.loads(config_file)
db_host = config_json.get("db_host")
db_port = config_json.get("db_port")
db_name = config_json.get("db_name")
db_user = config_json.get("db_user")
db_password = config_json.get("db_password")

connection = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host, port=db_port)

most_views_query = """
select title, views
  FROM articlesViewCount
  limit 3
"""

most_popular_author_query = """
select authors.name, sum(views) as views
  FROM articlesViewCount
  join authors on articlesViewCount.author = authors.id
GROUP BY authors.name
ORDER BY views DESC
"""

error_prone_days_query = """
select to_char(time::date, 'Mon DD, YYYY'),
  count(case when status not like '200%' then 1 end) "error",
  count(case when status like '200%' then 1 end) ok,
  round(((count(case when status not like '200%' then 1 end)::float / count(*))*100)::NUMERIC, 1) as percentage
  from log
GROUP BY time::date
having (count(case when status not like '200%' then 1 end)::float / count(*))*100 > 1
"""


def execute(sql, variables=None):
    crs = connection.cursor()
    try:
        crs.execute(sql, variables)
        connection.commit()
        return crs
    except psycopg2.Error as e:
        connection.rollback()
        print(e.diag.message_primary)


def get_articles_ordered_by_views():
    print(u"What are the most popular three articles of all time? ")
    for rec in execute(most_views_query):
        print(u"\u2022 {} \u2014 {} views".format(rec[0], rec[1]))


def get_most_popular_authors():
    print(u"Who are the most popular article authors of all time?")
    for rec in execute(most_popular_author_query):
        print(u"\u2022 {} \u2014 {} views".format(rec[0], rec[1]))


def get_error_prone_days():
    print(u"On which days did more than 1% of requests lead to errors?")
    for rec in execute(error_prone_days_query):
        print(u"\u2022 {} \u2014 {}% errors".format(rec[0], rec[3]))


get_articles_ordered_by_views()

get_most_popular_authors()

get_error_prone_days()

