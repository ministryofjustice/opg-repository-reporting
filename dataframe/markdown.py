import pandas as pd
from .csv import dataframe_to_csv
# convert and save dataframe
class dataframe_to_markdown(dataframe_to_csv):
    ext = '.md'

    def save(self, processed_results):
        if len(processed_results) > 0:
            df = pd.DataFrame(processed_results)
            if df is not None:
                df.sort_values(by=self.sortby, inplace=True)
                df.to_markdown(self.filename, index=False)
        return
