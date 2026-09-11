import math
import streamlit as st

st.set_page_config(
    page_title="Solar Advisor",
    page_icon="☀️",
    layout="centered"
)

APP_NAME = "Solar Advisor"

if "page" not in st.session_state:
    st.session_state.page = 1


def go_to_page(page_number):
    st.session_state.page = page_number
    st.rerun()


def calculate_battery_hours(backup_duration):
    hours_map = {
        "No backup": 0,
        "2 hours": 2,
        "4 hours": 4,
        "6 hours": 6,
        "8 hours": 8,
        "Overnight": 10
    }

    return hours_map.get(backup_duration, 0)


def calculate_panel_count(system_kw, panel_watt):
    panel_kw = panel_watt / 1000

    if panel_kw <= 0:
        return 0

    return math.ceil(system_kw / panel_kw)


def round_system_size(size):
    if size <= 0:
        return 0

    return round(size * 2) / 2


def calculate_battery_size(backup_load_kw, backup_hours):
    if backup_load_kw <= 0 or backup_hours <= 0:
        return 0

    required_energy = backup_load_kw * backup_hours

    battery_size = required_energy / 0.85

    return math.ceil(battery_size * 2) / 2


def estimate_system_cost(
    system_kw,
    system_type,
    battery_kwh,
    budget_type
):

    if system_type == "On-grid":
        base_cost_per_kw = 55000

    elif system_type == "Hybrid":
        base_cost_per_kw = 70000

    elif system_type == "Off-grid":
        base_cost_per_kw = 75000

    else:
        base_cost_per_kw = 65000

    solar_cost = system_kw * base_cost_per_kw

    battery_cost = battery_kwh * 12000

    installation_cost = system_kw * 5000

    total = (
        solar_cost
        + battery_cost
        + installation_cost
    )

    if budget_type == "Economical":
        total *= 0.95

    elif budget_type == "Premium":
        total *= 1.15

    return round(total, -3)


def estimate_annual_savings(
    annual_consumption,
    annual_generation,
    monthly_bill
):

    if monthly_bill > 0:
        annual_bill = monthly_bill * 12
    else:
        # Preliminary assumed electricity value
        annual_bill = annual_consumption * 8

    generation_used = min(
        annual_generation,
        annual_consumption
    )

    electricity_value = (
        generation_used * 8
    )

    savings = min(
        electricity_value,
        annual_bill
    )

    return round(savings)


def system_recommendation(
    monthly_units,
    objective,
    system_preference,
    backup_duration,
    roof_area
):

    annual_consumption = monthly_units * 12

    solar_yield = 1300

    if "Reduce electricity bill" in objective:
        target_percentage = 0.75

    elif "Maximum solar generation" in objective:
        target_percentage = 1.00

    elif "Reduce dependence" in objective:
        target_percentage = 0.90

    else:
        target_percentage = 0.80

    target_generation = (
        annual_consumption
        * target_percentage
    )

    calculated_capacity = (
        target_generation
        / solar_yield
    )


    roof_capacity = roof_area / 100

    if roof_capacity > 0:

        recommended_capacity = min(
            calculated_capacity,
            roof_capacity
        )

    else:

        recommended_capacity = calculated_capacity

    if recommended_capacity < 1:
        recommended_capacity = 1

    recommended_capacity = round_system_size(
        recommended_capacity
    )

    annual_generation = (
        recommended_capacity
        * solar_yield
    )

    if annual_consumption > 0:

        coverage = (
            annual_generation
            / annual_consumption
        ) * 100

    else:

        coverage = 0

    # Determine system type.

    if system_preference == "Let Solar Advisor recommend":

        if backup_duration == "No backup":
            system_type = "On-grid"
        else:
            system_type = "Hybrid"

    else:

        system_type = system_preference

    return (
        recommended_capacity,
        annual_generation,
        coverage,
        system_type,
        solar_yield
    )



with st.sidebar:

    st.header("📞 Contact Us")

    st.write(
        "Need help with your solar assessment?"
    )

    st.markdown(
        """
        ### 📧 Email

        thakreswarnim1@gmail.com

        ### 💼 LinkedIn

        www.linkedin.com/in/swarnim-thakre-690440335

        ### 💻 GitHub

        https://github.com/swarnimT
        """
    )

    st.divider()

    st.caption(
        "Solar Advisor"
    )

    st.caption(
        "Preliminary solar planning tool"
    )


