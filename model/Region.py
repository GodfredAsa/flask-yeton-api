from db import db
from utils.GeneralUtils import generate_uuid


class RegionModel(db.Model):
    __tablename__ = "regions"
    id = db.Column(db.Integer, primary_key=True)
    regionId = db.Column(db.String(10), unique=True)
    name = db.Column(db.String(150), unique=True)
    city = db.Column(db.String(200), unique=True)

    def __init__(self, name, city):
        self.name = name
        self.city = city
        self.regionId = generate_uuid()

    def __repr__(self):
        return f"<Region: {self.name}>"

    def json(self):
        return {
            "regionId": self.regionId,
            "name": self.name,
            "city": self.city
        }

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_uuid(cls, regionId: str) -> 'RegionModel':
        return cls.query.filter_by(regionId=regionId).first()

    @classmethod
    def find_region_by_name(cls, name: str):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all_regions(cls):
        return cls.query.all()

