import scipy.optimize
import pandas as pd
import numpy as np

DEATHS_CSV = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
CONFIRMED_CSV = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

def clean_jhu_data(global_df, country, cutoff=0):
    dropnames = ["Lat", "Long", "Province/State", "Country/Region"]
    df = (
        global_df[global_df["Country/Region"] == country]
        .drop(dropnames, axis=1)
        .sum()
        .transpose()
    )
    df.index = pd.DatetimeIndex(df.index)
    return df[df > cutoff]


class Fitter:
    def __init__(self, data, xoffset=0):
        self.xoffset = xoffset
        self.xvals = list(range(xoffset, xoffset + len(data)))
        (self.a, self.b), self.cov = scipy.optimize.curve_fit(
            self.func,
            self.xvals,
            data.values,
            p0=[1.0, 1.0]
        )

    @staticmethod
    def func(x, a, b):
        return a * np.exp(b * x)

    def __call__(self, x):
        return self.func(x, self.a, self.b)

    @property
    def predict(self):
        return [self(x) for x in self.xvals]

    def extrapolate(self, x_min, x_max):
        return [self(x) for x in range(x_min, x_max)]


class DataSeries:
    def __init__(self, global_df, country):
        self._data = clean_jhu_data(global_df, country)

    def fit(self, cutoff=0, slicing=None):
        data = self.data(cutoff, slicing)
        xoffset = 0
        if slicing is not None:
            start = slicing.start
            if start < 0:
                xoffset = len(self.data(cutoff)) + start
            else:
                xoffset = start

        return Fitter(data, xoffset)

    def data(self, cutoff=0, slicing=None):
        if slicing is None:
            slicing = slice(None)
        return self._data[self._data > cutoff][slicing]


def exponent_timeseries(series, cutoff, interval=5):
    series_cutoff = series.data(cutoff=cutoff)
    b_values = [
        series.fit(cutoff=cutoff, slicing=slice(start, start+interval)).b
        for start in range(len(series_cutoff) - interval)
    ]
    return pd.Series(b_values, index=series_cutoff.index[interval:])
