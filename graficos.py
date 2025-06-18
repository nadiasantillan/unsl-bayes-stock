from datetime import date
from seaborn import histplot

from modelo import CotizacionHistorica

class GraficosCotizaciones:
    def __init__(self, cotizaciones):
        self.cotizaciones = cotizaciones

    def aperturas(self, fecha_desde=None, fecha_hasta=None):
        self._histograma("Open", fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

    def maximos(self, fecha_desde=None, fecha_hasta=None):
        self._histograma("High", fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

    def minimos(self, fecha_desde=None, fecha_hasta=None):
        self._histograma("Low", fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

    def ultimos_cierres(self, fecha_desde=None, fecha_hasta=None):
        self._histograma("Close/Last", fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

    def diferencias_cierre_apertura(self, fecha_desde=None, fecha_hasta=None):
        self._histograma("Diff_Apertura_Cierre", fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

    def diferencias_max_min(self, fecha_desde=None, fecha_hasta=None):
        self._histograma("Diff_Max_Min", fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

    def _histograma(self, variable, fecha_desde=None, fecha_hasta=None):
        desde = fecha_desde or self.cotizaciones.fecha_min()
        hasta = fecha_hasta or self.cotizaciones.fecha_max()

        df = self.cotizaciones.cotizaciones(desde, hasta)
        histplot(df, x=variable)
