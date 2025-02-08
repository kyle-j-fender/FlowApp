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

    # st.markdown("# Calculations")
    # st.sidebar.markdown("# User Input")
    col0, col1, col2, col3 = st.columns([1, 1, 1, 1])

    col0.subheader("Inputs", divider=True)
    col1.subheader("K-Factor", divider=True)
    col2.subheader("Q - Flow", divider=True)
    col3.subheader("Required Pressure", divider=True)

    if 'df_parent' not in st.session_state:
        st.session_state.df_parent = pd.DataFrame(
        [
            {"Field": "K-Factor", "Value": 5.6},
            {"Field": "Q-Flow", "Value": 15.4},
            {"Field": "Required Pressure", "Value": 7},
        ]
    )

    if 'df_sprinkler' not in st.session_state:
        st.session_state.df_sprinkler = pd.DataFrame(
            [
                {"Field": "Sprinkler Head Coverage (Sq. Ft)", "Value": 5.6},
                {"Field": "Q-Flow", "Value": 15.4},
            ]
        )

    # Function to update dependent DataFrames
    def update_dependent_dataframes():
        df_parent = st.session_state.df_parent

        # Update first child DataFrame
        st.session_state.df_child1 = pd.DataFrame(
            [
                {"Field": "K-Factor", "Value": calc.determining_factor_calculated(df_parent.loc[1,'Value'],df_parent.loc[2,'Value'])},
                {"Field": "Q-Flow", "Value": "{:.2f}".format(df_parent.loc[1,'Value'])},
                {"Field": "Required Pressure", "Value": "{:.2f}".format(df_parent.loc[2,'Value'])},
            ]
        )

        st.session_state.df_child2 = pd.DataFrame(
            [
                {"Field": "K-Factor", "Value": "{:.2f}".format(df_parent.loc[0, 'Value'])},
                {"Field": "Q-Flow", "Value": calc.q_calculated(df_parent.loc[0, 'Value'],df_parent.loc[2, 'Value'])},
                {"Field": "Required Pressure", "Value": "{:.2f}".format(df_parent.loc[2, 'Value'])},
            ]
        )

        st.session_state.df_child3 = pd.DataFrame(
            [
                {"Field": "K-Factor", "Value": "{:.2f}".format(df_parent.loc[0, 'Value'])},
                {"Field": "Q-Flow", "Value": "{:.2f}".format(df_parent.loc[1,'Value'])},
                {"Field": "Required Pressure", "Value": calc.pressure_calculated(df_parent.loc[0, 'Value'],df_parent.loc[1, 'Value'])},
            ]
        )

    def update_dependent_dataframes1():
        df_sprinkler = st.session_state.df_sprinkler

        st.session_state.df_child4 = pd.DataFrame(
            [
                {"Field": "Pressure", "Value": calc.pressure_calc_2(df_sprinkler.loc[0, 'Value'], df_sprinkler.loc[1, 'Value'])}
            ]
        )

    if 'df_child1' not in st.session_state:
        update_dependent_dataframes()

    if 'df_child2' not in st.session_state:
        update_dependent_dataframes()

    if 'df_child3' not in st.session_state:
        update_dependent_dataframes()

    if 'df_child4' not in st.session_state:
        update_dependent_dataframes1()

    edited_df = col0.data_editor(st.session_state.df_parent, key="df_editor",hide_index=True,use_container_width=True)

    if not edited_df.equals(st.session_state.df_parent):
        st.session_state.df_parent = edited_df
        update_dependent_dataframes()

    second_table = col1.data_editor(st.session_state.df_child1,hide_index=True,use_container_width=True, disabled=True)
    third_table = col2.data_editor(st.session_state.df_child2, hide_index=True, use_container_width=True, disabled=True)
    fourth_table = col3.data_editor(st.session_state.df_child3, hide_index=True, use_container_width=True, disabled=True)

    st.divider()

    col5, col6 = st.columns([1, 1])
    col5.subheader("Flow", divider=True)
    col5.caption("This is pressure based on sprinkler head coverage and flow.")
    edited_df_sprinkler = col5.data_editor(st.session_state.df_sprinkler, key="df_editor_6", hide_index=True, use_container_width=True)

    if not edited_df_sprinkler.equals(st.session_state.df_sprinkler):
        st.session_state.df_sprinkler = edited_df_sprinkler
        update_dependent_dataframes1()

    fifth_table = col5.data_editor(st.session_state.df_child4, hide_index=True, use_container_width=True, disabled=True)

    # edited_df = col0.data_editor(df,hide_index=True,use_container_width=True)
    # kfactor_input = edited_df.loc[0,'Value']
    # qflow_input = edited_df.loc[1,'Value']
    # requiredpressure_input = edited_df.loc[2,'Value']
    #

    col6.subheader("Basic Calculations", divider=True)

    sqroot = col6.number_input(
        "Square Root", value=4.543, placeholder="Type a number...", format="%0.3f"
    )
    sq_answer = calc.square_root_eq(sqroot)
    sq_display = col6.container(height=100)
    shp_display = sq_display.metric(label="Squared Root", value=sq_answer)

    squared = col6.number_input(
        "Squared", value=5.432, placeholder="Type a number", format="%0.3f"
    )
    squared_answer = calc.squared(squared)
    squared_display = col6.container(height=100)
    squaredanswer_display = squared_display.metric(label="Squared", value=squared_answer)

    st.divider()

    col7, col8 = st.columns([1, 1])

    col7.subheader("Distance (Head to Wall)", divider=True)
    hw_feet = col7.number_input(
        "Feet (HW)", value=5.678, placeholder="Type a number...", format="%0.3f"
    )
    hw_inches = col7.number_input(
        "Inches (HW)", value=5.4534, placeholder="Type a number...", format="%0.3f"
    )
    hw_answer = calc.hw_total(hw_feet, hw_inches)
    hw_display = col7.metric(label = "Head to Wall (Conversion)", value=hw_answer)

    col8.subheader("Distance (Head to Head)", divider=True)
    hh_feet = col8.number_input(
        "Feet (HH)", value=5.54354, placeholder="Type a number...", format="%0.3f"
    )
    hh_inches = col8.number_input(
        "Inches (HH)", value=23.48434, placeholder="Type a number...", format="%0.3f"
    )
    hh_answer = calc.hh_total(hh_feet, hh_inches)
    hh_display = col8.metric(label = "Head to Head (Conversion)", value = hh_answer)

    st.divider()
    st.header("Distance", divider=True)

    col9, col10 = st.columns([1, 1])

    distance_east = col9.number_input(
        "East (Feet in Decimals)", value=5.323, placeholder="Type a number...", format="%0.3f"
    )
    distance_west = col9.number_input(
        "West (Feet in Decimals)", value=5.321, placeholder="Type a number...", format="%0.3f"
    )
    distance_north = col9.number_input(
        "North (Feet in Decimals)", value=5.123, placeholder="Type a number...", format="%0.3f"
    )
    distance_south = col9.number_input(
        "South (Feet in Decimals)", value=5.534, placeholder="Type a number...", format="%0.3f"
    )

    e2w = calc.distance_calculation(distance_east, distance_west)
    n2s = calc.distance_calculation(distance_north, distance_south)
    sca = calc.area_calculation(e2w, n2s)

    e2w_display = col10.metric(label="East to West Distance (Ft)", value=e2w)
    n2s_display = col10.metric(label="North to South (Ft)", value=n2s)
    sca_display = col10.metric(label="Sprinker Coverage Area (Ft^2)", value=sca)

    # # Calulated K-Factor (based on Q-Flow and Required Pressure)
    # det_calc = calc.determining_factor_calculated(qflow_input,requiredpressure_input)
    # kfactor_df = pd.DataFrame(
    #     [
    #         {"Field": "K-Factor", "Value": det_calc},
    #         {"Field": "Q-Flow", "Value": qflow_input},
    #         {"Field": "Required Pressure", "Value": requiredpressure_input},
    #     ]
    # )
    # kfactor_table = col1.data_editor(kfactor_df,hide_index=True,use_container_width=True,disabled=True)


    # shc_on = st.sidebar.toggle("Sprinkler Head (Sq. Footage)")
    # if shc_on:
    #     sprinkler_head_pressure = st.sidebar.number_input("Sprinkler Head Coverage", value=5)
    #
    # density_on = st.sidebar.toggle("Density")
    # if density_on:
    #     density = st.sidebar.number_input("Density", value=0.05)
    #
    # df_on = st.sidebar.toggle("K-Factor")
    # if df_on:
    #     determining_factor = st.sidebar.number_input("K-Factor", value=5.6)
    #
    # square_root_on = st.sidebar.toggle("Square Root")
    # if square_root_on:
    #     square_root_input = st.sidebar.number_input("What do you need the square root of?", value=256)
    #
    # squared_on = st.sidebar.toggle("Squared")
    # if squared_on:
    #     squared_input = st.sidebar.number_input("What do you need squared?", value = 12)

    # flow_on = st.sidebar.toggle("Q")
    # if flow_on:
    #     flow = st.sidebar.number_input("Q", value=22.5)
    #
    # rp_on = st.sidebar.toggle("P (Required Pressure)")
    # if rp_on:
    #     required_pressure = st.sidebar.number_input("Required Pressure", value=16.14)
    #     square_root_rp = math.sqrt(required_pressure)

    # if (shc_on & density_on & df_on) | squared_on | square_root_on:
    #     if (shc_on & density_on & df_on):
    #         col0.subheader("Inputs", divider=True)
    #         col0.caption("Inputs from the user.")
    #         col1.subheader("Q - Flow", divider=True)
    #         col1.caption("This is the calculated flow.")
    #         col2.subheader("P (Required Pressure)", divider=True)
    #         col2.caption("This is the pressure at the node.")
    #
    #         shp_container = col0.container(height=120)
    #         density_container = col0.container(height=120)
    #         kfactor_container = col0.container(height=120)
    #         flow_column_display = col1.container(height=120)
    #         pressure_display = col2.container(height=120)
    #
    #         shp_display = shp_container.metric(label="SHP", value=sprinkler_head_pressure)
    #         density_display = density_container.metric(label="Density", value=density)
    #         kfactor_display = kfactor_container.metric(label="K-Factor", value=determining_factor)
    #         flow_calc_shp = sprinkler_head_pressure * density
    #         flow_calc_display = flow_column_display.metric(label="Flow", value=flow_calc_shp)
    #         rp_calc = (flow_calc_shp / determining_factor) ** 2
    #         rp_calc_formatted = "{:.2f}".format(rp_calc)
    #         rp_display = pressure_display.metric(label="PSI (from K-Factor & Q)", value=rp_calc_formatted)
    #     if squared_on | square_root_on:
    #         col3.subheader("Additional Math", divider=True)
    #         col3.caption("This is for additional math that may be necessary.")
    #         if square_root_on:
    #             square_root_container = col3.container(height=120)
    #             square_root_calc = math.sqrt(square_root_input)
    #             square_root_display = square_root_container.metric(label="Square Root", value=square_root_calc)
    #         if squared_on:
    #             squared_container = col3.container(height=120)
    #             squared_calc = squared_input ** 2
    #             squared_display = squared_container.metric(label="Squared", value=squared_calc)
    # else:
    #     st.title("Please input values into the sidebar before proceeding.")


    # if flow_on & rp_on:
    #     det_calc = calc.determining_factor_calculated(flow, square_root_rp)
    #     det_calc_formatted = "{:.3f}".format(det_calc)
    #     det_display = det_calculation_box.metric(label="Calculated", value=det_calc_formatted)
    # if df_on & flow_on & rp_on:
    #     det_verification_box = sub1_col2.container(height=120)
    #     dm_bound1 = calc.bounds(determining_factor,det_calc)
    #     dm_bound2 = calc.bounds(det_calc,determining_factor)
    #     det_metric_calc_formatted = "{:.1f}%".format(dm_bound1)
    #     range_des = "hello"
    #     if (98< dm_bound1 < 102) or (98 < dm_bound2 < 102):
    #         range_des = "In Range"
    #     else:
    #         range_des = "Out of Range"
    #     det_metric = det_verification_box.metric(label="Match", value=det_metric_calc_formatted, delta=range_des)
    #
    # sub2_col1, sub2_col2 = col2.columns([1,1])
    # sub2_col1_1, sub2_col2_2 = col2.columns([1,1])
    # flow_calculation_box = sub2_col1.container(height=120)
    # flow_shp_box = sub2_col1_1.container(height=120)
    # flow_match_box_shp = sub2_col2_2.container(height=120)
    # if df_on & rp_on:
    #     flow_calc = determining_factor * square_root_rp
    #     flow_calc_formatted = "{:.3f}".format(flow_calc)
    #     flow_display = flow_calculation_box.metric(label="Q (from DF & RP)", value=flow_calc_formatted)
    #     flow_calc_shp = sprinkler_head_pressure * density
    #     flow_calculation_shp = flow_shp_box.metric(label="Q (from SHP and Density)", value=flow_calc_shp)
    # if df_on & flow_on & rp_on:
    #     flow_verification_box = sub2_col2.container(height=120)
    #     flow_bound1 = calc.bounds(flow_calc, flow)
    #     flow_bound2 = calc.bounds(flow, flow_calc)
    #     flow_metric_calc_formatted = "{:.1f}%".format(flow_bound1)
    #     range_flow = "hello"
    #     if (98 < flow_bound1 < 102) or (98 < flow_bound2 < 102):
    #         range_flow = "In Range"
    #     else:
    #         range_flow = "Out of Range"
    #     flow_metric = flow_verification_box.metric(label="Match", value=flow_metric_calc_formatted, delta=range_flow)
    #     flow_bound1_shp = calc.bounds(flow_calc_shp, flow)
    #     flow_bound2_shp = calc.bounds(flow, flow_calc_shp)
    #     flow_metric_calc_formatted_shp = "{:.1f}%".format(flow_bound1_shp)
    #     range_flow_shp = "hello"
    #     if (98 < flow_bound1_shp < 102) or (98 < flow_bound2_shp < 102):
    #         range_flow_shp = "In Range"
    #     else:
    #         range_flow_shp = "Out of Range"
    #     flow_metric_shp = flow_match_box_shp.metric(label="Match", value=flow_metric_calc_formatted_shp, delta=range_flow_shp)
    #
    # sub3_col1, sub3_col2 = col3.columns([1,1])
    # rp_calculation_box = sub3_col1.container(height=120)
    # if df_on & flow_on:
    #     rp_calc = (flow/determining_factor) ** 2
    #     rp_calc_formatted = "{:.2f}".format(rp_calc)
    #     rp_display = rp_calculation_box.metric(label="PSI (from K-Factor & Q)", value=rp_calc_formatted)
    # if df_on & flow_on & rp_on:
    #     rp_verification_box = sub3_col2.container(height=120)
    #     rp_bound1 = calc.bounds(rp_calc, required_pressure)
    #     rp_bound2 = calc.bounds(required_pressure, rp_calc)
    #     rp_metric_calc_formatted = "{:.1f}%".format(rp_bound1)
    #     range_rp = "hello"
    #     if (98 < rp_bound1 < 102) or (98 < rp_bound2 < 102):
    #         range_rp = "In Range"
    #     else:
    #         range_rp = "Out of Range"
    #     rp_metric = rp_verification_box.metric(label="Match", value=rp_metric_calc_formatted, delta=range_rp)
    #
    # json_file_path = 'KStandards.json'  # Replace with your JSON file path
    # df = ji.json_to_dataframe(json_file_path)
    #
    # if df_on:
    #     closest_row = ji.get_closest_value(df, 'Nominal K-Factor', determining_factor)
    # elif (flow_on & rp_on) & (df_on == False):
    #     closest_row = ji.get_closest_value(df, 'Nominal K-Factor', det_calc)
    #
    # nkf = ji.get_nominal_kfactor(closest_row)
    # min = ji.get_nominal_kfactor_min(closest_row)
    # max = ji.get_nominal_kfactor_max(closest_row)
    # percent = ji.get_nominal_kfactor_percent(closest_row)
    # thread = ji.get_nominal_kfactor_thread(closest_row)
    #
    # st1, st2, st3, st4, st5 = st.columns([1,1,1,1,1])
    # nearest_container = st1.container(height=120)
    # nearest_display = nearest_container.metric(label="Nearest K-Factor", value=nkf)
    #
    # min_container = st2.container(height=120)
    # min_display = min_container.metric(label="Min K-Factor", value=min)
    #
    # max_container = st3.container(height=120)
    # max_display = max_container.metric(label="Max K-Factor", value=max)
    #
    # percent_container = st4.container(height=120)
    # percent_setup = percent * 100
    # percent_formatted = "{}%".format(percent_setup)
    # percent_display = percent_container.metric(label="Percent of Discharge", value=percent_formatted)
    #
    # thread_container = st5.container(height=120)
    # thread_display = thread_container.metric(label="Thread Type", value=thread)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
