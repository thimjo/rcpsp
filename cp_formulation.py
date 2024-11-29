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
    intervals = []
    for i in range(0, rcpsp.num_tasks):
        duration = rcpsp.duration[i]
        interval = interval_var(name=str(i))
        interval.set_size_min(duration)
        interval.set_size_max(duration)
        intervals.append(interval)

    return intervals


def build_precedences(mdl: CpoModel, rcpsp: RCPSP, intervals: list[CpoIntervalVar]):
    for edge in rcpsp.precedences:
        pred = intervals[edge[0]]
        suc = intervals[edge[1]]
        precedence = modeler.end_before_start(pred, suc)
        mdl.add(precedence)


def build_resource_constraints(mdl: CpoModel, rcpsp: RCPSP, intervals: list[CpoIntervalVar]):
    num_resources = len(rcpsp.capacity)

    for r in range(0, num_resources):
        c = rcpsp.capacity[r]
        cum_r = modeler.step_at(0, c)
        for i in range(0, len(intervals)):
            interval = intervals[i]
            req = rcpsp.requirements[i][r]
            if req > 0:
                cum_r -= modeler.pulse(interval, req)
        mdl.add(cum_r >= 0)


def build_objective(mdl: CpoModel, intervals: list[CpoIntervalVar]) -> CpoExpr:
    ends = []
    for interval in intervals:
        ends.append(modeler.end_of(interval))

    mk = modeler.max(ends)
    objective = modeler.minimize(mk)
    mdl.add(objective)

    return mk
