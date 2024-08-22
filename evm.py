import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO

def save_as_jpg(content, file_name, title, subtitle):
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.axis('off')

    # Title
    ax.text(0.5, 0.95, title, ha='center', va='top', fontsize=36, fontweight='bold', color='black', bbox=dict(facecolor='pink', edgecolor='black', boxstyle='round,pad=0.5'))

    # Subtitle
    ax.text(0.5, 0.85, subtitle, ha='center', va='top', fontsize=22, fontweight='bold', color='black', bbox=dict(facecolor='yellow', edgecolor='black', boxstyle='round,pad=0.5'))

    # Content
    ax.text(0.05, 0.6, content, ha='left', va='top', fontsize=16, color='black', bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='jpg', bbox_inches='tight', pad_inches=0.1)
    img_buffer.seek(0)
    plt.close(fig)  # Close the figure to free up memory

    return img_buffer

def generate_graph():
    # Time points for S-Curves
    time_points = np.linspace(0, 1, 100)

    # Calculate cumulative values starting from the origin
    def s_curve(max_value):
        return max_value * (time_points ** 2)

    ev_curve = s_curve(ev)
    pv_curve = s_curve(pv)
    ac_curve = s_curve(ac)

    # Combined EV, PV, and AC S-Curves on one graph
    fig, ax = plt.subplots(figsize=(14, 10))  # Increased figure size
    ax.plot(time_points, pv_curve, label='Planned Value (PV) S-Curve', color='blue')
    ax.plot(time_points, ev_curve, label='Earned Value (EV) S-Curve', color='green')
    ax.plot(time_points, ac_curve, label='Actual Cost (AC) S-Curve', color='red')

    # Shaded area where Earned Value (EV) is below Planned Value (PV)
    ax.fill_between(time_points, ev_curve, pv_curve, where=(ev_curve < pv_curve), color='lightgreen', alpha=0.5, label='Under-Completion Area (EV < PV)')

    # Shaded area where Actual Cost (AC) is below Planned Value (PV)
    ax.fill_between(time_points, ac_curve, pv_curve, where=(ac_curve < pv_curve), color='lightcoral', alpha=0.5, label='Cost Overrun Area (AC < PV)')

    # Draw lines for ETC and VAC
    time_period = 0.5  # Specify the time period for lines
    etc_line = np.full_like(time_points, etc)
    vac_line = np.full_like(time_points, vac)

    ax.axvline(x=time_period, color='orange', linestyle='--', label='ETC Line')
    ax.axhline(y=etc, color='orange', linestyle='--', label='ETC Value')
    ax.axhline(y=vac, color='purple', linestyle='--', label='VAC Value')

    # Add CV and SV as horizontal lines
    ax.axhline(y=cv, color='brown', linestyle='--', label='Cost Variance (CV)')
    ax.axhline(y=sv, color='pink', linestyle='--', label='Schedule Variance (SV)')
    ax.axhline(y=bac, color='black', linestyle='--', label='Budget at Completion (BAC)')

    ax.set_title('Planned Value (PV), Earned Value (EV), and Actual Cost (AC) S-Curves with Variance Areas', fontsize=16, fontweight='bold')
    ax.set_xlabel('Time', fontsize=14, fontweight='bold')
    ax.set_ylabel('Value', fontsize=14, fontweight='bold')
    
    # Move legend below the graph
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3)

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='jpg')
    img_buffer.seek(0)
    plt.close(fig)  # Close the figure to free up memory

    return img_buffer

# Sidebar with EVM, Application Information, and Graph Legends
st.sidebar.title("EVM Calculator")
st.sidebar.markdown("""
### About Earned Value Management (EVM)
Earned Value Management (EVM) is a project management technique that integrates scope, cost, and schedule metrics to assess project performance and progress. It provides key insights into project health, including:

- **Planned Value (PV):** The value of the work that was planned to be completed by a specific time.
- **Earned Value (EV):** The value of the work actually completed by a specific time.
- **Actual Cost (AC):** The actual cost incurred for the work performed by a specific time.

### About This Application
This EVM Calculator allows you to input project parameters and generate key EVM metrics such as CPI, SPI, CV, and SV. The application also provides visual representations through S-Curves and variance areas.

### Graph Legends and Colors
- **Planned Value (PV) S-Curve:** Blue
- **Earned Value (EV) S-Curve:** Green
- **Actual Cost (AC) S-Curve:** Red
- **Under-Completion Area (EV < PV):** Light Green (Shaded Area)
- **Cost Overrun Area (AC < PV):** Light Coral (Shaded Area)
- **ETC Line:** Orange (Dashed Line)
- **ETC Value:** Orange (Dashed Horizontal Line)
- **VAC Value:** Purple (Dashed Horizontal Line)
- **Cost Variance (CV):** Brown (Dashed Horizontal Line)
- **Schedule Variance (SV):** Pink (Dashed Horizontal Line)
- **Budget at Completion (BAC):** Black (Dashed Horizontal Line)
""")

