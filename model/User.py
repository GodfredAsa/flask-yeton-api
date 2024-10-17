from db import db
from utils.GeneralUtils import generate_uuid


class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(20), unique=True)
    name = db.Column(db.String(80), nullable=False)
    # email = db.Column(db.String(80), nullable=False)
    imageUrl = db.Column(db.String(250))
    phone_number = db.Column(db.String(10), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(80), nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    isOnline = db.Column(db.Boolean)
    isBlackListed = db.Column(db.Boolean)

    def __init__(self, name, password, imageUrl, phone, gender):
        self.name = name
        # self.email = email
        self.imageUrl = imageUrl
        self.password = password
        self.phone_number = phone
        self.is_admin = False
        self.isBlackListed = False
        self.gender = gender
        self.user_id = generate_uuid()
        self.isOnline = False

    def json(self):
        return {
            "userId": self.user_id,
            "name": self.name,
            "phone": self.phone_number,
            # "email": self.email,
            "imageUrl": self.imageUrl,
            "isAdmin": self.is_admin,
            "gender": self.gender,
            "isOnline": self.isOnline
        }

    # @classmethod
    # def find_by_email(cls, email: str) -> 'UserModel':
    #     return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_phone(cls, phone: str) -> 'UserModel':
        return cls.query.filter_by(phone_number=phone).first()

    @classmethod
    def find_by_id(cls, _id: int) -> 'UserModel':
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_uuid(cls, userId: str) -> 'UserModel':
        return cls.query.filter_by(user_id=userId).first()

    @classmethod
    def find_all_users(cls):
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
