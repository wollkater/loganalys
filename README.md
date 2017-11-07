###Install
Clone the repo and install Psycopg (http://initd.org/psycopg/docs/index.html)

###Run
First add the view from down below and update config.json according to your set up. Then run Main.py

##Views
    ```sql
    CREATE VIEW articlesViewCount AS
      select articles.author, articles.title, count(log.ip) as views
      FROM articles
      join log on log.path = '/article/' || articles.slug
      GROUP BY articles.id, articles.title
      ORDER BY views DESC;
    ```