import mysql.connector

user = 'root',
password = '123456',
host = 'localhost',
port = '3306',
database = 'tv_drama_resys'


class MysqlDb(object):
    def __init__(self):
        self.cnx = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            database=database
        )
        self.cursor = self.cnx.cursor()

    def close(self):
        self.cursor.close()
        self.cnx.close()

    def commit(self):
        self.cnx.commit()

    def insert_drama(self, drama):
        self.cursor.execute(
            'insert into meiju_drama(id, title_cn, title_en, image, country, duration, pubdate, '
            'year, language, website, tv, episodes, summary, avg_rating, num_raters) '
            'values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
            [drama.id, drama.title_cn, drama.title_en, drama.image, drama.country,
             drama.duration, drama.pubdate, drama.year, drama.language, drama.website,
             drama.tv, drama.episodes, drama.summary, drama.avg_rating, drama.num_raters])

    def insert_director(self, director_list):
        for director in director_list:
            self.cursor.execute(
                'insert into meiju_director(drama_id, name) values(%s, %s)', [director.drama_id, director.name])

    def insert_writer(self, writer_list):
        for writer in writer_list:
            self.cursor.execute(
                'insert into meiju_writer(drama_id, name) values(%s, %s)', [writer.drama_id, writer.name])

    def insert_cast(self, cast_list):
        for cast in cast_list:
            self.cursor.execute(
                'insert into meiju_cast(drama_id, name) values(%s, %s)', [cast.drama_id, cast.name])

    def insert_type(self, drama_id, drama_type_list):
        for drama_type in drama_type_list:
            type_id = self.return_typeid_if_exists(drama_type)
            if type_id == 0:
                self.cursor.execute('insert into meiju_type(type) values(%s)', [drama_type.type])
                type_id = self.return_typeid_if_exists(drama_type)
            self.insert_drama_to_type(drama_id, type_id)

    def insert_drama_to_type(self, drama_id, type_id):
        self.cursor.execute(
            'insert into meiju_drama_types(dramatype_id, drama_id) values(%s, %s)', [drama_id, type_id])

    def return_typeid_if_exists(self, drama_type):
        self.cursor.execute('select * from meiju_type where type = %s', [drama_type.type])
        if self.cursor.rowcount > 0:
            row = self.cursor.fetchone()
            return row[0]
        else:
            return 0

    def insert_drama_all(self, drama, director_list, writer_list, cast_list, drama_type_list):
        self.insert_drama(drama)
        self.insert_cast(cast_list)
        self.insert_director(director_list)
        self.insert_writer(writer_list)
        self.insert_type(drama.id, drama_type_list)

        self.commit()
        self.close()
