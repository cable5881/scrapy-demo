class Drama(object):
    def __init__(self, _id, image, title_en, year, episodes,
                 avg_rating, seasons_count, current_season, title_cn=None,
                 summary=None, douban_url=None, aka=None):
        self.id = _id
        self.title_cn = title_cn
        self.title_en = title_en
        self.image = image
        # self.duration = duration
        self.year = year
        self.episodes = episodes
        self.summary = summary
        self.seasons_count = seasons_count
        self.current_season = current_season
        self.aka = aka
        self.douban_url = douban_url
        self.avg_rating = avg_rating


class Director(object):
    def __init__(self, drama_id, name):
        self.drama_id = drama_id
        self.name = name


class Cast(object):
    def __init__(self, drama_id, name):
        self.drama_id = drama_id
        self.name = name


class DramaType(object):
    def __init__(self, _type):
        self.type = _type
