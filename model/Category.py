from db import db
from utils.GeneralUtils import generate_uuid


class CategoryModel(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    categoryImageUrl = db.Column(db.String(250), nullable=False)

    def __init__(self, name, categoryImageUrl):
        self.name = name
        self.categoryImageUrl = categoryImageUrl
        self.category_id = generate_uuid()

    def __str__(self):
        f"""<Category: {self.name} | {self.categoryImageUrl} >"""

    def json(self):
        return {
            "categoryId": self.category_id,
            "name": self.name,
            "imageUrl": self.categoryImageUrl
        }

    @classmethod
    def find_by_category_name(cls, name: str) -> 'CategoryModel':
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_uuid(cls, categoryId: str) -> 'CategoryModel':
        return cls.query.filter_by(category_id=categoryId).first()

    @classmethod
    def find_all_categories(cls):
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
