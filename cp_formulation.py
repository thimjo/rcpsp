from docplex.cp.expression import CpoExpr
from docplex.cp.expression import interval_var
import docplex.cp.modeler as modeler
from docplex.cp.model import CpoModel
from docplex.cp.model import CpoSolver
from docplex.cp.model import CpoIntervalVar

from rcpsp import RCPSP


class CpFormulation:
    def __init__(self, mdl:CpoModel, mk: CpoExpr):
        self.mdl = mdl
        self.mk = mk


    def makespan_value(self) -> int:
        return self.mdl.get_obje


def solve(cp_formulation: CpFormulation, time_limit: int) -> [int, int]:
    params = {'TimeLimit': time_limit}
    mdl = cp_formulation.mdl
    mdl.set_parameters(params)
    solver = CpoSolver(model=mdl)
    result = solver.solve()
    if result:
        return result.solution.objective_values[0], result.solution.objective_gaps[0]

    return "error", -1, -1


def build_cp_formulation(rcpsp: RCPSP) -> CpFormulation:
    mdl = CpoModel()

    intervals = build_intervals(rcpsp)
    build_precedences(mdl, rcpsp, intervals)
    build_resource_constraints(mdl, rcpsp, intervals)
    mk = build_objective(mdl, intervals)

    return CpFormulation(mdl, mk)


def build_intervals(rcpsp: RCPSP) -> list[CpoIntervalVar]:
    raise NotImplementedError("Interval-variables have not been created!")
    intervals = []
    for i in range(0, rcpsp.num_tasks):
        # todo: create and initialize an interval per task
        interval = ...
        intervals.append(interval)

    return intervals


def build_precedences(mdl: CpoModel, rcpsp: RCPSP, intervals: list[CpoIntervalVar]):
    raise NotImplementedError("Precedence constraints have not been formulated!")
    for edge in rcpsp.precedences:
        # todo: formulate precedence-constraint
        precedence = ...
        mdl.add(precedence)


def build_resource_constraints(mdl: CpoModel, rcpsp: RCPSP, intervals: list[CpoIntervalVar]):
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


def build_objective(mdl: CpoModel, intervals: list[CpoIntervalVar]) -> CpoExpr:
    raise NotImplementedError("The expression for the objective function has not been formulated!")
    # todo: formulate the makespan expression
    mk = ...

    objective = modeler.minimize(mk)
    mdl.add(objective)

    return mk