if st.session_state.page == 1:

    st.title("☀️ Solar Advisor")

    st.subheader(
        "Professional Solar Assessment"
    )

    st.write(
        "Get a preliminary solar system recommendation "
        "based on your location, electricity usage, "
        "property and budget."
    )

    st.progress(14)

    st.subheader("📍 Location")

    st.write(
        "Tell us where the solar system will be installed."
    )

    pin_code = st.text_input(
        "PIN Code",
        placeholder="Enter your 6-digit PIN code"
    )

    city = st.text_input(
        "City",
        placeholder="Enter your city"
    )

    state = st.text_input(
        "State",
        placeholder="Enter your state"
    )

    if st.button(
        "Continue →",
        use_container_width=True
    ):

        if not pin_code or not city or not state:

            st.warning(
                "Please fill in all location details."
            )

        elif (
            len(pin_code) != 6
            or not pin_code.isdigit()
        ):

            st.warning(
                "Please enter a valid 6-digit PIN code."
            )

        else:

            st.session_state.pin_code = pin_code
            st.session_state.city = city
            st.session_state.state = state

            go_to_page(2)


elif st.session_state.page == 2:

    st.title("⚡ Electricity Consumption")

    st.write(
        "Your electricity usage is one of the most important "
        "inputs for determining solar capacity."
    )

    st.progress(28)

    method = st.radio(
        "How would you like to provide your electricity information?",
        [
            "Enter monthly electricity consumption",
            "Estimate from appliances"
        ]
    )

    if method == "Enter monthly electricity consumption":

        st.subheader("📊 Monthly Electricity Usage")

        monthly_units = st.number_input(
            "Average monthly consumption (kWh / units)",
            min_value=1.0,
            max_value=100000.0,
            value=300.0,
            step=10.0
        )

        monthly_bill = st.number_input(
            "Average monthly electricity bill (₹)",
            min_value=0.0,
            max_value=1000000.0,
            value=2000.0,
            step=100.0
        )

        st.info(
            "You can find your monthly consumption in "
            "your electricity bill. It is usually shown "
            "in kWh or units."
        )

        if st.button(
            "Continue →",
            use_container_width=True
        ):

            if monthly_units <= 0:

                st.warning(
                    "Please enter a valid electricity consumption."
                )

            else:

                st.session_state.monthly_units = (
                    monthly_units
                )

                st.session_state.monthly_bill = (
                    monthly_bill
                )

                st.session_state.consumption_method = (
                    "Monthly consumption"
                )

                go_to_page(3)


    else:

        st.subheader("🔌 Appliance Estimation")

        st.write(
            "We can estimate electricity consumption "
            "from the appliances you use."
        )

        st.markdown("### 🌀 Fans")

        fan_qty = st.number_input(
            "Number of fans",
            min_value=0,
            max_value=50,
            value=2
        )

        fan_hours = st.number_input(
            "Fan usage per day (hours)",
            min_value=0.0,
            max_value=24.0,
            value=8.0
        )

        st.markdown("### 💡 Lights")

        light_qty = st.number_input(
            "Number of LED lights",
            min_value=0,
            max_value=100,
            value=4
        )

        light_hours = st.number_input(
            "Light usage per day (hours)",
            min_value=0.0,
            max_value=24.0,
            value=6.0
        )

        st.markdown("### 📺 Television")

        tv_qty = st.number_input(
            "Number of TVs",
            min_value=0,
            max_value=20,
            value=1
        )

        tv_hours = st.number_input(
            "TV usage per day (hours)",
            min_value=0.0,
            max_value=24.0,
            value=4.0
        )

        st.markdown("### ❄️ Refrigerator")

        refrigerator_qty = st.number_input(
            "Number of refrigerators",
            min_value=0,
            max_value=10,
            value=1
        )

        refrigerator_hours = st.number_input(
            "Estimated refrigerator operating hours/day",
            min_value=0.0,
            max_value=24.0,
            value=10.0
        )

        if st.button(
            "Calculate Consumption →",
            use_container_width=True
        ):

            fan_energy = (
                fan_qty
                * 75
                * fan_hours
                / 1000
            )

            light_energy = (
                light_qty
                * 10
                * light_hours
                / 1000
            )

            tv_energy = (
                tv_qty
                * 120
                * tv_hours
                / 1000
            )

            refrigerator_energy = (
                refrigerator_qty
                * 150
                * refrigerator_hours
                / 1000
            )

            daily_consumption = (
                fan_energy
                + light_energy
                + tv_energy
                + refrigerator_energy
            )

            monthly_consumption = (
                daily_consumption
                * 30
            )

            st.session_state.monthly_units = (
                monthly_consumption
            )

            st.session_state.monthly_bill = 0

            st.session_state.consumption_method = (
                "Appliance estimate"
            )

            go_to_page(3)


