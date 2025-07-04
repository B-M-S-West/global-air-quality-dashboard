"""Chart generation utilities for air quality data visualization."""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict
import streamlit as st
from utils.config import POLLUTANT_INFO, AQI_THRESHOLDS


class AirQualityCharts:
    """Class for generating air quality charts and visualizations."""

    @staticmethod
    def create_time_series_chart(
        data: List[Dict], parameter: str, location_name: str = "Location"
    ) -> go.Figure:
        """Create time series chart for a single pollutant."""
        if not data:
            return go.Figure().add_annotation(
                text="No data available",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )

        df = pd.DataFrame(data)
        if "datetime" in df.columns:
            df["datetime"] = pd.to_datetime(df["datetime"])

        pollutant_info = POLLUTANT_INFO.get(parameter, {})
        color = pollutant_info.get("color", "#1f77b4")
        display_name = pollutant_info.get("display_name", parameter.upper())
        units = pollutant_info.get("units", "")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=df["datetime"],
                y=df["value"],
                mode="lines+markers",
                name=f"{display_name} ({units})",
                line=dict(color=color, width=2),
                marker=dict(size=4),
                hovertemplate=f"<b>{display_name}</b><br>"
                + "Time: %{x}<br>"
                + f"Value: %{y} {units}<br>"
                + "<extra></extra>",
            )
        )

        fig.update_layout(
            title=f"{display_name} Levels at {location_name}",
            xaxis_title="Time",
            yaxis_title=f"{display_name} ({units})",
            hovermode="x unified",
            showlegend=True,
            height=400,
        )

        return fig

    @staticmethod
    def create_multi_pollutant_chart(
        data_dict: Dict[str, List[Dict]], location_name: str = "Location"
    ) -> go.Figure:
        """Create chart comparing multiple pollutants."""
        fig = make_subplots(
            rows=len(data_dict),
            cols=1,
            subplot_titles=[
                POLLUTANT_INFO.get(param, {}).get("display_name", param.upper())
                for param in data_dict.keys()
            ],
            vertical_spacing=0.08,
        )

        for i, (parameter, data) in enumerate(data_dict.items(), 1):
            if not data:
                continue

            df = pd.DataFrame(data)
            if "datetime" in df.columns:
                df["datetime"] = pd.to_datetime(df["datetime"])

            pollutant_info = POLLUTANT_INFO.get(parameter, {})
            color = pollutant_info.get("color", "#1f77b4")
            display_name = pollutant_info.get("display_name", parameter.upper())
            units = pollutant_info.get("units", "")

            fig.add_trace(
                go.Scatter(
                    x=df["datetime"],
                    y=df["value"],
                    mode="lines",
                    name=f"{display_name} ({units})",
                    line=dict(color=color, width=2),
                    hovertemplate=f"<b>{display_name}</b><br>"
                    + "Time: %{x}<br>"
                    + f"Value: %{y} {units}<br>"
                    + "<extra></extra>",
                ),
                row=i,
                col=1,
            )

            fig.update_yaxis(title_text=f"{display_name} ({units})", row=i, col=1)

        fig.update_layout(
            title=f"Multi-Pollutant Analysis at {location_name}",
            height=300 * len(data_dict),
            showlegend=False,
            hovermode="x unified",
        )

        return fig

    @staticmethod
    def create_comparison_chart(
        locations_data: Dict[str, Dict[str, List[Dict]]], parameter: str
    ) -> go.Figure:
        """Create chart comparing same pollutant across multiple locations."""
        fig = go.Figure()

        pollutant_info = POLLUTANT_INFO.get(parameter, {})
        display_name = pollutant_info.get("display_name", parameter.upper())
        units = pollutant_info.get("units", "")

        colors = px.colors.qualitative.Set1

        for i, (location_name, location_data) in enumerate(locations_data.items()):
            data = location_data.get(parameter, [])
            if not data:
                continue

            df = pd.DataFrame(data)
            if "datetime" in df.columns:
                df["datetime"] = pd.to_datetime(df["datetime"])

            color = colors[i % len(colors)]

            fig.add_trace(
                go.Scatter(
                    x=df["datetime"],
                    y=df["value"],
                    mode="lines",
                    name=location_name,
                    line=dict(color=color, width=2),
                    hovertemplate=f"<b>{location_name}</b><br>"
                    + "Time: %{x}<br>"
                    + f"Value: %{y} {units}<br>"
                    + "<extra></extra>",
                )
            )

        fig.update_layout(
            title=f"{display_name} Comparison Across Locations",
            xaxis_title="Time",
            yaxis_title=f"{display_name} ({units})",
            hovermode="x unified",
            height=500,
        )

        return fig

    @staticmethod
    def create_current_conditions_chart(latest_data: List[Dict]) -> go.Figure:
        """Create bar chart of current conditions for all pollutants."""
        if not latest_data:
            return go.Figure().add_annotation(
                text="No current data available",
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.5,
                showarrow=False,
            )

        # Group by parameter
        param_data = {}
        for measurement in latest_data:
            param = measurement.get("parameter")
            if param:
                if param not in param_data:
                    param_data[param] = []
                param_data[param].append(measurement["value"])

        # Calculate averages
        parameters = []
        values = []
        colors = []
        units_list = []

        for param, vals in param_data.items():
            avg_val = sum(vals) / len(vals)
            pollutant_info = POLLUTANT_INFO.get(param, {})

            parameters.append(pollutant_info.get("display_name", param.upper()))
            values.append(avg_val)
            colors.append(pollutant_info.get("color", "#1f77b4"))
            units_list.append(pollutant_info.get("units", ""))

        fig = go.Figure(
            data=[
                go.Bar(
                    x=parameters,
                    y=values,
                    marker_color=colors,
                    hovertemplate="<b>%{x}</b><br>"
                    + "Average: %{y}<br>"
                    + "<extra></extra>",
                )
            ]
        )

        fig.update_layout(
            title="Current Air Quality Conditions",
            xaxis_title="Pollutants",
            yaxis_title="Concentration",
            height=400,
            showlegend=False,
        )

        return fig

    @staticmethod
    def create_aqi_gauge(value: float, parameter: str = "pm25") -> go.Figure:
        """Create AQI gauge chart."""
        thresholds = AQI_THRESHOLDS.get(parameter, AQI_THRESHOLDS["pm25"])

        # Determine AQI category
        aqi_category = "Good"
        aqi_color = "#00E400"

        for min_val, max_val, category, color in thresholds:
            if min_val <= value <= max_val:
                aqi_category = category
                aqi_color = color
                break

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=value,
                domain={"x": [0, 1], "y": [0, 1]},
                title={
                    "text": f"{POLLUTANT_INFO.get(parameter, {}).get('display_name', parameter.upper())} AQI"
                },
                delta={"reference": 35.4},  # Moderate threshold for PM2.5
                gauge={
                    "axis": {"range": [None, 300]},
                    "bar": {"color": aqi_color},
                    "steps": [
                        {"range": [0, 12], "color": "#E8F5E8"},
                        {"range": [12, 35.4], "color": "#FFFACD"},
                        {"range": [35.4, 55.4], "color": "#FFE4B5"},
                        {"range": [55.4, 150.4], "color": "#FFB6C1"},
                        {"range": [150.4, 250.4], "color": "#DDA0DD"},
                        {"range": [250.4, 300], "color": "#F0E68C"},
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": 150.4,
                    },
                },
            )
        )

        fig.update_layout(
            height=300,
            annotations=[
                dict(
                    text=aqi_category,
                    x=0.5,
                    y=0.2,
                    showarrow=False,
                    font=dict(size=16, color=aqi_color),
                )
            ],
        )

        return fig
