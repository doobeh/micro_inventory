import csv

def resolve_store(identifier):
    stores = {'GG': 3, 'SM': 4, 'IGA': 1, 'FS': 2}
    return stores.get(identifier,'??')


def clean_calculation(calculation):
    allowed_characters = '0123456789-+*()'
    calculation = "".join([x for x in calculation if x in allowed_characters])

    try:
        return eval(calculation), 'good'
    except SyntaxError:
        try:
            return int(calculation), 'good'
        except:
            return calculation, 'bad'


def droste_data(source='r:\\data\item_export.csv'):
    item_details = dict()
    with file(source, 'rb') as droste_data:
        csv_file = csv.reader(droste_data)
        for line in csv_file:
            gtin = line[0].zfill(13)

            unit_cost = float(line[5])
            description = line[4].strip().decode('latin8')
            pack = line[6].strip()
            size = '{}{}'.format(line[7].strip(), line[8].strip())

            item_details[gtin] = {
                'unit_cost': unit_cost,
                'description': description,
                'pack': pack,
                'size': size,
            }
    return item_details