elif st.session_state.page == 3:

    st.title("🎯 Solar Requirements")

    st.write(
        "Tell us what you expect from your solar system."
    )

    st.progress(42)

    st.subheader("🎯 Primary Objective")

    objective = st.radio(
        "What is your main goal?",
        [
            "💰 Reduce electricity bill",
            "🔋 Backup during power cuts",
            "☀️ Maximum solar generation",
            "🏠 Reduce dependence on the grid"
        ]
    )

    st.subheader("⚡ Preferred System")

    system_preference = st.selectbox(
        "How should the system be configured?",
        [
            "Let Solar Advisor recommend",
            "On-grid",
            "Hybrid",
            "Off-grid"
        ]
    )

    st.subheader("⚡ Power Cuts")

    power_cuts = st.selectbox(
        "How often do you experience power cuts?",
        [
            "Rare",
            "Occasional",
            "Frequent",
            "No grid connection"
        ]
    )

    st.subheader("🔋 Backup Requirement")

    backup_duration = st.selectbox(
        "How much backup do you need?",
        [
            "No backup",
            "2 hours",
            "4 hours",
            "6 hours",
            "8 hours",
            "Overnight"
        ]
    )

    backup_appliances = []

    if backup_duration != "No backup":

        st.subheader(
            "🔋 Essential Backup Appliances"
        )

        st.write(
            "Select only the appliances that must "
            "remain powered during a power cut."
        )

        if st.checkbox("🌀 Fans"):
            backup_appliances.append("Fans")

        if st.checkbox("💡 Lights"):
            backup_appliances.append("Lights")

        if st.checkbox("❄️ Refrigerator"):
            backup_appliances.append("Refrigerator")

        if st.checkbox("📺 Television"):
            backup_appliances.append("Television")

        if st.checkbox("📶 Wi-Fi Router"):
            backup_appliances.append("Wi-Fi Router")

        if st.checkbox("❄️ Air Conditioner"):
            backup_appliances.append("Air Conditioner")

        if st.checkbox("➕ Other appliances"):
            backup_appliances.append("Other")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Back",
            use_container_width=True
        ):

            go_to_page(2)

    with col2:

        if st.button(
            "Continue →",
            use_container_width=True
        ):

            st.session_state.objective = objective

            st.session_state.system_preference = (
                system_preference
            )

            st.session_state.power_cuts = (
                power_cuts
            )

            st.session_state.backup_duration = (
                backup_duration
            )

            st.session_state.backup_appliances = (
                backup_appliances
            )

            go_to_page(4)


