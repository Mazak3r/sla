import streamlit as st

def calculate_sla_and_downtime(uptime_days=0, uptime_hours=0, uptime_minutes=0, month_days=30):
    """
    Calculate SLA percentage and breakdown downtime into days, hours, and minutes.
    """
    total_month_minutes = month_days * 24 * 60
    total_uptime_minutes = (uptime_days * 24 * 60) + (uptime_hours * 60) + uptime_minutes

    if user_uptime_mins > total_month_minutes:
        return None, None

    # Calculate SLA percentage
    sla_percentage = (total_uptime_minutes / total_month_minutes) * 100
    sla_percentage = round(sla_percentage, 4)

    # Calculate total downtime in minutes
    downtime_mins = total_month_minutes - total_uptime_minutes

    # Convert downtime minutes into Days, Hours, Minutes
    dt_days = downtime_mins // (24 * 60)
    remaining_mins = downtime_mins % (24 * 60)
    dt_hours = remaining_mins // 60
    dt_minutes = remaining_mins % 60

    downtime_str = f"{dt_days}d {dt_hours}h {dt_minutes}m"

    return sla_percentage, downtime_str, (dt_days, dt_hours, dt_minutes)


# Streamlit Page Config
st.set_page_config(page_title="SLA Calculator", page_icon="⏱️", layout="centered")

st.title("⏱️ SLA Uptime Calculator")
st.write("Enter your uptime details below and click **Calculate SLA**.")

st.divider()

# Input Form with an explicit Enter/Submit button
with st.form("sla_form"):
    st.subheader("1. Month Settings")
    month_days = st.number_input("Days in the month", min_value=1, max_value=31, value=30, step=1)

    st.subheader("2. Total Uptime")
    col1, col2, col3 = st.columns(3)

    with col1:
        uptime_days = st.number_input("Days", min_value=0, max_value=month_days, value=29, step=1)

    with col2:
        uptime_hours = st.number_input("Hours", min_value=0, max_value=23, value=15, step=1)

    with col3:
        uptime_minutes = st.number_input("Minutes", min_value=0, max_value=59, value=30, step=1)

    st.markdown("---")
    # Enter / Submit Button
    submitted = st.form_submit_button("🚀 Calculate SLA", use_container_width=True)

# Process calculation when the user clicks the Enter button
if submitted:
    total_month_mins = month_days * 24 * 60
    user_uptime_mins = (uptime_days * 24 * 60) + (uptime_hours * 60) + uptime_minutes

    if user_uptime_mins > total_month_mins:
        st.error("⚠️ Total uptime cannot exceed total time available in the month!")
    else:
        sla, downtime_str, (dt_d, dt_h, dt_m) = calculate_sla_and_downtime(
            uptime_days, uptime_hours, uptime_minutes, month_days
        )

        # Results Display
        st.subheader("📊 Calculation Results")
        metric_col1, metric_col2 = st.columns(2)

        with metric_col1:
            st.metric(label="SLA Percentage", value=f"{sla}%")

        with metric_col2:
            st.metric(label="Total Downtime", value=downtime_str)

        # Visual Status Indicator
        if sla >= 99.99:
            st.success(f"🎯 **Exceeds Four Nines (99.99%) availability.** Total Downtime: {downtime_str}")
        elif sla >= 99.9:
            st.info(f"👍 **Meets Three Nines (99.9%) availability.** Total Downtime: {downtime_str}")
        elif sla >= 99.0:
            st.warning(f"⚠️ **Meets Two Nines (99.0%) availability.** Total Downtime: {downtime_str}")
        else:
            st.error(f"🚨 **SLA below 99.0%.** Total Downtime: {downtime_str}")
