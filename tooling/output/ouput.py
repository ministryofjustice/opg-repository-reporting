

# output class
class outputer:
    data_store = {}
    conversion_function = None
    save_function = None

    def __init__(self, conversion_function, save_function):
        self.conversion_function = conversion_function
        self.save_function = save_function
        return

    def append(self, key, values):
        self.data_store[key] = values
        return

    def output(self):
        if len(self.data_store) > 0:
            print('>>>>> Saving dataframe')
            convert = self.conversion_function
            processed = convert(self.data_store)
            save = self.save_function
            save(processed)
        else:
            print('>>>>> Nothing to save')
        return
