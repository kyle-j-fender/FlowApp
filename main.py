# This is a sample Python script.
import streamlit as st
import math
import calculations as calc
import pandas as pd
import numpy as np
import jsonImport as ji

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    st.markdown("# Calculations")
    st.sidebar.markdown("# User Input")
    col1, col2, col3 = st.columns([1, 1, 1])

    shc_on = st.sidebar.toggle("Sprinkler Head (Sq. Footage)")
    if shc_on:
        sprinkler_head_pressure = st.sidebar.number_input("Sprinkler Head Coverage", value=5)

    density_on = st.sidebar.toggle("Density")
    if density_on:
        density = st.sidebar.number_input("Density", value=0.05)

    df_on = st.sidebar.toggle("K-Factor")
    if df_on:
        determining_factor = st.sidebar.number_input("K-Factor", value=5.6)

    flow_on = st.sidebar.toggle("Q")
    if flow_on:
        flow = st.sidebar.number_input("Q", value=22.5)

    rp_on = st.sidebar.toggle("P (Required Pressure)")
    if rp_on:
        required_pressure = st.sidebar.number_input("Required Pressure", value=16.14)
        square_root_rp = math.sqrt(required_pressure)

    col1.subheader("K-Factor", divider = True)
    col1.caption("The equivalent K at a node.")
    col2.subheader("Q - Flow", divider = True)
    col2.caption("This is the calculated flow.")
    col3.subheader("P (Required Pressure)", divider = True)
    col3.caption("This is the pressure at the node.")


    sub1_col1, sub1_col2 = col1.columns([1,1])
    det_calculation_box = sub1_col1.container(height=120)
    if flow_on & rp_on:
        det_calc = calc.determining_factor_calculated(flow, square_root_rp)
        det_calc_formatted = "{:.3f}".format(det_calc)
        det_display = det_calculation_box.metric(label="Calculated", value=det_calc_formatted)
    if df_on & flow_on & rp_on:
        det_verification_box = sub1_col2.container(height=120)
        dm_bound1 = calc.bounds(determining_factor,det_calc)
        dm_bound2 = calc.bounds(det_calc,determining_factor)
        det_metric_calc_formatted = "{:.1f}%".format(dm_bound1)
        range_des = "hello"
        if (98< dm_bound1 < 102) or (98 < dm_bound2 < 102):
            range_des = "In Range"
        else:
            range_des = "Out of Range"
        det_metric = det_verification_box.metric(label="Match", value=det_metric_calc_formatted, delta=range_des)

    sub2_col1, sub2_col2 = col2.columns([1,1])
    sub2_col1_1, sub2_col2_2 = col2.columns([1,1])
    flow_calculation_box = sub2_col1.container(height=120)
    flow_shp_box = sub2_col1_1.container(height=120)
    flow_match_box_shp = sub2_col2_2.container(height=120)
    if df_on & rp_on:
        flow_calc = determining_factor * square_root_rp
        flow_calc_formatted = "{:.3f}".format(flow_calc)
        flow_display = flow_calculation_box.metric(label="Q (from DF & RP)", value=flow_calc_formatted)
        flow_calc_shp = sprinkler_head_pressure * density
        flow_calculation_shp = flow_shp_box.metric(label="Q (from SHP and Density)", value=flow_calc_shp)
    if df_on & flow_on & rp_on:
        flow_verification_box = sub2_col2.container(height=120)
        flow_bound1 = calc.bounds(flow_calc, flow)
        flow_bound2 = calc.bounds(flow, flow_calc)
        flow_metric_calc_formatted = "{:.1f}%".format(flow_bound1)
        range_flow = "hello"
        if (98 < flow_bound1 < 102) or (98 < flow_bound2 < 102):
            range_flow = "In Range"
        else:
            range_flow = "Out of Range"
        flow_metric = flow_verification_box.metric(label="Match", value=flow_metric_calc_formatted, delta=range_flow)
        flow_bound1_shp = calc.bounds(flow_calc_shp, flow)
        flow_bound2_shp = calc.bounds(flow, flow_calc_shp)
        flow_metric_calc_formatted_shp = "{:.1f}%".format(flow_bound1_shp)
        range_flow_shp = "hello"
        if (98 < flow_bound1_shp < 102) or (98 < flow_bound2_shp < 102):
            range_flow_shp = "In Range"
        else:
            range_flow_shp = "Out of Range"
        flow_metric_shp = flow_match_box_shp.metric(label="Match", value=flow_metric_calc_formatted_shp, delta=range_flow_shp)

    sub3_col1, sub3_col2 = col3.columns([1,1])
    rp_calculation_box = sub3_col1.container(height=120)
    if df_on & flow_on:
        rp_calc = (flow/determining_factor) ** 2
        rp_calc_formatted = "{:.2f}".format(rp_calc)
        rp_display = rp_calculation_box.metric(label="PSI (from K-Factor & Q)", value=rp_calc_formatted)
    if df_on & flow_on & rp_on:
        rp_verification_box = sub3_col2.container(height=120)
        rp_bound1 = calc.bounds(rp_calc, required_pressure)
        rp_bound2 = calc.bounds(required_pressure, rp_calc)
        rp_metric_calc_formatted = "{:.1f}%".format(rp_bound1)
        range_rp = "hello"
        if (98 < rp_bound1 < 102) or (98 < rp_bound2 < 102):
            range_rp = "In Range"
        else:
            range_rp = "Out of Range"
        rp_metric = rp_verification_box.metric(label="Match", value=rp_metric_calc_formatted, delta=range_rp)

    json_file_path = 'KStandards.json'  # Replace with your JSON file path
    df = ji.json_to_dataframe(json_file_path)

    if df_on:
        closest_row = ji.get_closest_value(df, 'Nominal K-Factor', determining_factor)
    elif (flow_on & rp_on) & (df_on == False):
        closest_row = ji.get_closest_value(df, 'Nominal K-Factor', det_calc)

    nkf = ji.get_nominal_kfactor(closest_row)
    min = ji.get_nominal_kfactor_min(closest_row)
    max = ji.get_nominal_kfactor_max(closest_row)
    percent = ji.get_nominal_kfactor_percent(closest_row)
    thread = ji.get_nominal_kfactor_thread(closest_row)

    st1, st2, st3, st4, st5 = st.columns([1,1,1,1,1])
    nearest_container = st1.container(height=120)
    nearest_display = nearest_container.metric(label="Nearest K-Factor", value=nkf)

    min_container = st2.container(height=120)
    min_display = min_container.metric(label="Min K-Factor", value=min)

    max_container = st3.container(height=120)
    max_display = max_container.metric(label="Max K-Factor", value=max)

    percent_container = st4.container(height=120)
    percent_setup = percent * 100
    percent_formatted = "{}%".format(percent_setup)
    percent_display = percent_container.metric(label="Percent of Discharge", value=percent_formatted)

    thread_container = st5.container(height=120)
    thread_display = thread_container.metric(label="Thread Type", value=thread)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
