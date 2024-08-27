import argparse
import csv

parser = argparse.ArgumentParser(description="")
parser.add_argument("--nodes", type=int, help="number of nodes")
parser.add_argument("--size", type=int, help="request size")
args = parser.parse_args()


def extract_end_to_end_metrics(file_name: str):
    end_to_end_tps = None
    end_to_end_latency = None

    with open(file_name, 'r') as file:
        lines = file.readlines()

        for line in lines:
            if "End-to-end TPS" in line:
                end_to_end_tps = float(line.split(":")[1].split()[0])
            if "End-to-end latency" in line:
                end_to_end_latency = float(line.split(":")[1].split()[0])

    return [end_to_end_tps, end_to_end_latency]


file_path = 'csv/peformance_data.csv'
output = 'csv/summary.csv'

with open(file_path, mode='r') as file:
    csv_reader = csv.reader(file)
    lines = [['Faults', 'Nodes', 'Rate', 'Size', 'Is_Attack', 'Attack_Level', 'TPS', 'Latency']]
    for index, row in enumerate(csv_reader):
        # Remove any extra spaces and assign to variables
        faults = int(row[0].strip())
        rate = int(row[1].strip())
        is_attack = row[2].strip().lower() == 'true'
        attack_level = int(row[3].strip())

        file = f'benchmark/results/bench-{faults}-{args.nodes}-{1}-{True}-{rate}-{args.size}-{is_attack}-{attack_level}.txt'
        metrics = extract_end_to_end_metrics(file)
        metrics.insert(0, faults)
        metrics.insert(0, args.nodes)
        metrics.insert(0, rate)
        metrics.insert(0, args.size)
        metrics.insert(0, is_attack)
        metrics.insert(0, attack_level)
        lines.append(metrics)

with open(output, mode='w') as file:
    csv_writer = csv.writer(file)
    for line in lines:
        csv_writer.writerow(line)
