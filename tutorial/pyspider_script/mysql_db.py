import mysql.connector


class MysqlDb(object):
    def __init__(self):
        self.cnx = mysql.connector.connect(
            user='root',
            password='123456',
            host='localhost',
            port='3306',
            database='tv_drama_resys'
        )
        self.cursor = self.cnx.cursor(buffered=True)

    def close(self):
        self.cursor.close()
        self.cnx.close()

    def commit(self):
        self.cnx.commit()

    # self, _id, title_en, title_cn, image, seasons_count, year, episodes, website
    # summary, avg_rating, , current_season, douban_url, aka
    def insert_drama(self, drama):
        self.cursor.execute(
            'insert into meiju_drama(id, title_cn, title_en, image, seasons_count, year, '
            'episodes, summary, avg_rating, current_season, douban_url, alternate_name) '
            'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            [drama.id, drama.title_cn, drama.title_en, drama.image, drama.seasons_count, drama.year,
             drama.episodes, drama.summary, drama.avg_rating, drama.current_season,
             drama.douban_url, drama.aka])

    def insert_director(self, drama_id, director_list):
        for director in director_list:
            self.cursor.execute(
                'insert into meiju_director(drama_id, name) values(%s, %s)', [drama_id, director['name']])

    def insert_cast(self, drama_id, cast_list):
        for cast in cast_list:
            print(cast)
            self.cursor.execute(
                'insert into meiju_cast(drama_id, name) values(%s, %s)', [drama_id, cast['name']])

    def insert_type(self, drama_id, drama_type_list):
        for drama_type in drama_type_list:
            type_id = self.return_typeid_if_exists(drama_type)
            if type_id == 0:
                self.cursor.execute('insert into meiju_type(type) values(%s)', [drama_type])
                type_id = self.return_typeid_if_exists(drama_type)
            self.insert_drama_to_type(drama_id, type_id)

    def insert_drama_to_type(self, drama_id, type_id):
        self.cursor.execute(
            'insert into meiju_drama_types(dramatype_id, drama_id) values(%s, %s)', [type_id, drama_id])

    def return_typeid_if_exists(self, drama_type):
        self.cursor.execute('select * from meiju_type where type = %s', [drama_type])
        if self.cursor.rowcount > 0:
            row = self.cursor.fetchone()
            return row[0]
        else:
            return 0

    def insert_drama_all(self, drama, director_list, cast_list, drama_type_list):
        self.insert_drama(drama)
        self.insert_cast(drama.id, cast_list)
        self.insert_director(drama.id, director_list)
        self.insert_type(drama.id, drama_type_list)

        self.commit()
        self.close()


db = MysqlDb()
