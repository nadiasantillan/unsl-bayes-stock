# from datetime import date
from seaborn import histplot, lineplot, boxplot
import matplotlib.pyplot as plt
from scipy.stats import probplot


class GraficosCotizaciones:
    def __init__(self, historico):
        self.historico = historico

    def aperturas(self, fecha_desde=None, fecha_hasta=None):
        self._histograma("Open", fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

    def maximos(self, fecha_desde=None, fecha_hasta=None):
        self._histograma("High", fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

    def minimos(self, fecha_desde=None, fecha_hasta=None):
        self._histograma("Low", fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

    def ultimos_cierres(self, fecha_desde=None, fecha_hasta=None):
        self._histograma("Close/Last", fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)

    def log_razon_cierres(self, fecha_desde=None, fecha_hasta=None):
        self._histograma("Log_Razon_Cierre_Anterior", 
                         fecha_desde=fecha_desde, 
                         fecha_hasta=fecha_hasta, 
                         titulo="Distribución de los rendimientos logarítmicos",
                         etiqueta_x="Rendimientos logarítmicos",
                         etiqueta_y="Frecuencia")

    def qq_log_razon_cierres(self, fecha_desde=None, fecha_hasta=None):
        probplot(self.historico.cotizaciones(fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)["Log_Razon_Cierre_Anterior"], plot=plt)
        plt.xlabel("z")
        plt.ylabel("Logaritmo natural rendimientos")
        plt.title("Gráfico cuantil-cuantil de los rendimientos logarítmicos")

    def evolucion_cotizacion(self, fecha_desde=None, fecha_hasta=None):
        desde = fecha_desde or self.historico.fecha_min()
        hasta = fecha_hasta or self.historico.fecha_max()
        plt.figure(figsize=(12, 5))
        data = self.historico.cotizaciones(fecha_desde=desde, fecha_hasta=hasta)
        outliers_3sigma = self.historico.atipicos("Log_Razon_Cierre_Anterior")
        plt.scatter(outliers_3sigma.index, outliers_3sigma["Close/Last"],
                    color="red", label="Valores atípicos", zorder=5)
        plt.plot(data.index, data["Close/Last"], label="Precio de cierre ajustado", color="steelblue")
        plt.xlabel("Fecha")
        plt.ylabel("Precio de Cierre (USD)")
        plt.title(f"Precio de cierre con atípicos de rendimientos logarítmicos destacados {desde.year}-{hasta.year}")

        plt.legend()
        plt.grid(True)
        plt.tight_layout()

    def evolucion_razones_log(self, fecha_desde=None, fecha_hasta=None):
        plt.figure(figsize=(10,5))
        df = self.historico.cotizaciones(fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)
        lineplot(df, x=df.index, y="Close/Last")
        plt.xlabel("Fecha")
        plt.ylabel("Precio de Cierre (USD)")
        plt.title("Precio de las acciones de Apple 2015-2025")

    def boxplot_rendimientos_logaritmicos(self, fecha_desde=None, fecha_hasta=None):
        returns = self.historico.cotizaciones(fecha_desde=fecha_desde, fecha_hasta=fecha_hasta)["Log_Razon_Cierre_Anterior"]
        plt.figure(figsize=(6, 5))
        boxplot(y=returns, width=0.3, color="skyblue")
        plt.title("Boxplot de rendimientos logarítmicos")
        plt.ylabel("Rendimientos logarítmicos")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def _histograma(self, variable, fecha_desde=None, fecha_hasta=None, titulo="", etiqueta_x="", etiqueta_y=""):
        plt.figure(figsize=(10,5))
        desde = fecha_desde or self.historico.fecha_min()
        hasta = fecha_hasta or self.historico.fecha_max()

        df = self.historico.cotizaciones(desde, hasta)
        histplot(df, x=variable, kde=True)
        plt.xlabel(etiqueta_x)
        plt.ylabel(etiqueta_y)
        plt.title(titulo)

    