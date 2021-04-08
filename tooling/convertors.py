

def for_output(temporary_store):
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
