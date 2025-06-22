import pandas as pd
import numpy as np
from datetime import date

class CotizacionHistorica:
    def __init__(self, archivo_nombre: str):
        df = pd.read_csv(archivo_nombre, parse_dates=["Date"])
        df["Año"] = df["Date"].apply(self._anio)
        df["Mes"] = df["Date"].apply(self._mes)
        df.set_index("Date", inplace=True)

        df["Close/Last"] = df["Close/Last"].apply(self._precio)
        df["Open"] = df["Open"].apply(self._precio)
        df["High"] = df["High"].apply(self._precio)
        df["Low"] = df["Low"].apply(self._precio)
        df["Diff_Cierre_Anterior"] = df["Close/Last"]-df["Close/Last"].shift(-1)
        df["Log_Razon_Cierre_Anterior"] = np.log(df["Close/Last"]/df["Close/Last"].shift(-1))
        self.df = df.dropna()

    def cotizaciones(self, fecha_desde=None, fecha_hasta=None):
        return self.df[(self.df.index>= self._fecha_desde(fecha_desde))
                       &(self.df.index<=self._fecha_hasta(fecha_hasta))]

    def media_desvio(self, variable, fecha_desde=None, fecha_hasta=None):
        df = self.cotizaciones(fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)[variable]
        return (df.mean(), df.std())

    def atipicos(self, variable, fecha_desde=None, fecha_hasta=None):
        df = self.cotizaciones(fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)
        q1, q3 = tuple(df[variable].quantile([0.25, 0.75]))
        iqr = q3 -q1
        inf, sup = (q1 - iqr * 1.5, q3 + iqr * 1.5)
        return df[(df[variable] < inf)|(df[variable]> sup)]

    def fecha_min(self):
        return self.df.index.min().to_pydatetime()

    def fecha_max(self):
        return self.df.index.max().to_pydatetime()
    
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