# Title
st.markdown("<h1 style='font-size: 36px; font-weight: bold; color: black; background-color: pink; padding: 10px; text-align: left;'>EVM CALCULATOR</h1>", unsafe_allow_html=True)

# Input Section
st.markdown("<h3 style='background-color: yellow; color: black; font-weight: bold; padding: 10px; font-size: 22px; text-align: left;'>Input</h3>", unsafe_allow_html=True)
with st.expander("Expand to enter inputs", expanded=True):
    bac = st.number_input("Budget at Completion (BAC)", min_value=0.0, value=1000000.0, help="Total budget allocated for the project.")
    pv = st.number_input("Planned Value (PV)", min_value=0.0, value=500000.0, help="The value of the work that was planned to be completed by a specific time.")
    ev = st.number_input("Earned Value (EV)", min_value=0.0, value=300000.0, help="The value of the work actually completed by a specific time.")
    ac = st.number_input("Actual Cost (AC)", min_value=0.0, value=250000.0, help="The actual cost incurred for the work performed by a specific time.")
    performance_percentage = st.number_input("Performance Percentage (%)", min_value=0.0, max_value=100.0, value=30.0, help="Percentage of work completed to calculate Earned Value (EV).")
    total_project_value = st.number_input("Total Project Value ($)", min_value=0.0, value=1000000.0, help="Total value of the project to calculate Budget at Completion (BAC).")

# Calculations
ev = (performance_percentage / 100) * total_project_value if total_project_value != 0 else 0
bac = total_project_value
cpi = ev / ac if ac != 0 else 0
spi = ev / pv if pv != 0 else 0
cv = ev - ac
sv = ev - pv
eac_cpi = bac / cpi if cpi != 0 else 0
eac_cpi_spi = ac + ((bac - ev) / (cpi * spi)) if cpi * spi != 0 else 0
etc = eac_cpi - ac if cpi != 0 else 0
vac = bac - ev

# Layout for Results and Graph
col1, col2 = st.columns([2, 1])  # Adjust column widths as needed

with col1:
    st.markdown("<h3 style='background-color: yellow; color: black; font-weight: bold; padding: 10px; font-size: 22px; text-align: left;'>Results</h3>", unsafe_allow_html=True)
    with st.expander("Expand to view results", expanded=True):
        st.write(f"### Results")
        
        results_content = (
            f"**Budget at Completion (BAC):** {bac:.2f}\n"
            f"**Earned Value (EV):** {ev:.2f}\n"
            f"**Planned Value (PV):** {pv:.2f}\n"
            f"**Actual Cost (AC):** {ac:.2f}\n"
            f"**Cost Performance Index (CPI):** {cpi:.2f}\n"
            f"**Schedule Performance Index (SPI):** {spi:.2f}\n"
            f"**Cost Variance (CV):** {cv:.2f}\n"
            f"**Schedule Variance (SV):** {sv:.2f}\n"
            f"**Estimate at Completion (EAC) based on CPI:** {eac_cpi:.2f}\n"
            f"**Estimate at Completion (EAC) based on CPI and SPI:** {eac_cpi_spi:.2f}\n"
            f"**Estimate to Complete (ETC):** {etc:.2f}\n"
            f"**Variance at Completion (VAC):** {vac:.2f}\n"
        )
        st.text(results_content)
        st.download_button(
            label="Download Results as JPG",
            data=save_as_jpg(results_content, 'results.jpg', 'EVM CALCULATOR RESULTS', 'Detailed Results'),
            file_name="evm_results.jpg",
            mime="image/jpeg"
        )
        
with col2:
    st.markdown("<h3 style='background-color: yellow; color: black; font-weight: bold; padding: 10px; font-size: 22px; text-align: left;'>Graph</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='color: black;'>Generated S-Curves with Variance Areas</h4>", unsafe_allow_html=True)
    graph_img = generate_graph()
    st.image(graph_img, caption='S-Curves for PV, EV, and AC with Variance Areas')
    st.download_button(
        label="Download Graph as JPG",
        data=graph_img,
        file_name="evm_graph.jpg",
        mime="image/jpeg"
    )
