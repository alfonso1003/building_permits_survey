from datetime import date
import urllib.error
import urllib.request


class DataExtractor:

    today = date.today()
    current_year = today.year
    months = range(1, 13)
    years = range(2004, current_year + 1)
    excel_file_start = date(2019, 11, 1)

    def should_download(self, year, month):
        return date(year, month, 1) <= self.today

    def build_url(self, year, month):
        url = f"https://www.census.gov/construction/bps/txt/tb3u{year}{month:02}.txt"
        if date(year, month, 1) >= self.excel_file_start:
            url = f"https://www.census.gov/construction/bps/xls/msamonthly_{year}{month:02}.xls"
        return url

    def find_file_format(self, year, month):
        file_format = "txt"
        if date(year, month, 1) >= self.excel_file_start:
            file_format = "xls"
        return file_format

    @staticmethod
    def download_file(url, output_file):
        try:
            urllib.request.urlretrieve(url, output_file)
            print(f"Downloaded: {output_file}")
        except urllib.error.URLError as e:
            print(f"{e}: {url}")

    def download_data(self):
        for year in self.years:
            for month in self.months:
                if not self.should_download(year, month):
                    continue

                url = self.build_url(year, month)
                file_format = self.find_file_format(year, month)
                output_file = f"./data/raw/bps_unit_{year}_{month:02}.{file_format}"
                self.download_file(url, output_file)


if __name__ == "__main__":
    extractor = DataExtractor()
    extractor.download_data()
