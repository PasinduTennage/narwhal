import csv
import os
import argparse

parser = argparse.ArgumentParser(description="")
parser.add_argument("--nodes", type=int, help="number of nodes")
parser.add_argument("--size", type=int, help="request size")
parser.add_argument("--input_csv", type=str, help="csv/peformance_data_50.csv")
parser.add_argument("--output_csv", type=str, help="csv/output.csv")
args = parser.parse_args()


def extract_end_to_end_metrics(file_name: str):
    end_to_end_tps = None
    end_to_end_latency = None
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()

            for line in lines:
                if "End-to-end TPS" in line:
                    end_to_end_tps = float(line.split(":")[1].split()[0].replace(',', ''))
                if "End-to-end latency" in line:
                    end_to_end_latency = float(line.split(":")[1].split()[0].replace(',', ''))

        return [end_to_end_tps, end_to_end_latency]
    except Exception as e:
        print(f"Error: {file_name}")
        return [None, None]


with open(args.output_csv, mode='w') as output_file:
    csv_writer = csv.writer(output_file, quoting=csv.QUOTE_NONE, escapechar='\\')

    with open(args.input_csv, mode='r') as file:
        csv_reader = csv.reader(file)
        line = ['Faults', 'Nodes', 'Rate', 'Size', 'Is_Attack', 'Attack_Level', 'TPS', 'Latency ms']
        csv_writer.writerow(line)
        # Iterate through each row in the CSV
        for index, row in enumerate(csv_reader):
            # Remove any extra spaces and assign to variables
            faults = int(row[0].strip())
            rate = int(row[1].strip())
            is_attack = row[2].strip().lower() == 'true'
            attack_level = int(row[3].strip())
            cmd = ''
            if is_attack:
                cmd = f'fab remote --faults {faults} --rate {rate} --attackLevel {attack_level} --numNodes {args.nodes} --size {args.size} --isAttack'
            else:
                cmd = f'fab remote --faults {faults} --rate {rate} --attackLevel {attack_level} --numNodes {args.nodes} --size {args.size}'
            print(cmd)
            os.system(cmd)

            file = f'results/bench-{faults}-{args.nodes}-{1}-{True}-{rate}-{args.size}-{is_attack}-{attack_level}.txt'

            metrics = extract_end_to_end_metrics(file)

            if metrics[0] is None or metrics[1] is None:
                continue
            else:
                metrics.insert(0, str(attack_level))
                metrics.insert(0, str(is_attack))
                metrics.insert(0, str(args.size))
                metrics.insert(0, str(rate))
                metrics.insert(0, str(args.nodes))
                metrics.insert(0, str(faults))
                csv_writer.writerow(metrics)
                output_file.flush()
