import csv
from os import listdir
from os.path import isfile, join

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.building_permits import Base, BuildingPermitSchema


class DataLoader:
    def __init__(self, database_url, data_dir):
        self.engine = create_engine(database_url)
        self.data_dir = data_dir
        self.data_files = self.get_data_files()
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)

    def get_data_files(self):
        return sorted(
            [
                join(self.data_dir, f)
                for f in listdir(self.data_dir)
                if isfile(join(self.data_dir, f)) and f.endswith(".csv")
            ]
        )

    def load_data(self):
        session = self.session()
        schema = BuildingPermitSchema()
        for data_file in self.data_files:
            self.load_file_into_db(data_file, session, schema)
        session.close()

    def load_file_into_db(self, data_file, session, schema):
        with open(data_file, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            nullable_int_columns = ["csa", "cbsa", "monthly_coverage_percent"]

            for row in reader:
                try:
                    for col in nullable_int_columns:
                        if row[col] == "":
                            row[col] = None
                        else:
                            row[col] = int(row[col]) if row[col].isdigit() else None

                    permit = schema.load(row, session=session)
                    session.add(permit)
                except ValueError as ve:
                    print(f"ValueError loading data: {ve}, in row: {row}")
                except TypeError as te:
                    print(f"ValidationError loading data: {te}, in row: {row}")
                except Exception as e:  # pylint: disable=broad-except
                    print(f"Unexpected error loading data: {e}, in row: {row['date']}")

            session.commit()


if __name__ == "__main__":
    loader = DataLoader(
        database_url="sqlite:///db/realestate.db", data_dir="./data/clean"
    )
    loader.load_data()
