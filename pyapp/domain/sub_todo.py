import os
import pg8000

# Prod
DEFAULT_DBUSER="postgres"
DEFAULT_DBPASS=""
DEFAULT_DBHOST="localhost"
DEFAULT_DBPORT=5432
DEFAULT_DBNAME="postgres"

DBHOST = os.getenv('DB_HOST', DEFAULT_DBHOST)
DBPORT = os.getenv('DB_PORT', DEFAULT_DBPORT)
DBNAME = os.getenv('DB_NAME', DEFAULT_DBNAME)
DBUSER = os.getenv('DB_USER', DEFAULT_DBUSER)
DBPASS = os.getenv('DB_PASS', DEFAULT_DBPASS)

# todos apis
class Todo:
    def create_todo(self, todo):
        conn = pg8000.connect(host=DBHOST, port=DBPORT, user=DBUSER, password=DBPASS, database=DBNAME)
        cur = conn.cursor()
        cur.execute(
            "insert into todo (title, content, state_machine) values (%s, %s, 0)",
            (todo["title"], todo.get("content", "")))
        conn.commit()
        conn.close()
        return todo

    def update_todo(self, todo):
        conn = pg8000.connect(host=DBHOST, port=DBPORT, user=DBUSER, password=DBPASS, database=DBNAME)
        cur = conn.cursor()
        cur.execute(
            "update todo set title=%s, content=%s, state_machine=%s where id = %s",
            (todo["title"], todo["content"], todo["state_machine"], todo["id"]))
        conn.commit()
        conn.close()
        return todo

    def list_todo(self, params):
        conn = pg8000.connect(host=DBHOST, port=DBPORT, user=DBUSER, password=DBPASS, database=DBNAME)
        cur = conn.cursor()
        cur.execute(
            "select * from todo order by state_machine;"
        )
        results = cur.fetchall()
        resp = []
        for row in results:
            row_resp = {}
            for i, col in enumerate(cur.description):
                row_resp[col[0].decode("utf-8")] = row[i]
            resp.append(row_resp)
        conn.close()
        return resp

