import pandas as pd
import numpy as np
from datetime import date

class CotizacionHistorica:
    def __init__(self, archivo_nombre: str):
        df = pd.read_csv(archivo_nombre, parse_dates=["Date"])
        df["Close/Last"] = df["Close/Last"].apply(self._precio)
        df["Open"] = df["Open"].apply(self._precio)
        df["High"] = df["High"].apply(self._precio)
        df["Low"] = df["Low"].apply(self._precio)
        df["Diff_Apertura_Cierre"] = df["Open"]-df["Close/Last"]
        df["Diff_Max_Min"] = df["High"]-df["Low"]
        df["Año"] = df["Date"].apply(self._anio)
        df["Mes"] = df["Date"].apply(self._mes)
        self.df = df

    def cotizaciones(self, fecha_desde=None, fecha_hasta=None):
        return self.df[(self.df["Date"]>= self._fecha_desde(fecha_desde))&(self.df["Date"]<=self._fecha_hasta(fecha_hasta))]
    
    def por_mes_anio(self, fecha_desde=None, fecha_hasta=None):
        return self.cotizaciones(
            fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)[["Año", "Mes", "Diff_Apertura_Cierre"]].groupby(
                ["Año", "Mes"]).agg([np.mean, np.std])
    
    def fecha_min(self):
        return self.df["Date"].min().to_pydatetime()

    def fecha_max(self):
        return self.df["Date"].max().to_pydatetime()
    
    def _fecha_desde(self, fecha_desde):
        return pd.to_datetime(fecha_desde if fecha_desde else self.fecha_min())
    
    def _fecha_hasta(self, fecha_hasta):
        return pd.to_datetime(fecha_hasta if fecha_hasta else self.fecha_max())

    @staticmethod
    def _precio(precio_str):
        return float(precio_str.replace("$", ""))
    
    @staticmethod
    def _anio(fecha):
        return fecha.year
    
    @staticmethod
    def _mes(fecha):
        return fecha.month