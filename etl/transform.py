from datetime import date
from os import listdir
from os.path import isfile, join

import pandas as pd
import xlrd


data_dir = "./data/raw"
data_files = sorted([join(data_dir, f) for f in listdir(data_dir) if isfile(join(data_dir, f))])

output_dir = "./data/clean"
output_cols = [
    "date",
    "csa",
    "cbsa",
    "name",
    "total",
    "one_unit",
    "two_units",
    "three_and_four_units",
    "five_units_or_more",
    "num_of_structures_with_5_units_or_more",
    "monthly_coverage_percent"
]


def get_numeric_column_count(file_year, file_month):
    numeric_column_count = 6
    if date(file_year, file_month, 1) >= date(2007, 11, 1):
        numeric_column_count = 7
    return numeric_column_count


def is_cbsa_file(file_year, file_month):
    cbsa = False
    aug_2009 = date(file_year, file_month, 1) == date(2009, 8, 1)
    after_october_2009 = date(file_year, file_month, 1) >= date(2009, 10, 1)
    if aug_2009 or after_october_2009:
        cbsa = True
    return cbsa


def contains_monthly_coverage_percent(file_year, file_month):
    return date(file_year, file_month, 1) >= date(2007, 11, 1)


def process_txt_file(data_file, file_year, file_month):

    data = []

    with open(data_file) as file:
        lines = map(str.strip, file.readlines())

    lines = list(lines)[11:]
    lines = [l.replace("*", "").split() for l in lines if l]

    join_lines = False
    clean_lines = []
    for line in lines:
        if not line[-1].isnumeric():
            join_lines = True
            clean_lines.append(line)
        elif join_lines:
            clean_lines[-1] = clean_lines[-1] + line
            join_lines = False
        else:
            clean_lines.append(line)

    numeric_column_count = get_numeric_column_count(file_year, file_month)
    for cl in clean_lines:
        if is_cbsa_file(file_year, file_month):
            data_row = (
                [date(file_year, file_month, 1).strftime("%m-%Y")] +
                list(map(int, cl[0:2])) +
                [" ".join(cl[2:-numeric_column_count])] +
                list(map(int, cl[-numeric_column_count:]))
                )
        else:
            data_row = (
                [date(file_year, file_month, 1).strftime("%m-%Y")] +
                [None, None] +
                [" ".join(cl[:-numeric_column_count])] +
                list(map(int, cl[-numeric_column_count:]))
                )

        if not contains_monthly_coverage_percent(file_year, file_month):
            data_row.append(None)

        data.append(data_row)

        if ("Yuma" in cl[0]) or ("Yuma" in cl[2]):
            break

    df = pd.DataFrame(data, columns=output_cols)

    output_file = data_file.split("/")[-1].split(".")[0] + ".csv"
    output_file = join(output_dir, output_file)
    df.to_csv(output_file, index=False)


def get_sheetname(file_year, file_month):
    sheetname = "MSA Units"
    if file_year == 2019 and file_month in (11, 12):
        sheetname = "Units"
    return sheetname


def process_xls_file(data_file, file_year, file_month):

    sheetname = get_sheetname(file_year, file_month)

    workbook = xlrd.open_workbook(data_file)
    worksheet = workbook.sheet_by_name(sheetname)
    max_row_index = worksheet.nrows  # exclusive

    data = []
    for row in range(9, max_row_index):
        data_row = [date(file_year, file_month, 1).strftime("%m-%Y")]
        for col in range(0,10):
            val = worksheet.cell(row, col).value
            if isinstance(val, float):
                val = int(val)
            else:
                val = val.strip()
            data_row.append(val)
        data.append(data_row)

    df = pd.DataFrame(data, columns=output_cols)

    output_file = data_file.split("/")[-1].split(".")[0] + ".csv"
    output_file = join(output_dir, output_file)
    df.to_csv(output_file, index=False)

for data_file in data_files:
    _, _, _, file_year, file_month, file_format = data_file.replace(".", "_").split("_")
    file_year, file_month = int(file_year), int(file_month)
    if file_format == "txt":
        process_txt_file(data_file, file_year, file_month)
    elif file_format == "xls":
        process_xls_file(data_file, file_year, file_month)
