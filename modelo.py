import pandas as pd
from datetime import date

class CotizacionHistorica:
    def __init__(self, archivo_nombre: str):
        df = pd.read_csv(archivo_nombre, parse_dates=["Date"])
        df["Close/Last"] = df["Close/Last"].apply(self._precio)
        df["Open"] = df["Open"].apply(self._precio)
        df["High"] = df["High"].apply(self._precio)
        df["Low"] = df["Low"].apply(self._precio)
        self.df = df

    def cotizaciones(self, fecha_desde, fecha_hasta):
        desde = pd.to_datetime(fecha_desde)
        hasta = pd.to_datetime(fecha_hasta)
        return self.df[(self.df["Date"]>= desde)&(self.df["Date"]<= hasta)]
    
    @staticmethod
    def _precio(precio_str):
        return float(precio_str.replace("$", ""))