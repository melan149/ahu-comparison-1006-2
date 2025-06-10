import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px # Import plotly for charting
import plotly.graph_objects as go # Import graph objects for more control if needed

# Load data
@st.cache_data
def load_data():
    # Assuming Data_2025.xlsx is in the same directory as app.py
    url = "Data_2025.xlsx"
    return pd.read_excel(url, sheet_name="data", engine='openpyxl')

df = load_data()

# Resolve potential column naming issues for robustness
def get_column_safe(df, name_options):
    for name in name_options:
        if name in df.columns:
            return name
    return None

unit_name_col = get_column_safe(df, ["Unit name", "Unit Name"])
region_col = get_column_safe(df, ["Region"])
year_col = get_column_safe(df, ["Year"])
quarter_col = get_column_safe(df, ["Quarter"])
recovery_col = get_column_safe(df, ["Recovery type", "Recovery Type", "Recovery_type"])
size_col = get_column_safe(df, ["Unit size", "Unit Size"])
brand_col = get_column_safe(df, ["Brand name", "Brand"])
logo_col = get_column_safe(df, ["Brand logo", "Brand Logo"])
unit_photo_col = get_column_safe(df, ["Unit photo", "Unit Photo", "Unit Photo Name"]) # Added common names for unit photo column

# Specific columns to trigger chart display below them in the table
internal_height_supply_filter_col = get_column_safe(df, ["Internal Height (Supply Filter)", "Internal Height Supply Filter"])
unit_cross_section_area_supply_fan_col = get_column_safe(df, ["Unit cross section area (Supply Fan)", "Unit cross section area Supply Fan"])


# --- Chart 1 specific coordinate column names (X1-X5, Y1-Y5) ---
coord_col_pairs_1_5 = []
for i in range(1, 6):
    x_col_name = get_column_safe(df, [f"X{i}", f"x{i}", f"X{i}_coord", f"x{i}_coord"])
    y_col_name = get_column_safe(df, [f"Y{i}", f"y{i}", f"Y{i}_coord", f"y{i}_coord"])
    if x_col_name and y_col_name:
        coord_col_pairs_1_5.append((x_col_name, y_col_name))

# --- Chart 2 specific coordinate column names (X6-X10, Y6-Y10) ---
coord_col_pairs_6_10 = []
for i in range(6, 11): # For X6, Y6 to X10, Y10
    x_col_name = get_column_safe(df, [f"X{i}", f"x{i}", f"X{i}_coord", f"x{i}_coord"])
    y_col_name = get_column_safe(df, [f"Y{i}", f"y{i}", f"Y{i}_coord", f"y{i}_coord"])
    if x_col_name and y_col_name:
        coord_col_pairs_6_10.append((x_col_name, y_col_name))


# Main layout filters for the comparison interface
st.title("Technical Data Comparison")

# Create two columns for side-by-side selection and display
col_filter1, col_filter2 = st.columns(2)

with col_filter1:
    selected_year1 = st.selectbox("Year", sorted(df[year_col].dropna().unique()), key="year1")
    selected_quarter1 = st.selectbox("Quarter", sorted(df[quarter_col].dropna().unique()), key="quarter1")
    selected_region1 = st.selectbox("Region", sorted(df[region_col].dropna().unique()), key="region1")
    selected_brand1 = st.selectbox("Select Brand", sorted(df[brand_col].dropna().unique()), key="brand1")

    brand1_logo_path = df[df[brand_col] == selected_brand1][logo_col].iloc[0] if not df[df[brand_col] == selected_brand1].empty and logo_col else None
    if brand1_logo_path:
        try:
            image1 = Image.open(f"images/{brand1_logo_path}")
            width1 = 150
            height1 = int(image1.height * (width1 / image1.width))
            image1 = image1.resize((width1, height1))
            st.image(image1, caption=f"Logo for {selected_brand1}")
        except FileNotFoundError:
            st.warning(f"Brand logo image not found for {selected_brand1}: images/{brand1_logo_path}")
        except Exception as e:
            st.warning(f"Error loading brand logo for {selected_brand1}: {e}")
    else:
        st.write("No logo available for selected brand.")

    selected_unit1 = st.selectbox("Unit name", sorted(df[unit_name_col].dropna().unique()), key="unit1")
    selected_recovery1 = st.selectbox("Recovery type", sorted(df[recovery_col].dropna().unique()), key="recovery1")
    selected_size1 = st.selectbox("Unit size", sorted(df[size_col].dropna().unique()), key="size1")


