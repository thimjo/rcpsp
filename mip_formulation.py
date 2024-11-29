from docplex.mp.model import Model
from docplex.mp.dvar import Var

from rcpsp import RCPSP

class MIP:
    def __init__(self, mdl:Model):
        self.mdl = mdl


def build_mip_formulation(rcpsp: RCPSP):
    mdl = Model()

    binary_start_times = build_binary_start_times(mdl, rcpsp)
    build_precedences(mdl, binary_start_times, rcpsp)
    build_resource_constraints(mdl, binary_start_times, rcpsp)
    mk = build_objective(mdl, binary_start_times, rcpsp)

    return MIP(mdl)


def build_binary_start_times(mdl: Model, rcpsp: RCPSP) -> list[list[Var]]:
    binary_start_times = []
    for i in range(0, rcpsp.num_tasks):
        i_start = []
        for t in range(0, rcpsp.horizon):
            i_start.append(mdl.binary_var(f"{i}_{t}"))
        binary_start_times.append(i_start)
        mdl.add(mdl.sum(i_start) == 1)  # each task has a single start-time

    return binary_start_times


def build_precedences(mdl: Model, start_times: list[list[Var]], rcpsp: RCPSP):
    for precedence in rcpsp.precedences:
        pred = precedence[0]
        suc = precedence[1]

        pred_start = 0
        suc_start = 0
        for t in range(0, rcpsp.horizon):
            pred_start += t * start_times[pred][t]
            suc_start += t * start_times[suc][t]
        pred_dur = rcpsp.duration[pred]

        constraint = (suc_start - pred_start >= pred_dur)
        mdl.add(constraint)


def build_resource_constraints(mdl: Model, start_times: list[list[Var]], rcpsp: RCPSP):
    num_resources = len(rcpsp.capacity)
    for r in range(0, num_resources):
        r_c = rcpsp.capacity[r]
        for t in range(0, rcpsp.horizon):
            resource_util = 0
            for i in range(0, rcpsp.num_tasks):
                i_dur = rcpsp.duration[i]
                i_r_req = rcpsp.requirements[i][r]
                i_uses_r_in_t = 0
                m_max = min(t + i_dur, rcpsp.horizon)
                for m in range(t, m_max):
                    i_uses_r_in_t += start_times[i][m]
                resource_util += (i_r_req * i_uses_r_in_t)

            mdl.add(resource_util <= r_c)


def build_objective(mdl: Model, start_times: list[list[Var]], rcpsp: RCPSP):
    i_dummy_sink = rcpsp.num_tasks - 1
    mk = 0
    for t in range(0, rcpsp.horizon):
        mk += start_times[i_dummy_sink][t] * t
    mdl.minimize(mk)

    return mk
