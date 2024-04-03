from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class BuildingPermit(Base):
    __tablename__ = "building_permits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String)
    csa = Column(Integer, nullable=True)
    cbsa = Column(Integer, nullable=True)
    name = Column(String)
    total = Column(Integer)
    one_unit = Column(Integer)
    two_units = Column(Integer)
    three_and_four_units = Column(Integer)
    five_units_or_more = Column(Integer)
    num_of_structures_with_5_units_or_more = Column(Integer)
    monthly_coverage_percent = Column(Integer, nullable=True)


class BuildingPermitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BuildingPermit
        load_instance = True
