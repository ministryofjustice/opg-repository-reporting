

def for_output(temporary_store):
    processed_results = []
    for key in temporary_store:
        item = temporary_store[key]
        processed_results.append(item)
    return processed_results
