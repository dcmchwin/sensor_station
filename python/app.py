"""Bokeh app to stream home climate data to localhost."""

from bokeh.layouts import column
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models.widgets import Panel, Tabs
import numpy as np

from utils import senstat_paths
from data_store import get_last


class CurrentWeatherFigure():
    """Class to hold the figure shown in the 'Current Weather' tab."""
    def __init__(self):
        """Initialise current weather figure."""

        # Create blank figure (hiding default toolbar, axes and grid)
        self.fig = figure(x_range=(0, 100),
                          y_range=(0, 100),
                          toolbar_location=None)#
        self.fig.axis.visible = False
        self.fig.grid.visible = False

        self.text_glyph = self.fig.text(x=[], y=[], text=[],
                                        text_font_size="30pt",
                                        text_baseline="middle",
                                        text_align="left")

        self.text_ds = self.text_glyph.data_source

        self.text_ds.data['x'] = [10, 10]
        self.text_ds.data['y'] = [70, 40]
        self.get_current_weather()

    def get_current_weather(self):
        """Retrieve the most recent weather data from the database."""
        df = get_last()
        temperature_int = int(np.round(df.temperature))
        temperature_str = ('Temperature: {:d} {}C'.
                            format(temperature_int, u'\N{DEGREE SIGN}'))
        humidity_str = 'Humidity: '
        self.text_ds.data['text'] = [temperature_str, humidity_str]


cw = CurrentWeatherFigure()

tab1 = Panel(child=cw.fig, title="Current Weather")

tabs = Tabs(tabs=[ tab1 ])

curdoc().add_periodic_callback(cw.get_current_weather,
                               2000)

curdoc().add_root(tabs)