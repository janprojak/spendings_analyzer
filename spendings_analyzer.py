import argparse
import csv


def CreateArgumentParser():
    parser = argparse.ArgumentParser(
        description="""
                    This analyzer is aimed to analyze and systemize your spendings.
                    You have to provide input data and will have a .csv table with systematized output.
                    For now the .csv format of input is supported.
                    """
    )

    parser.add_argument(
        "-i",
        "--input",
        action="store",
        required=True,
        help="Use to provide a path to input file."
    )

    parser.add_argument(
        "-o",
        "--output",
        action="store",
        required=True,
        help="Use to provide a path to where store the output file."
    )

    return parser


class Spending:
    def __init__(self, date, name, mcc, sum):
        self.date = date
        self.name = name
        self.mcc = mcc
        self.sum = sum

    def __lt__(self, other):
        return (self.date, self.name, self.mcc, self.sum) < (other.date, other.name, other.mcc, other.sum)

    def ToString(self):
        return "date: {}, name: {}, mcc: {}, sum: {}".format(self.date,
                                                             self.name,
                                                             self.mcc, self.sum
                                                             )

    def ToList(self):
        return [self.date, self.name, self.mcc, self.sum]


def ParseCsv(path_to_table):
    with open(path_to_table, "r", newline="", encoding="utf-8") as input_data_file:
        reader = csv.reader(input_data_file, delimiter=",")

        # skip headers
        next(reader, None)

        spendings = list()

        for row in reader:
            date_time = row[0]
            date = date_time.split(sep=" ")[0]
            operation_name = row[1]
            operation_mcc = row[2]
            operation_sum = row[3]

            spendings.append(Spending(date, operation_name,
                             operation_mcc, operation_sum))

        return spendings


def WriteToCsv(path_to_table, spendings):
    with open(path_to_table, "w", newline="", encoding="utf-8") as output_data_file:
        writer = csv.writer(output_data_file)

        writer.writerow(["Дата", "Найменування", "MCC", "Значення"])

        for sp in spendings:
            writer.writerow(sp.ToList())


if __name__ == "__main__":
    parser = CreateArgumentParser()
    args = parser.parse_args()

    print("Input: {}, Output: {}".format(args.input, args.output))

    spendings = ParseCsv(args.input)

    spendings.sort()

    WriteToCsv(args.output, spendings)

    for sp in spendings:
        print(sp.ToString())