with col_filter2:
    selected_year2 = st.selectbox("Year", sorted(df[year_col].dropna().unique()), key="year2")
    selected_quarter2 = st.selectbox("Quarter", sorted(df[quarter_col].dropna().unique()), key="quarter2")
    selected_region2 = st.selectbox("Region", sorted(df[region_col].dropna().unique()), key="region2")
    selected_brand2 = st.selectbox("Select Brand", sorted(df[brand_col].dropna().unique()), key="brand2")

    brand2_logo_path = df[df[brand_col] == selected_brand2][logo_col].iloc[0] if not df[df[brand_col] == selected_brand2].empty and logo_col else None
    if brand2_logo_path:
        try:
            image2 = Image.open(f"images/{brand2_logo_path}")
            width2 = 150
            height2 = int(image2.height * (width2 / image2.width))
            image2 = image2.resize((width2, height2))
            st.image(image2, caption=f"Logo for {selected_brand2}")
        except FileNotFoundError:
            st.warning(f"Brand logo image not found for {selected_brand2}: images/{brand2_logo_path}")
        except Exception as e:
            st.warning(f"Error loading brand logo for {selected_brand2}: {e}")
    else:
        st.write("No logo available for selected brand.")

    selected_unit2 = st.selectbox("Unit name", sorted(df[unit_name_col].dropna().unique()), key="unit2")
    selected_recovery2 = st.selectbox("Recovery type", sorted(df[recovery_col].dropna().unique()), key="recovery2")
    selected_size2 = st.selectbox("Unit size", sorted(df[size_col].dropna().unique()), key="size2")

# Filter dataframes based on selected criteria for both comparison sets
filtered_df1 = df[
    (df[year_col] == selected_year1) &
    (df[quarter_col] == selected_quarter1) &
    (df[region_col] == selected_region1) &
    (df[brand_col] == selected_brand1) &
    (df[unit_name_col] == selected_unit1) &
    (df[recovery_col] == selected_recovery1) &
    (df[size_col] == selected_size1)
]

filtered_df2 = df[
    (df[year_col] == selected_year2) &
    (df[quarter_col] == selected_quarter2) &
    (df[region_col] == selected_region2) &
    (df[brand_col] == selected_brand2) &
    (df[unit_name_col] == selected_unit2) &
    (df[recovery_col] == selected_recovery2) &
    (df[size_col] == selected_size2)
]

# Display Unit Photos after dropdowns and before the comparison table
st.subheader("Unit Photo")
col_photo1, col_photo2 = st.columns(2)

with col_photo1:
    unit_photo_path1 = filtered_df1[unit_photo_col].values[0] if not filtered_df1.empty and unit_photo_col and unit_photo_col in filtered_df1.columns else None
    if unit_photo_path1:
        try:
            unit_image1 = Image.open(f"images/{unit_photo_path1}")
            st.image(unit_image1, caption=f"{selected_unit1} Photo")
        except FileNotFoundError:
            st.warning(f"Unit photo image not found for {selected_unit1}: images/{unit_photo_path1}")
        except Exception as e:
            st.warning(f"Error loading unit photo for {selected_unit1}: {e}")
    else:
        st.write("No unit photo available for this selection.")

with col_photo2:
    unit_photo_path2 = filtered_df2[unit_photo_col].values[0] if not filtered_df2.empty and unit_photo_col and unit_photo_col in filtered_df2.columns else None
    if unit_photo_path2:
        try:
            unit_image2 = Image.open(f"images/{unit_photo_path2}")
            st.image(unit_image2, caption=f"{selected_unit2} Photo")
        except FileNotFoundError:
            st.warning(f"Unit photo image not found for {selected_unit2}: images/{unit_photo_path2}")
        except Exception as e:
            st.warning(f"Error loading unit photo for {selected_unit2}: {e}")
    else:
        st.write("No unit photo available for this selection.")

st.markdown("---")


