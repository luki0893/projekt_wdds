import csv

class Dataset:

    def __init__(self):
        self.data = []
        self.labels = []
        self.class_column_index = None

    def read_data(self, filepath: str, header=True, delimiter=',', class_col_index=-1, encoding='utf-8'):

        self.class_column_index = class_col_index

        try:
            with open(filepath, mode='r', encoding=encoding) as filehandler:
                for line_idx, line in enumerate(filehandler):
                    if line_idx == 0 and header:
                        self.labels.append(line.split(delimiter))
                    else:
                        self.data.append(line.split(delimiter))


        except IOError as err:
            print(f"Błąd odczytu pliku z danymi: {err}")

    def get_labels(self):
        if self.labels:
            print("Etykiety kolumn:", self.labels)
        else:
            print("Brak etykiet kolumn w danym datasecie.")

    def get_data(self, start=None, end=None):
        if start is not None and end is not None:
            for row in self.data[start:end]:
                print(row)
        else:
            for row in self.data:
                print(row)


    def data_split(self, train_pct, test_pct, valid_pct):
        import random


        random.shuffle(self.data)

        train_last_index = int(len(self.data) * train_pct)
        test_last_index = int(len(self.data) * (train_pct + test_pct))

        train_data = self.data[:train_last_index]
        test_data = self.data[train_last_index:test_last_index]
        valid_data = self.data[test_last_index:]

        return train_data, test_data, valid_data

    def get_number_of_classes(self):

        class_counts = {}

        for row in self.data:
            class_name = row[self.class_column_index]

            if class_name in class_counts:
                class_counts[class_name] += 1
            else:
                class_counts[class_name] = 1

        return [(key, value) for key, value in class_counts.items()]

    def class_data(self, class_col_index, class_name):
        for row in self.data:
            if row[class_col_index] == class_name:
                print(row)

    def save_to_csv(self, data, file_name):
        with open(file_name, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if self.labels:
                writer.writerow(self.labels)
            writer.writerows(data)
        print(f'Dane zostały zapisane do pliku {file_name}')



ds = Dataset()
ds.read_data('Toxicity-13F.csv')
print(ds.get_labels())
print(ds.get_data(1, 3))
train_data, test_data, valid_data = ds.data_split(0.7, 0.2, 0.1)

for subset in ds.data_split(0.7, 0.2, 0.1):
    print(f"Ilość elementów w zbiorze: {len(subset)}")

print(ds.get_number_of_classes())
print(ds.class_data(13, 'NonToxic'))
ds.save_to_csv(train_data, 'train_data.csv')
