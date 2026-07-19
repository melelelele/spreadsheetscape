import os
import csv
import requests
import time
import cscape
from io import StringIO


SHEET_ID = "1OBr7gCgwBKDFzp2G9-3Apv5eeUgBREYVbVOfW0s3bz8"
SHEET_GID = "0"

SHEET_CSV_URL = (
    f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export"
    f"?format=csv&gid={SHEET_GID}"
)


class Game:
    title = "SheetScape: Das geheime Geschenkregister"

    def get_rows(self):
        separator = "&" if "?" in SHEET_CSV_URL else "?"
        url = SHEET_CSV_URL + separator + "cachebust=" + str(time.time_ns())

        response = requests.get(
            url,
            timeout=5,
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            }
        )
        response.raise_for_status()
        response.encoding = "utf-8"

        return list(csv.reader(StringIO(response.text)))

    def cell(self, rows, address):
        col_letters = ""
        row_digits = ""

        for char in address.upper():
            if char.isalpha():
                col_letters += char
            elif char.isdigit():
                row_digits += char

        col = 0
        for char in col_letters:
            col = col * 26 + (ord(char) - ord("A") + 1)

        row = int(row_digits)

        try:
            return rows[row - 1][col - 1].strip()
        except Exception:
            return ""

    def normalized_cell(self, rows, address):
        return self.cell(rows, address).strip().lower()

    def check_name_done(self):
        rows = self.get_rows()
        name = self.cell(rows, "B1").strip()

        if name:
            cscape.store("name", name)
            return True

        return False

    def check_first_sum_done(self):
        rows = self.get_rows()
        return self.cell(rows, "D4") == "20"

    def check_all_sums_done(self):
        rows = self.get_rows()
        return (
                self.cell(rows, "D4") == "20"
                and self.cell(rows, "D5") == "22"
                and self.cell(rows, "D6") == "15"
        )

    def check_total_done(self):
        rows = self.get_rows()
        return self.cell(rows, "D7") == "57"

    def check_combo_codes_done(self):
        rows = self.get_rows()
        return (
                self.normalized_cell(rows, "D10") == "mila-sternenlampe"
                and self.normalized_cell(rows, "D11") == "noah-schneekugel"
                and self.normalized_cell(rows, "G10") == "mila-sternenlampe"
                and self.normalized_cell(rows, "G11") == "noah-schneekugel"
        )

    def check_lookup_gifts_done(self):
        rows = self.get_rows()

        print("B12 =", repr(self.cell(rows, "B12")))
        print("B13 =", repr(self.cell(rows, "B13")))

        return (
                self.normalized_cell(rows, "B12") == "märchenbuch"
                and self.normalized_cell(rows, "B13") == "kompass"
        )



    def check_count_wrapped_done(self):
        rows = self.get_rows()
        return self.cell(rows, "C16") == "4"

    def check_open_count_done(self):
        rows = self.get_rows()
        return self.cell(rows, "C17") == "0"

    def check_sleigh_status_done(self):
        rows = self.get_rows()
        return self.normalized_cell(rows, "C18") == "startklar"


if __name__ == "__main__":
    import cscape
    cscape.run(Game())