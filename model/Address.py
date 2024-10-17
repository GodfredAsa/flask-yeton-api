from db import db
from model.User import UserModel
from model.Region import RegionModel
from utils.GeneralUtils import generate_uuid


class AddressModel(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer, primary_key=True)
    addressId = db.Column(db.String(10), unique=True)
    user_id = db.Column(db.String(20), unique=True)
    regionId = db.Column(db.String(256), nullable=False)
    location = db.Column(db.String(256))

    def __init__(self, userId, regionId, location):
        self.user_id = userId
        self.regionId = regionId
        self.addressId = generate_uuid()
        self.location = location

    def __repr__(self):
        return f"< Address: {self.addressId} {self.user_id} >"

    def json(self):
        region = RegionModel.find_by_uuid(self.regionId)
        user = UserModel.find_by_uuid(self.user_id)

        return {
            "phone": user.phone_number if user else None,
            "id": self.addressId,
            "region": region.name if region else None,
            "location": self.location
        }

    @classmethod
    def find_by_uuid(cls, addressId: str) -> 'AddressModel':
        return cls.query.filter_by(addressId=addressId).first()

    @classmethod
    def find_all_addresses(cls):
        return cls.query.all()

    @classmethod
    def find_address_by_userId(cls, userId: str) -> 'AddressModel':
        return cls.query.filter_by(user_id=userId).first()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()