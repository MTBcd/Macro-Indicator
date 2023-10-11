import pandas as pd
import datetime

# Import your custom modules
from toolbox import Toolbox
from data_scraping import DataScraper
from chart import Chart

def main():
    # Step 2: Data Scraping
    indicators = ["BAA10Y", "IC4WSA", "PERMIT", "T10YFF", "VIXCLS"]
    data_scrap = DataScraper(indicators)
    start_date = datetime.datetime(1990, 1, 1)
    end_date = datetime.datetime.today()
    indicator_df = data_scrap.scrape_data(start_date, end_date)

    # Step 3: Data Transformation
    macro_indicator = Toolbox.PCA_transform(indicator_df)
    filtered_data = Toolbox.L1_trend_filter(macro_indicator, regulation_param=0.5)
    regime_encode = Toolbox.Regime_identification(filtered_data, macro_indicator)
    # Step 4: Data Visualization
    chart = Chart()
    chart.create_chart(macro_indicator, filtered_data, regime_encode)

if __name__ == "__main__":
    main()
