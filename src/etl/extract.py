from datetime import date
import urllib.error
import urllib.request


# https://www.census.gov/construction/bps/msamonthly.html

today = date.today()
current_year = today.year
months = range(1,13)
years = range(2004, current_year + 1)
excel_file_start = date(2019, 11, 1)

for year in years:
    for month in months:

        report_year_month = date(year, month, 1)

        if report_year_month > today:
            continue

        url = f"https://www.census.gov/construction/bps/txt/tb3u{year}{month:02}.txt"
        format = "txt"
        if  report_year_month >= excel_file_start:
            url = f"https://www.census.gov/construction/bps/xls/msamonthly_{year}{month:02}.xls"
            format = "xls"

        output_file = f"./data/raw/bps_unit_{year}_{month:02}.{format}"

        try:
            urllib.request.urlretrieve(url, output_file)
        except urllib.error.URLError as e:
            print(f"{e}: {url}")
