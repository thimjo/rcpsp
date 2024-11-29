import re


class RCPSP:
    def __init__(self,
                 num_tasks: int,
                 duration: list[int],
                 requirements: list[list[int]],
                 capacity: list[int],
                 precedences: list[tuple[int, int]],
                 horizon: int):
        self.num_tasks = num_tasks
        self.duration = duration
        self.requirements = requirements
        self.capacity = capacity
        self.precedences = precedences
        self.horizon = horizon


def read_from_psplib_file(file_path: str) -> "RCPSP":
    """
    Parse a PSPLIB instance file and create an RCPSP instance.

    :param file_path: Path to the PSPLIB instance file.
    :return: An RCPSP object.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    num_tasks_line = lines[5]
    num_tasks = int(''.join(filter(str.isdigit, num_tasks_line)))

    num_resources_line = lines[8]
    num_resources = int(''.join(filter(str.isdigit, num_resources_line)))

    duration = read_durations(lines, num_tasks)
    resource_requirements = read_resource_requirements(lines, num_tasks, num_resources)
    resource_capacity = read_resource_capacity(lines, num_tasks)
    precedences = read_precedences(lines, num_tasks)

    horizon_line = lines[6]
    horizon = int(''.join(filter(str.isdigit, horizon_line)))

    return RCPSP(num_tasks, duration, resource_requirements, resource_capacity, precedences, horizon)


def read_durations(lines: list[str], num_tasks: int) -> list[int]:
    duration_lines_start = 18 + num_tasks + 4
    if "DURATIONS" not in lines[duration_lines_start - 3]:
        raise ValueError("The file does not have the expected structure!")

    duration: list[int] = []
    for duration_line in lines[duration_lines_start: duration_lines_start+num_tasks]:
        extracted_numbers = re.findall(r'\d+', duration_line)
        duration.append(int(extracted_numbers[2]))

    return duration


def read_resource_requirements(lines: list[str], num_tasks: int, num_resources: int) -> list[list[int]]:
    reqs_lines_start = 18 + num_tasks + 4
    if "REQUESTS" not in lines[reqs_lines_start - 3]:
        raise ValueError("The file does not have the expected structure!")

    resource_requirements: list[list[int]] = []
    for reqs_line in lines[reqs_lines_start: reqs_lines_start + num_tasks]:
        extracted_numbers = re.findall(r'\d+', reqs_line)
        task_reqs: list[int] = []
        for r in range(0, num_resources):
            req = int(extracted_numbers[3 + r])
            task_reqs.append(req)
        resource_requirements.append(task_reqs)

    return resource_requirements


def read_precedences(lines: list[str], num_tasks: int) -> list[tuple[int, int]]:
    precedence_lines_start = 18
    if "PRECEDENCE RELATIONS" not in lines[precedence_lines_start-2]:
        raise ValueError("The file does not have the expected structure!")

    precedences: list[tuple[int, int]] = []
    for precedences_line in lines[precedence_lines_start : precedence_lines_start + num_tasks]:
        extracted_numbers = re.findall(r'\d+', precedences_line)
        if len(extracted_numbers) < 4:
            pass

        pred = int(extracted_numbers[0]) - 1
        for suc_string in extracted_numbers[3: len(extracted_numbers)]:
            suc = int(suc_string) - 1
            precedence = (pred, suc)
            precedences.append(precedence)

    return precedences


def read_resource_capacity(lines: list[str], num_tasks: int) -> list[int]:
    capacities_line_index = 18 + num_tasks + 4 + num_tasks + 3
    if "RESOURCEAVAILABILITIES" not in lines[capacities_line_index - 2]:
        raise ValueError("The file does not have the expected structure!")

    capacities_line = lines[capacities_line_index]
    extracted_numbers = re.findall(r'\d+', capacities_line)
    capacities: list[int] = []
    for c in extracted_numbers:
        capacities.append(int(c))

    return capacities
