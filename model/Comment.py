from db import db
from enums.CommentStatus import CommentStatus


class CommentModel(db.Model):
    __tablename__ = 'comments '
    id = db.Column(db.Integer, primary_key=True)
    commentId = db.Column(db.String(100), nullable=False)
    userId = db.Column(db.String(100), nullable=False)
    orderId = db.Column(db.String(100), nullable=False)  # show the order code
    message = db.Column(db.String(10), nullable=False)
    commentStatus = db.Column(db.Enum(CommentStatus), default=CommentStatus.PENDING)
    createdAt = db.Column(db.String(256))
    updatedAt = db.Column(db.String(10))

    def __init__(self):
        pass

    def __str__(self):
        pass

    def json(self):
        pass

    @classmethod
    def find_by_uuid(cls, orderId: str) -> 'CommentModel':
        return cls.query.filter_by(orderId=orderId).first()

    @classmethod
    def find_all_comments(cls):
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
