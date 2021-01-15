data = []


def add_entries(*entries):
    data.extend(entries)


def search_entries(query):
    return filter(lambda x: query in x['title'], data)