elif st.session_state.page == 4:

    st.title("🏠 Roof & Property")

    st.write(
        "The available installation area helps determine "
        "how much solar capacity can physically fit."
    )

    st.progress(57)

    st.subheader("🏢 Property Information")

    property_type = st.selectbox(
        "Property type",
        [
            "Residential",
            "Commercial",
            "Industrial"
        ]
    )

    installation_type = st.selectbox(
        "Installation type",
        [
            "Rooftop",
            "Ground-mounted"
        ]
    )

    st.subheader("📐 Available Installation Area")

    roof_area = st.number_input(
        "Available area (sq. ft.)",
        min_value=1.0,
        max_value=1000000.0,
        value=500.0,
        step=50.0
    )

    st.subheader("🏠 Roof Type")

    roof_type = st.selectbox(
        "Roof type",
        [
            "Flat concrete roof",
            "Sloped roof",
            "Metal roof",
            "Tile roof",
            "Other"
        ]
    )

    st.subheader("☀️ Shading")

    shading = st.select_slider(
        "How much shade does the installation area receive?",
        options=[
            "Very Low",
            "Low",
            "Moderate",
            "High",
            "Very High"
        ],
        value="Low"
    )

    st.caption(
        "Consider trees, buildings, tanks, chimneys "
        "and other objects that may shade the panels."
    )

    st.subheader("🧭 Roof Orientation")

    roof_orientation = st.selectbox(
        "Roof orientation",
        [
            "South",
            "South-East",
            "South-West",
            "East",
            "West",
            "North",
            "Multiple directions",
            "Not sure"
        ]
    )

    ownership = st.selectbox(
        "Property ownership",
        [
            "Owned",
            "Rented / Leased"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Back",
            use_container_width=True
        ):

            go_to_page(3)

    with col2:

        if st.button(
            "Continue →",
            use_container_width=True
        ):

            if roof_area <= 0:

                st.warning(
                    "Please enter the available area."
                )

            else:

                st.session_state.property_type = (
                    property_type
                )

                st.session_state.installation_type = (
                    installation_type
                )

                st.session_state.roof_area = (
                    roof_area
                )

                st.session_state.roof_type = (
                    roof_type
                )

                st.session_state.shading = (
                    shading
                )

                st.session_state.roof_orientation = (
                    roof_orientation
                )

                st.session_state.ownership = (
                    ownership
                )

                go_to_page(5)


elif st.session_state.page == 5:

    st.title("💰 Budget & Investment")

    st.write(
        "Your budget preference helps us choose a "
        "practical system configuration."
    )

    st.progress(71)

    budget_type = st.radio(
        "Budget preference",
        [
            "Economical",
            "Balanced",
            "Premium",
            "Custom Budget"
        ]
    )

    custom_budget = 0

    if budget_type == "Custom Budget":

        custom_budget = st.number_input(
            "Maximum budget (₹)",
            min_value=10000.0,
            max_value=100000000.0,
            value=200000.0,
            step=10000.0
        )

    st.subheader("💡 Investment Priority")

    investment_priority = st.selectbox(
        "What matters most?",
        [
            "Lowest initial cost",
            "Best balance of cost and performance",
            "Maximum long-term savings",
            "Premium equipment and reliability"
        ]
    )

    st.subheader("☀️ Panel Preference")

    panel_watt = st.selectbox(
        "Preferred panel size",
        [
            400,
            450,
            500,
            550,
            600
        ]
    )

    st.info(
        "Panel prices, inverter prices and installation "
        "costs vary by manufacturer, location and market "
        "conditions. The financial figures in this tool "
        "are preliminary estimates."
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "← Back",
            use_container_width=True
        ):

            go_to_page(4)

    with col2:

        if st.button(
            "Generate Recommendation →",
            use_container_width=True
        ):

            st.session_state.budget_type = (
                budget_type
            )

            st.session_state.custom_budget = (
                custom_budget
            )

            st.session_state.investment_priority = (
                investment_priority
            )

            st.session_state.panel_watt = (
                panel_watt
            )

            go_to_page(6)


elif st.session_state.page == 6:

    st.title("☀️ Your Solar Recommendation")

    st.success(
        "Assessment completed successfully."
    )

    st.progress(100)

    
    monthly_units = (
        st.session_state.monthly_units
    )

    monthly_bill = (
        st.session_state.monthly_bill
    )

    objective = (
        st.session_state.objective
    )

    system_preference = (
        st.session_state.system_preference
    )

    backup_duration = (
        st.session_state.backup_duration
    )

    roof_area = (
        st.session_state.roof_area
    )

    budget_type = (
        st.session_state.budget_type
    )

    panel_watt = (
        st.session_state.panel_watt
    )

    
    (
        recommended_capacity,
        annual_generation,
        coverage_percentage,
        system_type,
        solar_yield
    ) = system_recommendation(
        monthly_units,
        objective,
        system_preference,
        backup_duration,
        roof_area
    )

    annual_consumption = (
        monthly_units * 12
    )

    panel_count = calculate_panel_count(
        recommended_capacity,
        panel_watt
    )

    actual_panel_capacity = (
        panel_count
        * panel_watt
        / 1000
    )

    backup_hours = calculate_battery_hours(
        backup_duration
    )

    backup_appliances = (
        st.session_state.backup_appliances
    )

    appliance_loads = {
        "Fans": 0.15,
        "Lights": 0.04,
        "Refrigerator": 0.15,
        "Television": 0.12,
        "Wi-Fi Router": 0.02,
        "Air Conditioner": 1.50,
        "Other": 0.30
    }

    backup_load_kw = 0

    for appliance in backup_appliances:

        backup_load_kw += appliance_loads.get(
            appliance,
            0
        )

    battery_kwh = calculate_battery_size(
        backup_load_kw,
        backup_hours
    )


    if system_type == "On-grid":

        inverter_kw = recommended_capacity

    elif system_type == "Hybrid":

        inverter_kw = max(
            recommended_capacity,
            backup_load_kw
        )

    else:

        inverter_kw = max(
            recommended_capacity,
            backup_load_kw
        )

    inverter_kw = round_system_size(
        inverter_kw
    )


    estimated_cost = estimate_system_cost(
        recommended_capacity,
        system_type,
        battery_kwh,
        budget_type
    )


    budget_warning = False

    if budget_type == "Custom Budget":

        custom_budget = (
            st.session_state.custom_budget
        )

        if estimated_cost > custom_budget:

            budget_warning = True


    annual_savings = estimate_annual_savings(
        annual_consumption,
        annual_generation,
        monthly_bill
    )

    if annual_savings > 0:

        payback_years = (
            estimated_cost
            / annual_savings
        )

    else:

        payback_years = 0


    st.subheader(
        "Recommended System"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Solar Capacity",
            f"{recommended_capacity:.1f} kW"
        )

    with col2:

        st.metric(
            "System Type",
            system_type
        )

    col3, col4 = st.columns(2)

    with col3:

        st.metric(
            "Annual Generation",
            f"{annual_generation:,.0f} kWh"
        )

    with col4:

        st.metric(
            "Consumption Coverage",
            f"{coverage_percentage:.0f}%"
        )

    
    st.divider()

    st.subheader("☀️ Solar Panels")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Panel Size",
            f"{panel_watt} W"
        )

    with col2:

        st.metric(
            "Panel Count",
            f"{panel_count}"
        )

    st.write(
        f"Estimated installed panel capacity: "
        f"**{actual_panel_capacity:.1f} kW**"
    )

    st.subheader("⚡ Inverter")

    st.write(
        f"Preliminary inverter size: "
        f"**{inverter_kw:.1f} kW**"
    )

    st.caption(
        "Final inverter selection depends on the selected "
        "panel configuration, electrical design, maximum "
        "load and manufacturer specifications."
    )

    st.subheader("🔋 Battery")

    if backup_duration == "No backup":

        st.info(
            "No battery is recommended because you selected "
            "no backup requirement."
        )

    else:

        st.metric(
            "Estimated Battery Capacity",
            f"{battery_kwh:.1f} kWh"
        )

        st.write(
            f"Estimated essential backup load: "
            f"**{backup_load_kw:.2f} kW**"
        )

        st.write(
            f"Requested backup duration: "
            f"**{backup_duration}**"
        )

        if not backup_appliances:

            st.warning(
                "You selected a backup duration but did not "
                "select any essential backup appliances."
            )

    st.divider()

    st.subheader(
        "🏠 Installation Assessment"
    )

    approximate_required_area = (
        actual_panel_capacity * 100
    )

    st.write(
        f"Available area: "
        f"**{roof_area:,.0f} sq. ft.**"
    )

    st.write(
        f"Approximate panel area requirement: "
        f"**{approximate_required_area:,.0f} sq. ft.**"
    )

    if roof_area >= approximate_required_area:

        st.success(
            "The entered installation area appears "
            "sufficient for the preliminary system size."
        )

    else:

        st.warning(
            "The available area may be insufficient for "
            "the selected system. A detailed site survey "
            "is required."
        )

    
    shading = (
        st.session_state.shading
    )

    st.subheader(
        "☀️ Shading Assessment"
    )

    if shading in [
        "Very Low",
        "Low"
    ]:

        st.success(
            f"Reported shading: {shading}. "
            "The preliminary assessment assumes relatively "
            "low shading impact."
        )

    elif shading == "Moderate":

        st.warning(
            "Moderate shading may reduce actual generation. "
            "A site-specific shading analysis is recommended."
        )

    else:

        st.warning(
            "High shading may significantly affect solar "
            "generation. A professional site survey is strongly "
            "recommended before final system sizing."
        )

    orientation = (
        st.session_state.roof_orientation
    )

    st.subheader(
        "🧭 Orientation"
    )

    if orientation == "South":

        st.success(
            "South-facing orientation is generally favorable "
            "for solar generation in India."
        )

    elif orientation in [
        "South-East",
        "South-West"
    ]:

        st.info(
            "This orientation can work well, although the "
            "actual generation depends on tilt and shading."
        )

    elif orientation == "Not sure":

        st.info(
            "Orientation was not confirmed. A site survey "
            "should determine the optimal panel placement."
        )

    else:

        st.warning(
            "The selected orientation may affect annual "
            "generation. Detailed solar modelling is recommended."
        )


    st.divider()

    st.subheader(
        "💰 Financial Estimate"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Estimated System Cost",
            f"₹{estimated_cost:,.0f}"
        )

    with col2:

        st.metric(
            "Estimated Annual Savings",
            f"₹{annual_savings:,.0f}"
        )

    if payback_years > 0:

        st.metric(
            "Estimated Payback",
            f"{payback_years:.1f} years"
        )

    else:

        st.warning(
            "Payback could not be estimated."
        )

    if budget_warning:

        st.error(
            "The preliminary system estimate is above "
            "your selected custom budget."
        )


    st.subheader(
        "💡 Budget Assessment"
    )

    if budget_type == "Economical":

        st.write(
            "The recommendation prioritizes lower initial "
            "investment while maintaining a practical system."
        )

    elif budget_type == "Balanced":

        st.write(
            "The recommendation aims to balance system cost, "
            "generation and long-term value."
        )

    elif budget_type == "Premium":

        st.write(
            "The recommendation allows greater investment "
            "for equipment quality and long-term reliability."
        )

    else:

        st.write(
            f"Your maximum stated budget is "
            f"**₹{st.session_state.custom_budget:,.0f}**."
        )

    
    st.divider()

    st.subheader(
        "📋 Customer Assessment Summary"
    )

    st.write(
        f"**Location:** "
        f"{st.session_state.city}, "
        f"{st.session_state.state} "
        f"- {st.session_state.pin_code}"
    )

    st.write(
        f"**Property:** "
        f"{st.session_state.property_type}"
    )

    st.write(
        f"**Installation:** "
        f"{st.session_state.installation_type}"
    )

    st.write(
        f"**Monthly consumption:** "
        f"{monthly_units:,.0f} units"
    )

    st.write(
        f"**Annual consumption:** "
        f"{annual_consumption:,.0f} kWh"
    )

    st.write(
        f"**Primary objective:** "
        f"{objective}"
    )

    st.write(
        f"**Power cuts:** "
        f"{st.session_state.power_cuts}"
    )

    st.write(
        f"**Backup:** "
        f"{backup_duration}"
    )

    st.write(
        f"**Roof type:** "
        f"{st.session_state.roof_type}"
    )

    st.write(
        f"**Roof orientation:** "
        f"{orientation}"
    )

    st.write(
        f"**Shading:** "
        f"{shading}"
    )

    st.write(
        f"**Budget:** "
        f"{budget_type}"
    )


    st.divider()

    st.subheader(
        "⚠️ Important"
    )

    st.info(
        "This tool provides a preliminary planning estimate. "
        "It is not a substitute for a professional solar site "
        "survey or electrical engineering design. Final system "
        "capacity, panel layout, inverter selection, battery "
        "capacity, structural suitability, electricity savings, "
        "pricing, subsidies and financial returns should be "
        "verified using current local data, site conditions, "
        "utility rules and qualified professionals."
    )

    
    if st.button(
        "🔄 Start New Assessment",
        use_container_width=True
    ):

        st.session_state.clear()

        st.session_state.page = 1

        st.rerun()