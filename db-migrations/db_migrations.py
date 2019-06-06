import pg8000
import os
from typing import List

class DbMigration:
    """
    Execute migration for db initialization.
    migration() execute sqls in ../db-migrations/*.sql

    Attributes
    ----------
    dir_path: str
        absolute directory path contains migrations sql files ( relative path is  ../db-migrations)
    conn : pg8000.Connection
        database connection for migration.
        if migration() is called, it will be closed.
    """
    def __init__(self, host: str, port: str, user: str, password: str, database: str):
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.conn = pg8000.connect(host=host, port=port, user=user, password=password, database=database)

    def __get_migrations(self) -> List[str]:
        migration_sqls = []
        for filename in os.listdir(self.dir_path):
            # TODO: filter filename which have sql ext
            if filename.split(".")[1] == "sql":
                f = open(self.dir_path + "/" + filename)
                migration_sqls.append(f.read())
        return migration_sqls

    def migration(self):
        """
        migrate database with db-migrations/*.sql
        """
        cur = self.conn.cursor()
        sqls = self._DbMigration__get_migrations()
        for sql in sqls:
            cur.execute(sql)
        self.conn.commit()
        self.conn.close()
