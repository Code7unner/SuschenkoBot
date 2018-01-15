# -*- coding: utf-8 -*-
class Gift:
    gift_id = 0
    sex = 0
    name = ""
    description = ""
    link = ""
    mark = 0.0
    mark_count = 0

    def __init__(self, gift_id, sex, name, description, link, mark, mark_count):
        self.gift_id = gift_id
        self.sex = sex
        self.name = name
        self.description = description
        self.link = link
        self.mark = mark
        self.mark_count = mark_count
