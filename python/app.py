"""Bokeh app to stream home climate data to localhost."""

from bokeh.layouts import column
from bokeh.io import curdoc
from bokeh.plotting import figure
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import Range1d, ColumnDataSource
from datetime import datetime
import numpy as np
import pandas as pd
from pandas.tseries.offsets import DateOffset

from utils import senstat_paths, time_format, delay_s
from data_store import get_last, read_into_df


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

        self.date_text_glyph = self.fig.text(x=[], y=[], text=[],
                                             text_font_size='16pt',
                                             text_baseline="middle",
                                             text_align="left")

        self.text_ds = self.text_glyph.data_source
        self.date_text_ds = self.date_text_glyph.data_source

        self.text_ds.data['x'] = [10, 10]
        self.text_ds.data['y'] = [70, 40]
        self.date_text_ds.data['x'] = [10]
        self.date_text_ds.data['y'] = [10]
        self.get_current_weather()

    def get_current_weather(self):
        """Retrieve the most recent weather data from the database."""
        df = get_last()

        # Set the text for temperature and humidity
        temperature_int = int(np.round(df.temperature))
        temperature_str = ('Temperature: {:d} {}C'.
                            format(temperature_int, u'\N{DEGREE SIGN}'))
        humidity_str = 'Humidity: '
        self.text_ds.data['text'] = [temperature_str,
                                     humidity_str]

        # Set the date text
        dt = datetime.strptime(df.date.iloc[-1], time_format)
        dtstr = "Data retrieved {}".format(dt.strftime("%Y-%m-%d %H:%M:%S"))
        self.date_text_ds.data['text'] = [dtstr]


class HistoryPlotFigure():
    """Class for figure plotting historical weather."""
    def __init__(self):
        """Initialise historical weather plot."""
        y_axis_label = "Temperature ({}C)".format(u'\N{DEGREE SIGN}')

        self.fig = figure(x_axis_type='datetime',
                          y_axis_label=y_axis_label,
                          x_axis_label="Time and Date")

        self.df = self._tidy_df(read_into_df())
        data = self._get_data_dict(self.df)
        self.ds = ColumnDataSource(data)
        self._set_axis_limits()

        self.scatter = self.fig.scatter(source=self.ds,
                                        x='date',
                                        y='temperature')


    @staticmethod
    def _tidy_df(df):
        """Tidy the acquired weather for null values and date format."""
        df.date = df.date.apply(lambda x: pd.Timestamp(x, tz='Europe/London'))
        df.dropna(axis=1, how='any', inplace=True)
        df = df[df.temperature >= -30]
        return df


    @staticmethod
    def _get_data_dict(df):
        """Get a dict of data to instantiate or add to a ColumnDataSource."""
        le_keys = ['index'] + list(df.keys())
        data = {k: getattr(df, k).get_values() for k in le_keys}
        return data


    @staticmethod
    def convert_unix_ms(ts):
        """Get time in unix ms from input timestamps."""
        unix_ms = ts.value // 10 ** 6
        return unix_ms


    def _set_axis_limits(self):
        """Set the date axis to be the last 24 hours."""

        # Get date range in unix seconds
        now = pd.Timestamp.now()
        ytd = now - DateOffset(days=1)
        now_ms = self.convert_unix_ms(now)
        ytd_ms = self.convert_unix_ms(ytd)

        # Set the x axis limits to be the last 24 hours
        self.fig.x_range = Range1d(ytd_ms, now_ms)


    def update_data_source(self):
        """Update the temperature plot with newest data."""
        self.df = self._tidy_df(read_into_df())
        new_data = self._get_data_dict(self.df)
        new_ds = ColumnDataSource(new_data)
        self.ds.data = new_ds.data
        self._set_axis_limits()


cw = CurrentWeatherFigure()
hp = HistoryPlotFigure()

tabcw = Panel(child=cw.fig, title="Current Weather")
tabhp = Panel(child=hp.fig, title="Historical Plot")

tabs = Tabs(tabs=[ tabcw, tabhp])

curdoc().add_periodic_callback(cw.get_current_weather,
                               delay_s * 1000)
curdoc().add_periodic_callback(hp.update_data_source,
                               delay_s * 1000)

curdoc().add_root(tabs)
curdoc().title = "Home Sensor Station"