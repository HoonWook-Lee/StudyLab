from ninja import Schema

class BookSchema(Schema):
    title : str
    content : str
    date : str
    link : str