import pandas as pd

# convert and save dataframe to csv
class dataframe_to_csv:
    filename = './report.csv'
    ext = '.csv'
    sortby = ['Repository']

    def __init__(self, filename, sortby=None):
        self.filename = filename + self.ext
        if sortby != None:
            self.sortby = sortby
        return


    def save(self, processed_results):
        if len(processed_results) > 0:
            df = pd.DataFrame(processed_results)
            if df is not None:
                df.sort_values(by=self.sortby, inplace=True)
                df.to_csv(self.filename, index=False)
        return
