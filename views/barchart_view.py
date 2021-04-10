from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PySide2.QtWidgets import QWidget, QSizePolicy, QComboBox, QLabel, QGridLayout
import matplotlib
import numpy as np

from views.base_plot_view import BasePlotView

class BarChartView(QWidget):
    def __init__(self, historical_data: dict):
        super().__init__()
        self._setupView()
        self._updatePlot(historical_data)

    def _setupView(self):
        self._createFigure()

    def _createFigure(self):
        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setSizePolicy(QSizePolicy.Expanding,
                                  QSizePolicy.Expanding)
        self.canvas.updateGeometry()

    def _updatePlot(self, historical_data: dict):
        labels = [keys in historical_data.keys()] # dates for each data point in historical data 
        positive_totals = [value[0] for value in historical_data.values()] # get list of positive tweet totals for each day
        negative_totals = [value[1] for value in historical_data.values()] # get list of negative tweet totals for each day

        x = np.arange(len(historical_data))  # the label locations
        width = 0.35  # the width of the bars
        rects1 = self.ax1.bar(x - width/2, positive_totals, width, label='Positive')
        rects2 = self.ax1.bar(x + width/2, negative_totals, width, label='Negative')

        # Add some text for labels, title and custom x-axis tick labels, etc.
        self.ax1.set_ylabel('No. Tweets')
        self.ax1.set_title('7-day Sentiment')
        self.ax1.set_xticks(x,, rotation = 45)
        self.ax1.set_xticklabels(labels)
        self.ax1.legend()

        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                self.ax1.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        # add totals above each bar
        autolabel(rects1)
        autolabel(rects2)

        self.fig.tight_layout()