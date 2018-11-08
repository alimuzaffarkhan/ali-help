import json


class BaseParser(object):

    def __init__(self, filename):
        self.content = json.loads(open(filename, 'rb').read())

    def dig(self, row, dot_notation):
        value = row
        paths = dot_notation.split('.')
        for path in paths:
            try:
                value = value[path]
            except KeyError:
                pass
            except TypeError:
                method = getattr(self, path, None)
                if method:
                    value = method(value)
        return value

    def parse_row(self, raw_row):
        row = {}
        for fieldname, notation in self.FIELDS.items():
            row[fieldname] = self.dig(raw_row, notation)
        return row

    def parse(self):
        return [
            self.parse_row(row)
            for row in self.content['data']
        ]


class FileOneParser(BaseParser):

    FIELDS = {
        'ali': 'top.inner.nested',
        'highest_paid': 'daily_rates.get_highest'
    }

    def get_highest(self, values):
        max_rate = 0
        entry = None
        for value in values:
            if value['rate'] > max_rate:
                entry = value
        return entry.get('name', None)


parser = FileOneParser('file1.json')
print parser.parse()