# Display comparison table if data is available for both selections
if not filtered_df1.empty and not filtered_df2.empty:
    st.subheader("Comparison Table")

    col1, col2, col3 = st.columns([2, 3, 3])
    with col1:
        st.markdown("**Parameter**")
    with col2:
        st.markdown(f"**{selected_brand1}**")
    with col3:
        st.markdown(f"**{selected_brand2}**")

    # List of columns to be excluded from the comparison table display
    excluded_cols_from_table = [
        brand_col, logo_col, unit_photo_col, year_col, quarter_col, region_col,
        unit_name_col, recovery_col, size_col,
        # unit_cross_section_area_supply_filter_col, # This row should now be shown in the table
        # internal_height_supply_fan_col # This row should now be shown in the table
    ]
    # Add all resolved coordinate column names to the excluded list
    for x_name, y_name in coord_col_pairs_1_5:
        excluded_cols_from_table.append(x_name)
        excluded_cols_from_table.append(y_name)
    for x_name, y_name in coord_col_pairs_6_10:
        excluded_cols_from_table.append(x_name)
        excluded_cols_from_table.append(y_name)


    chart1_displayed = False
    chart2_displayed = False

    for col in df.columns:
        # Display the row if it's not in the general exclusion list
        # Check if the column is NOT in the excluded list, and also NOT one of the chart trigger columns
        if col not in excluded_cols_from_table: # No need to check for chart trigger columns here specifically, they are in excluded_cols_from_table if we want them hidden
            val1 = filtered_df1[col].values[0] if col in filtered_df1.columns else "-"
            val2 = filtered_df2[col].values[0] if col in filtered_df2.columns else "-"
            
            row_col1, row_col2, row_col3 = st.columns([2, 3, 3])
            with row_col1:
                st.write(col)
            with row_col2:
                st.write(val1)
            with row_col3:
                st.write(val2)

        # Insert Chart 1 after "Internal Height (Supply Filter)" row
        if col == internal_height_supply_filter_col and not chart1_displayed:
            st.markdown("---")
            chart_data_1 = []
            
            # Ensure the specific coordinate columns for chart 1 are present in the filtered dataframes
            required_coord_cols_chart1 = [name for pair in coord_col_pairs_1_5 for name in pair]
            
            can_plot_brand1_chart1 = True
            if not filtered_df1.empty:
                for coord_col in required_coord_cols_chart1:
                    if coord_col not in filtered_df1.columns or pd.isna(filtered_df1[coord_col].values[0]):
                        can_plot_brand1_chart1 = False
                        break
            else:
                can_plot_brand1_chart1 = False

            can_plot_brand2_chart1 = True
            if not filtered_df2.empty:
                for coord_col in required_coord_cols_chart1:
                    if coord_col not in filtered_df2.columns or pd.isna(filtered_df2[coord_col].values[0]):
                        can_plot_brand2_chart1 = False
                        break
            else:
                can_plot_brand2_chart1 = False

            if can_plot_brand1_chart1:
                for i, (x_name, y_name) in enumerate(coord_col_pairs_1_5):
                    chart_data_1.append({
                        'X_coord_actual': filtered_df1[x_name].values[0],
                        'Y_coord_actual': filtered_df1[y_name].values[0],
                        'Display_Label': f"Left: {selected_year1}-{selected_quarter1}-{selected_brand1}-{selected_unit1}-{selected_size1}",
                        'Point_Order': i + 1
                    })
            
            if can_plot_brand2_chart1:
                for i, (x_name, y_name) in enumerate(coord_col_pairs_1_5):
                    chart_data_1.append({
                        'X_coord_actual': filtered_df2[x_name].values[0],
                        'Y_coord_actual': filtered_df2[y_name].values[0],
                        'Display_Label': f"Right: {selected_year2}-{selected_quarter2}-{selected_brand2}-{selected_unit2}-{selected_size2}",
                        'Point_Order': i + 1
                    })
            
            if chart_data_1:
                st.subheader("Internal Cross Section area (Supply Filter)") # New title for Chart 1
                chart_df_1 = pd.DataFrame(chart_data_1)
                chart_df_1 = chart_df_1.sort_values(by=['Display_Label', 'Point_Order'])
                
                fig1 = px.line(chart_df_1,
                               x="X_coord_actual", # Use actual values for X axis
                               y="Y_coord_actual", # Use actual values for Y axis
                               color="Display_Label",
                               line_group="Display_Label",
                               markers=True,
                               title=None, # Title is now set via subheader
                               hover_data={'X_coord_actual': True, 'Y_coord_actual': True}) # Still show actual in hover
                
                fig1.update_layout(
                    xaxis_title="Unit internal width_Supply Filter (mm)",
                    yaxis_title="Unit internal height_Supply Filter (mm)",
                    hovermode="x unified",
                    legend_title_text="Selection - Year-Quarter-Brand-Unit-Size",
                    xaxis_constrain="domain",
                    yaxis_constrain="domain",
                    showlegend=True
                )
                fig1.update_yaxes(scaleanchor="x", scaleratio=1)
                st.plotly_chart(fig1, use_container_width=True)
            elif not can_plot_brand1_chart1 and not can_plot_brand2_chart1:
                st.warning("No complete coordinate data (X1-X5, Y1-Y5) found for selected units to generate Chart 1. Please ensure data is present and valid for both selections.")
            st.markdown("---")
            chart1_displayed = True

        # Insert Chart 2 after "Unit cross section area (Supply Fan)" row
        if col == unit_cross_section_area_supply_fan_col and not chart2_displayed:
            st.markdown("---")
            chart_data_2 = []
            
            # Ensure the specific coordinate columns for chart 2 are present in the filtered dataframes
            required_coord_cols_chart2 = [name for pair in coord_col_pairs_6_10 for name in pair]

            can_plot_brand1_chart2 = True
            if not filtered_df1.empty:
                for coord_col in required_coord_cols_chart2:
                    if coord_col not in filtered_df1.columns or pd.isna(filtered_df1[coord_col].values[0]):
                        can_plot_brand1_chart2 = False
                        break
            else:
                can_plot_brand1_chart2 = False

            can_plot_brand2_chart2 = True
            if not filtered_df2.empty:
                for coord_col in required_coord_cols_chart2:
                    if coord_col not in filtered_df2.columns or pd.isna(filtered_df2[coord_col].values[0]):
                        can_plot_brand2_chart2 = False
                        break
            else:
                can_plot_brand2_chart2 = False

            if can_plot_brand1_chart2:
                for i, (x_name, y_name) in enumerate(coord_col_pairs_6_10):
                    chart_data_2.append({
                        'X_coord_actual': filtered_df1[x_name].values[0],
                        'Y_coord_actual': filtered_df1[y_name].values[0],
                        'Display_Label': f"Left: {selected_year1}-{selected_quarter1}-{selected_brand1}-{selected_unit1}-{selected_size1}",
                        'Point_Order': i + 1
                    })
            
            if can_plot_brand2_chart2:
                for i, (x_name, y_name) in enumerate(coord_col_pairs_6_10):
                    chart_data_2.append({
                        'X_coord_actual': filtered_df2[x_name].values[0],
                        'Y_coord_actual': filtered_df2[y_name].values[0],
                        'Display_Label': f"Right: {selected_year2}-{selected_quarter2}-{selected_brand2}-{selected_unit2}-{selected_size2}",
                        'Point_Order': i + 1
                    })
            
            if chart_data_2:
                st.subheader("Internal Cross Section area (Supply Fan)") # New title for Chart 2
                chart_df_2 = pd.DataFrame(chart_data_2)
                chart_df_2 = chart_df_2.sort_values(by=['Display_Label', 'Point_Order'])
                
                fig2 = px.line(chart_df_2,
                               x="X_coord_actual", # Use actual values for X axis
                               y="Y_coord_actual", # Use actual values for Y axis
                               color="Display_Label",
                               line_group="Display_Label",
                               markers=True,
                               title=None, # Title is now set via subheader
                               hover_data={'X_coord_actual': True, 'Y_coord_actual': True}) # Still show actual in hover
                
                fig2.update_layout(
                    xaxis_title="Unit internal width_Supply Fan (mm)", # Corrected X-axis title
                    yaxis_title="Unit internal height_Supply Fan (mm)", # Corrected Y-axis title
                    hovermode="x unified",
                    legend_title_text="Selection - Year-Quarter-Brand-Unit-Size",
                    xaxis_constrain="domain",
                    yaxis_constrain="domain",
                    showlegend=True
                )
                fig2.update_yaxes(scaleanchor="x", scaleratio=1)
                st.plotly_chart(fig2, use_container_width=True)
            elif not can_plot_brand1_chart2 and not can_plot_brand2_chart2:
                st.warning("No complete coordinate data (X6-X10, Y6-Y10) found for selected units to generate Chart 2. Please ensure data is present and valid for both selections.")
            st.markdown("---") # Separator after chart 2
            chart2_displayed = True


else:
    st.warning("One of the selected combinations has no data to display for comparison. Please adjust your selections.")
