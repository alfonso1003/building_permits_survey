from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, Date, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class BuildingPermit(Base):
    __tablename__ = "building_permits"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    csa = Column(Integer)
    cbsa = Column(Integer)
    name = Column(String)
    total = Column(Integer)
    one_unit = Column(Integer)
    two_units = Column(Integer)
    three_and_four_units = Column(Integer)
    five_units_or_more = Column(Integer)
    num_of_structures_with_5_units_or_more = Column(Integer)
    monthly_coverage_percent = Column(Integer)


class BuildingPermitSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BuildingPermit
        load_instance = True  # Optional: deserialize to model instances
