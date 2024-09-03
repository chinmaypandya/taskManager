def requestSchema(item):
    return {
        **item,
        '_id': str(item['_id'])
    }