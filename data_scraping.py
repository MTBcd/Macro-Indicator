import pandas as pd
from functools import reduce
import pandas_datareader.data as web
from datetime import datetime

class DataScraper:
    def __init__(self, indicators):
        self.indicators = indicators
        self.data = None

    def scrape_data(self, start_date, end_date):
        if not (isinstance(start_date, datetime) and isinstance(end_date, datetime)):
            raise TypeError("start_date and end_date must be datetime objects.")

        data_frames = []
        for indicator in self.indicators:
            data = web.DataReader(indicator, "fred", start=start_date, end=end_date)
            data_frames.append(data)

        # Merge data frames based on timestamps and handle missing values
        merged_data = reduce(lambda left, right: pd.merge_asof(left, right, left_index=True,
                                                              right_index=True,
                                                              tolerance=pd.Timedelta(days=1),
                                                              direction='nearest'), data_frames)

        #if merged_data.isna().values.any():
        #    raise ValueError("Missing or NaN values detected in the data. Handle these cases accordingly.")

        # Resample the data to 'M' (monthly) frequency and fill missing values
        self.data = merged_data.resample("M").last().fillna(method='ffill')

        return self.data
