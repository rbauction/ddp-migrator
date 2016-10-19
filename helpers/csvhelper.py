import csv
import io


def load_csv_with_two_id_keys(csv_text, id_key, unique_key):
    """ Loads CSV file from a string, creates key1->key2 and key2->key1 maps and removes Id column """
    stream = io.StringIO(csv_text)
    reader = csv.reader(stream)
    header = next(reader)
    uk_index = header.index(unique_key)
    id_index = header.index(id_key)
    # Remove Id column from the header
    del header[id_index]

    id_to_uk = {}
    uk_to_id = {}
    rows = {}
    for row in reader:
        uk = row[uk_index]
        row_id = row[id_index]
        # Update maps
        id_to_uk[row_id] = uk
        uk_to_id[uk] = row_id
        # Remove Id column
        del row[id_index]
        rows[uk] = row

    return id_to_uk, uk_to_id, header, rows


def load_csv_with_one_id_key(csv_text, id_key):
    """ Loads CSV file from a string """
    stream = io.StringIO(csv_text)
    reader = csv.reader(stream)
    header = next(reader)
    id_index = header.index(id_key)
    # Remove Id column from the header
    del header[id_index]

    rows = {}
    for row in reader:
        row_id = row[id_index]
        # Remove Id column
        del row[id_index]
        rows[row_id] = row

    return header, rows


def save_csv(filename, header, rows):
    """ Saves table (header + rows) as CSV file """
    with open(filename, "w", encoding="utf-8", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        keys = list(rows.keys())
        # Saving CSV files sorted by unique key ensures 'git diff' will show only real changes
        keys.sort()
        for key in keys:
            writer.writerow(rows[key])


def save_csv_with_ids(file, header, rows, names_to_ids):
    """ Saves table (header + rows) as CSV file """
    should_close = True
    if isinstance(file, str):
        csv_file = open(file, 'w', encoding='utf-8', newline='')
    else:
        csv_file = file
        should_close = False

    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
    header_with_id = list(header)
    header_with_id.insert(0, 'Id')
    writer.writerow(header_with_id)
    keys = list(rows.keys())
    # Saving CSV files sorted by unique key ensures 'git diff' will show only real changes
    keys.sort()
    for key in keys:
        row_with_id = list(rows[key])
        row_with_id.insert(0, names_to_ids[key])
        writer.writerow(row_with_id)

    if should_close:
        csv_file.close()
