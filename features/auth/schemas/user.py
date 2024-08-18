def userSchema(item):
    return {
        **item,
        '_id': str(item['_id'])
    }