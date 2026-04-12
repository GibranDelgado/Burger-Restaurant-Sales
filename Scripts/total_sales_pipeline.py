from Scripts.google_sheets_client import GoogleSheetsClient
from Scripts.sales_data_processing import StoreSales, DigitalSales


class SalesPipeline:
    def __init__(self, creds_file):
        self.creds_file = creds_file
        self.gsc = GoogleSheetsClient()
        self.client = self.gsc.get_client(self.creds_file)

    def get_store_sales(self):
        store_ss = self.gsc.get_spreadsheet(self.client, "Ventas")
        store_ws = self.gsc.get_worksheets(store_ss)
        return StoreSales(store_ss, store_ws).cleaning_data()

    def get_digital_sales(self):
        digital_ss = self.gsc.get_spreadsheet(
            self.client, "Historico Ventas"
        )
        return DigitalSales(digital_ss).cleaning_data()