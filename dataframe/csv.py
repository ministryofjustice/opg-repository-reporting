import pandas as pd

# convert and save dataframe to csv
class dataframe_to_csv:
    filename = './report.csv'
    ext = '.csv'

    def __init__(self, filename):
        self.filename = filename + self.ext
        return


    def save(self, processed_results):
        if len(processed_results) > 0:
            df = pd.DataFrame(processed_results)
            if df is not None:
                df.sort_values(by=['Repository'], inplace=True)
                df.to_csv(self.filename, index=False)
        return
