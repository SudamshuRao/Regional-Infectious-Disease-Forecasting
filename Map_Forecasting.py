import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_plotly_events import plotly_events

# ----------------------------
# Load results
# ----------------------------
df7 = pd.read_csv("7_day_forecast - Sheet1.csv")
df14 = pd.read_csv("14_day_forecast - Sheet1.csv")

# State abbreviation lookup
state_lookup = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA",
    "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH",
    "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
    "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN",
    "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"
}

df7["abbrev"] = df7["state"].map(state_lookup)
df14["abbrev"] = df14["state"].map(state_lookup)

st.title("Interactive Regional SNN Forecasting Map")

st.write("Click a state on the map to view **7-day and 14-day** forecasts and module contributions.")

# ----------------------------
# One Map Only
# ----------------------------
fig = px.choropleth(
    df7,
    locations="abbrev",
    locationmode="USA-states",
    color="RMSE_7",
    hover_name="state",
    color_continuous_scale="RdYlGn_r",
    scope="usa",
    title="Click a State to View Forecast Details"
)

# This renders the map *and* captures click events
clicked = plotly_events(fig, click_event=True, hover_event=False)

# ----------------------------
# Show results when a state is clicked
# ----------------------------
if clicked:
    # Get row index from pointIndex
    idx = clicked[0]["pointIndex"]
    abbrev = df7.iloc[idx]["abbrev"]

    # Convert abbrev to state name
    state_name = [s for s, a in state_lookup.items() if a == abbrev][0]

    st.subheader(f"Forecasting Results for {state_name}")

    r7 = df7[df7["state"] == state_name].iloc[0]
    r14 = df14[df14["state"] == state_name].iloc[0]

    # 7-day
    st.markdown("### 🟦 7-Day Forecast")
    st.write(f"**MAE:** {r7['MAE_7']:.3f}")
    st.write(f"**RMSE:** {r7['RMSE_7']:.3f}")
    st.write("**Module Contributions:**")
    st.json({
        "Temporal": r7["temporal"],
        "Mobility": r7["mobility"],
        "Vaccination": r7["vaccine"],
        "Environment": r7["environment"]
    })

    # 14-day
    st.markdown("### 🟧 14-Day Forecast")
    st.write(f"**MAE:** {r14['MAE_14']:.3f}")
    st.write(f"**RMSE:** {r14['RMSE_14']:.3f}")
    st.write("**Module Contributions:**")
    st.json({
        "Temporal": r14["temporal"],
        "Mobility": r14["mobility"],
        "Vaccination": r14["vaccine"],
        "Environment": r14["environment"]
    })
