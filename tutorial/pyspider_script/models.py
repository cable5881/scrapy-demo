class Drama(object):
    def __init__(self, _id, image, country, title_en, duration, pubdate, year,
                 episodes, avg_rating, num_raters, title_cn=None, language=None,
                 website=None, tv=None, summary=None):
        self.id = _id
        self.title_cn = title_cn
        self.title_en = title_en
        self.image = image
        self.country = country
        self.duration = duration
        self.pubdate = pubdate
        self.year = year
        self.language = language
        self.website = website
        self.tv = tv
        self.episodes = episodes
        self.summary = summary
        self.avg_rating = avg_rating
        self.num_raters = num_raters


class Director(object):
    def __init__(self, drama_id, name):
        self.drama_id = drama_id
        self.name = name


class Writer(object):
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
