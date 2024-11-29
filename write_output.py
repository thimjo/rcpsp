import csv


def initialize_csv(output_file_path: str):
    try:
        with open(output_file_path, mode="x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["project-id", "makespan", "optimality-gap"])  # Header row
    except FileExistsError:
        # File already exists; do nothing
        pass


# Append a tuple to the CSV file
def append_to_csv(file_path: str, data: [str, int, int]):
    with open(file_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(data)
