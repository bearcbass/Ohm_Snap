from flask_pymongo import PyMongo


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = PyMongo(current_app).db

    return db


def add_file(file_name, file):
    file_doc = {"name": file_name, "data": file}
    return db.files.insert_one()
