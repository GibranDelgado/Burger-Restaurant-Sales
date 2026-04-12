import pandas as pd


class CleaningMethods:
    def clean_cols(self, cols):
        return cols.str.replace(" ", "_")

    def convert_to_int(self, df, col):
        return df[col].astype("Int32")

    def convert_to_float(self, df, col):
        return df[col].str.replace("$", "").astype("float64")

    def convert_to_date(self, df, col):
        return pd.to_datetime(df[col], format="%d/%m/%Y")

    def remove_blanks(self, df, col, replacement_value):
        return df[col].replace("", replacement_value).fillna(replacement_value)

    def remove_parenthesis(self, df, col):
        return df[col].str.replace(r"\(.*\)", "", regex=True).str.strip()

    def remove_blanks_and_parenthesis(self, df, col, replacement_value):
        return (
            df[col]
            .replace("", replacement_value)
            .fillna(replacement_value)
            .str.replace(r"\(.*\)", "", regex=True)
            .str.strip()
        )

    def add_weekday(self, df, col):
        return (
            df[col]
            .dt.day_name()
            .map(
                {
                    "Monday": "Lunes",
                    "Tuesday": "Martes",
                    "Wednesday": "Miercoles",
                    "Thursday": "Jueves",
                    "Friday": "Viernes",
                    "Saturday": "Sabado",
                    "Sunday": "Domingo",
                }
            )
        )


class StoreSales(CleaningMethods):
    def __init__(self, spreadsheet, worksheets):
        self.spreadsheet = spreadsheet
        self.worksheets = worksheets

    def _worksheets_values(self):
        ranges = [
            f"{sheet.title}"
            for sheet in self.worksheets
            if sheet.title not in ["Productos", "Descuentos"]
        ]
        return self.spreadsheet.values_batch_get(ranges)["valueRanges"]

    def _add_columns(self, df):
        return df.assign(
            Cantidad=self.convert_to_int(df, "Cantidad"),
            Precio=self.convert_to_float(df, "Precio"),
            Total_del_pago=self.convert_to_float(df, "Total_del_pago"),
            Fecha=self.convert_to_date(df, "Fecha"),
            Tipo_de_pago=self.remove_blanks(df, "Tipo_de_pago", "Efectivo"),
            Edad_del_consumidor=self.remove_blanks_and_parenthesis(
                df, "Edad_del_consumidor", "No aplica"
            ),
            Genero=self.remove_blanks(df, "Genero", "Desconocido"),
            Momento_del_dia=self.remove_blanks_and_parenthesis(
                df, "Momento_del_dia", "No aplica"
            ),
            Dia_de_la_semana=lambda df: self.add_weekday(df, "Fecha"),
            Canal_de_venta="Tienda",
        )

    def cleaning_data(self):
        data = []
        raw_data = self._worksheets_values()

        for sheet in raw_data:
            values = sheet["values"][1:]
            for v in values:
                if len(v) > 6:
                    data.append(v[0:10])

        headers = raw_data[0]["values"][0][0:10]
        data = pd.DataFrame(data, columns=headers)
        data.columns = self.clean_cols(data.columns)

        products_to_remove = ["Pedido DiDi", "Pedido Rappi", "Paneles 3D"]

        data = data.pipe(
            lambda df: df[
                (df["Producto"] != "")
                & (~df["Producto"].isin(products_to_remove))
            ]
        ).pipe(self._add_columns)

        return data


class DigitalSales(CleaningMethods):
    def __init__(self, spreadsheet):
        self.spreadsheet = spreadsheet

    def _worksheet_values(self):
        sheet = self.spreadsheet.worksheet("VentasDiDi")
        return sheet.get("A:L")

    def _add_columns(self, df):
        return df.assign(
            Pedido=self.convert_to_int(df, "Pedido"),
            Cantidad=self.convert_to_int(df, "Cantidad"),
            Precio=self.convert_to_float(df, "Precio"),
            Total_del_pago=self.convert_to_float(df, "Total_del_pago"),
            Antes_del_descuento=self.convert_to_float(
                df, "Antes_del_descuento"
            ),
            Tarifa_de_servicio=self.convert_to_float(df, "Tarifa_de_servicio"),
            Fecha=self.convert_to_date(df, "Fecha"),
            Momento_del_dia=self.remove_parenthesis(df, "Momento_del_dia"),
            Dia_de_la_semana=lambda df: self.add_weekday(df, "Fecha"),
            Canal_de_venta="DiDi",
        )

    def cleaning_data(self):
        raw_data = self._worksheet_values()
        headers = raw_data[0]
        data = pd.DataFrame(raw_data[1:], columns=headers)
        data.columns = self.clean_cols(data.columns)

        return data.pipe(self._add_columns)
