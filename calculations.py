import math

def determining_factor_calculated(flow, rp):
    square_root_rp = math.sqrt(rp)
    det_calc = flow / square_root_rp
    det_formatted = "{:.2f}".format(det_calc)
    return det_formatted

def q_calculated(det_factor, rp):
    square_root_rp = math.sqrt(rp)
    q_calc = det_factor * square_root_rp
    q_formatted = "{:.2f}".format(q_calc)
    return q_formatted

def pressure_calculated(det_factor, flow):
    pressure_calc = (flow / det_factor) ** 2
    pressure_formatted = "{:.2f}".format(pressure_calc)
    return pressure_formatted

def pressure_calc_2(shc, density):
    pc2 = shc * density
    return pc2


def bounds(value1, value2):
    bound = (value1/value2) * 100
    return bound