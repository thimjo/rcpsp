from ortools.sat.python import cp_model
from rcpsp import RCPSP


class OrToolsFormulation:
    def __init__(self, mdl:cp_model.CpSolver, mk: cp_model.IntVar):
        self.mdl = mdl
        self.mk = mk


    def makespan_value(self) -> int:
        return self.mdl.get_obje


def solve(or_formulation: OrToolsFormulation, time_limit: int) -> [int, int]:
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit

    status = solver.Solve(or_formulation.mdl)
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        makespan = or_formulation.mk

        best_obj = solver.ObjectiveValue()
        best_bound = solver.BestObjectiveBound()
        gap = best_obj - best_bound
        return solver.Value(makespan), gap

    return "error", -1, -1


def build_or_tools_formulation(rcpsp: RCPSP) -> OrToolsFormulation:
    mdl = cp_model.CpModel()

    intervals = build_intervals(rcpsp)
    build_precedences(mdl, rcpsp, intervals)
    build_resource_constraints(mdl, rcpsp, intervals)
    mk = build_objective(mdl, intervals)

    return OrToolsFormulation(mdl, mk)


def build_intervals(rcpsp: RCPSP) -> list[cp_model.IntervalVar]:
    raise NotImplementedError("Interval-variables have not been created!")
    intervals = []
    for i in range(0, rcpsp.num_tasks):
        # todo: create and initialize an interval per task
        interval = ...
        intervals.append(interval)

    return intervals


def build_precedences(mdl: cp_model.CpModel, rcpsp: RCPSP, intervals: list[cp_model.IntervalVar]):
    raise NotImplementedError("Precedence constraints have not been formulated!")
    for edge in rcpsp.precedences:
        # todo: formulate precedence-constraint
        precedence = ...
        mdl.add(precedence)


def build_resource_constraints(mdl: cp_model.CpModel, rcpsp: RCPSP, intervals: list[cp_model.IntervalVar]):
    raise NotImplementedError("Resource constraints have not been formulated!")
    num_resources = len(rcpsp.capacity)
    for r in range(0, num_resources):
        capacity = rcpsp.capacity[r]
        capacity_function = modeler.step_at(0, capacity)
        demand_function = modeler.step_at(0, 0)
        for i in range(0, len(intervals)):
            # todo: add task-demand
            task_demand = ...
            demand_function += task_demand
        # todo: formulate resource constraint
        resource_constraint = ...
        mdl.add(resource_constraint)


def build_objective(mdl: cp_model.CpModel, intervals: list[cp_model.IntervalVar]) -> cp_model.IntVar:
    raise NotImplementedError("The expression for the objective function has not been formulated!")
    # todo: formulate the makespan expression
    mk = ...

    objective = modeler.minimize(mk)
    mdl.add(objective)

    return mk
