from db import db
from utils.GeneralUtils import generate_uuid


class FAQModel(db.Model):
    __tablename__ = "FAQs"
    id = db.Column(db.Integer, primary_key=True)
    faqId = db.Column(db.String(10), unique=True)
    title = db.Column(db.String(20), unique=True)
    message = db.Column(db.String(256), nullable=False)

    def __init__(self, title, message) -> None:
        self.title = title
        self.message = message
        self.faqId = generate_uuid()

    def __repr__(self):
        return f"< FAQ: {self.faqId} {self.title} {self.message} >"

    def json(self):
        return {
            "faqId": self.faqId,
            "title": self.title,
            "message": self.message,
        }

    @classmethod
    def find_by_uuid(cls, faqId: str) -> 'FAQModel':
        return cls.query.filter_by(faqId=faqId).first()

    @classmethod
    def find_by_title(cls, title: str) -> 'FAQModel':
        return cls.query.filter_by(title=title).first()

    @classmethod
    def find_all_faqs(cls):
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
