import pandas as pd

# convert and save dataframe to csv
class dataframe_to_csv:
    filename = './report.csv'
    ext = '.csv'

    def __init__(self, filename):
        self.filename = filename + self.ext
        return


    def convert(self, temporary_store):
        processed_results = []
        for key in temporary_store:
            item = temporary_store[key]
            # ony save if it has a location
            if len(item['Locations']) > 0:
                processed_results.append({
                    'Repository': item['Repository'].replace("ministryofjustice/", ""),
                    'Tool': item['Tool'] if 'Tool' in item else "",
                    'Category': item['Category'] if 'Category' in item else "",
                    'Locations': "\n".join(item['Locations'])
                })
        return processed_results

    def save(self, processed_results):
        if len(processed_results) > 0:
            df = pd.DataFrame(processed_results)
            if df is not None:
                df.sort_values(by=['Repository'], inplace=True)
                df.to_csv(self.filename, index=False)
        return
