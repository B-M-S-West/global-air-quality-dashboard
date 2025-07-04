
"""Main Streamlit application for OpenAQ Air Quality Dashboard."""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import time
from typing import List, Dict

# Import our modules
from ..api.client import get_openaq_client
from ..plots.charts import AirQualityCharts
from ..plots.maps import AirQualityMaps
from ..utils.config import Config, POLLUTANT_INFO

# Page configuration
st.set_page_config(
    page_title="OpenAQ Air Quality Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .pollutant-info {
        background-color: #e8f4fd;
        padding: 0.5rem;
        border-radius: 0.25rem;
        margin: 0.25rem 0;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

class AirQualityDashboard:
    """Main dashboard application class."""
    
    def __init__(self):
        self.client = get_openaq_client()
        self.charts = AirQualityCharts()
        self.maps = AirQualityMaps()
        
        # Initialize session state
        if 'selected_locations' not in st.session_state:
            st.session_state.selected_locations = []
        if 'last_refresh' not in st.session_state:
            st.session_state.last_refresh = datetime.now()
    
    def run(self):
        """Run the main dashboard application."""
        # Header
        st.markdown('<h1 class="main-header">🌍 OpenAQ Air Quality Dashboard</h1>', 
                   unsafe_allow_html=True)
        
        # Sidebar controls
        self.render_sidebar()
        
        # Main content tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🗺️ Global Overview", 
            "📊 Current Conditions", 
            "📈 Historical Trends", 
            "🔍 Location Comparison",
            "ℹ️ About"
        ])
        
        with tab1:
            self.render_global_overview()
        
        with tab2:
            self.render_current_conditions()
        
        with tab3:
            self.render_historical_trends()
        
        with tab4:
            self.render_location_comparison()
        
        with tab5:
            self.render_about()
    
    def render_sidebar(self):
        """Render sidebar controls."""
        st.sidebar.header("🎛️ Dashboard Controls")
        
        # Data refresh
        if st.sidebar.button("🔄 Refresh Data", type="primary"):
            st.cache_data.clear()
            st.session_state.last_refresh = datetime.now()
            st.rerun()
        
        st.sidebar.write(f"Last refresh: {st.session_state.last_refresh.strftime('%H:%M:%S')}")
        
        # Location filters
        st.sidebar.subheader("📍 Location Filters")
        
        # Get countries
        countries = self.client.get_countries()
        country_names = ['All Countries'] + [c.get('name', '') for c in countries if c.get('name')]
        selected_country = st.sidebar.selectbox("Select Country", country_names)
        
        # Get cities based on selected country
        cities = []
        if selected_country != 'All Countries':
            cities = self.client.get_cities(selected_country)
        
        city_names = ['All Cities'] + [c.get('name', '') for c in cities if c.get('name')]
        selected_city = st.sidebar.selectbox("Select City", city_names)
        
        # Pollutant selection
        st.sidebar.subheader("🧪 Pollutant Selection")
        available_pollutants = list(POLLUTANT_INFO.keys())
        selected_pollutants = st.sidebar.multiselect(
            "Select Pollutants",
            available_pollutants,
            default=['pm25', 'pm10', 'no2'],
            format_func=lambda x: POLLUTANT_INFO[x]['display_name']
        )
        
        # Time range for historical data
        st.sidebar.subheader("📅 Time Range")
        time_range = st.sidebar.selectbox(
            "Select Time Range",
            ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Custom Range"]
        )
        
        date_from = datetime.now() - timedelta(days=1)
        date_to = datetime.now()
        
        if time_range == "Last 7 Days":
            date_from = datetime.now() - timedelta(days=7)
        elif time_range == "Last 30 Days":
            date_from = datetime.now() - timedelta(days=30)
        elif time_range == "Custom Range":
            col1, col2 = st.sidebar.columns(2)
            with col1:
                date_from = st.date_input("From", value=date_from.date())
                date_from = datetime.combine(date_from, datetime.min.time())
            with col2:
                date_to = st.date_input("To", value=date_to.date())
                date_to = datetime.combine(date_to, datetime.min.time())
        
        # Store selections in session state
        st.session_state.selected_country = selected_country if selected_country != 'All Countries' else None
        st.session_state.selected_city = selected_city if selected_city != 'All Cities' else None
        st.session_state.selected_pollutants = selected_pollutants
        st.session_state.date_from = date_from
        st.session_state.date_to = date_to
        
        # Display current selections
        st.sidebar.subheader("📋 Current Selection")
        st.sidebar.write(f"**Country:** {selected_country}")
        st.sidebar.write(f"**City:** {selected_city}")
        st.sidebar.write(f"**Pollutants:** {len(selected_pollutants)} selected")
        st.sidebar.write(f"**Time Range:** {time_range}")
    
    def render_global_overview(self):
        """Render global overview tab."""
        st.header("🗺️ Global Air Quality Overview")
        
        # Get locations based on filters
        locations = self.client.get_locations(
            country=st.session_state.get('selected_country'),
            city=st.session_state.get('selected_city')
        )
        
        if not locations:
            st.warning("No monitoring locations found for the selected filters.")
            return
        
        # Get latest measurements
        location_ids = [loc['id'] for loc in locations[:100]]  # Limit for performance
        latest_data = self.client.get_latest_measurements(
            location_ids=location_ids,
            parameters=st.session_state.get('selected_pollutants', ['pm25'])
        )
        
        # Display summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Locations", len(locations))
        
        with col2:
            active_locations = len([loc for loc in locations if latest_data])
            st.metric("Active Locations", active_locations)
        
        with col3:
            countries = len(set(loc.get('country') for loc in locations if loc.get('country')))
            st.metric("Countries", countries)
        
        with col4:
            cities = len(set(loc.get('city') for loc in locations if loc.get('city')))
            st.metric("Cities", cities)
        
        # Map visualization options
        st.subheader("🗺️ Map Visualization")
        
        map_type = st.selectbox(
            "Select Map Type",
            ["Monitoring Locations", "Pollutant Heatmap", "Clustered View"]
        )
        
        if map_type == "Monitoring Locations":
            map_obj = self.maps.create_locations_map(locations, latest_data)
        elif map_type == "Pollutant Heatmap":
            selected_param = st.selectbox(
                "Select Pollutant for Heatmap",
                st.session_state.get('selected_pollutants', ['pm25']),
                format_func=lambda x: POLLUTANT_INFO[x]['display_name']
            )
            map_obj = self.maps.create_heatmap(locations, latest_data, selected_param)
        else:  # Clustered View
            map_obj = self.maps.create_clustered_map(locations, latest_data)
        
        # Display map
        try:
            from streamlit_folium import st_folium
            st_folium(map_obj, width=700, height=500)
        except ImportError:
            st.error("Folium map display requires streamlit-folium. Please install it.")
            st.write("Map data available but cannot display interactive map.")
    
    def render_current_conditions(self):
        """Render current conditions tab."""
        st.header("📊 Current Air Quality Conditions")
        
        # Get latest measurements
        latest_data = self.client.get_latest_measurements(
            countries=[st.session_state.get('selected_country')] if st.session_state.get('selected_country') else None,
            parameters=st.session_state.get('selected_pollutants', ['pm25'])
        )
        
        if not latest_data:
            st.warning("No current data available for the selected filters.")
            return
        
        # Current conditions overview chart
        st.subheader("📈 Pollutant Levels Overview")
        overview_chart = self.charts.create_current_conditions_chart(latest_data)
        st.plotly_chart(overview_chart, use_container_width=True)
        
        # Individual pollutant metrics
        st.subheader("🧪 Individual Pollutant Details")
        
        # Group data by parameter
        param_data = {}
        for measurement in latest_data:
            param = measurement.get('parameter')
            if param and param in st.session_state.get('selected_pollutants', []):
                if param not in param_data:
                    param_data[param] = []
                param_data[param].append(measurement)
        
        # Display metrics for each pollutant
        for param, measurements in param_data.items():
            pollutant_info = POLLUTANT_INFO.get(param, {})
            display_name = pollutant_info.get('display_name', param.upper())
            units = pollutant_info.get('units', '')
            description = pollutant_info.get('description', '')
            
            with st.expander(f"{display_name} - {len(measurements)} measurements"):
                col1, col2, col3 = st.columns(3)
                
                values = [m['value'] for m in measurements if m.get('value') is not None]
                if values:
                    avg_val = sum(values) / len(values)
                    min_val = min(values)
                    max_val = max(values)
                    
                    with col1:
                        st.metric(f"Average {display_name}", f"{avg_val:.2f} {units}")
                    with col2:
                        st.metric(f"Minimum {display_name}", f"{min_val:.2f} {units}")
                    with col3:
                        st.metric(f"Maximum {display_name}", f"{max_val:.2f} {units}")
                    
                    # AQI Gauge for PM2.5
                    if param == 'pm25':
                        st.subheader("Air Quality Index (AQI)")
                        aqi_chart = self.charts.create_aqi_gauge(avg_val, param)
                        st.plotly_chart(aqi_chart, use_container_width=True)
                
                st.markdown(f'<div class="pollutant-info"><strong>About {display_name}:</strong> {description}</div>', 
                           unsafe_allow_html=True)
        
        # Data table
        st.subheader("📋 Detailed Measurements")
        if latest_data:
            df = pd.DataFrame(latest_data)
            
            # Select relevant columns
            display_columns = ['locationName', 'city', 'country', 'parameter', 'value', 'unit', 'lastUpdated']
            available_columns = [col for col in display_columns if col in df.columns]
            
            if available_columns:
                df_display = df[available_columns].copy()
                
                # Format parameter names
                if 'parameter' in df_display.columns:
                    df_display['parameter'] = df_display['parameter'].map(
                        lambda x: POLLUTANT_INFO.get(x, {}).get('display_name', x.upper())
                    )
                
                st.dataframe(df_display, use_container_width=True)
                
                # Export functionality
                csv = df_display.to_csv(index=False)
                st.download_button(
                    label="📥 Download Current Data as CSV",
                    data=csv,
                    file_name=f"openaq_current_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    def render_historical_trends(self):
        """Render historical trends tab."""
        st.header("📈 Historical Air Quality Trends")
        
        # Location selection for detailed analysis
        locations = self.client.get_locations(
            country=st.session_state.get('selected_country'),
            city=st.session_state.get('selected_city')
        )
        
        if not locations:
            st.warning("No locations found for the selected filters.")
            return
        
        # Select specific location for detailed analysis
        location_options = {f"{loc.get('name', 'Unknown')} ({loc.get('city', 'N/A')})": loc['id'] 
                          for loc in locations[:50]}  # Limit for performance
        
        selected_location_name = st.selectbox(
            "Select Location for Detailed Analysis",
            list(location_options.keys())
        )
        
        if not selected_location_name:
            return
        
        selected_location_id = location_options[selected_location_name]
        
        # Get historical data for selected pollutants
        st.subheader(f"📊 Trends for {selected_location_name}")
        
        pollutant_data = {}
        
        with st.spinner("Loading historical data..."):
            for param in st.session_state.get('selected_pollutants', ['pm25']):
                measurements = self.client.get_measurements(
                    location_id=selected_location_id,
                    parameter=param,
                    date_from=st.session_state.get('date_from'),
                    date_to=st.session_state.get('date_to'),
                    limit=1000
                )
                if measurements:
                    pollutant_data[param] = measurements
        
        if not pollutant_data:
            st.warning("No historical data available for the selected location and time range.")
            return
        
        # Display options
        chart_type = st.selectbox(
            "Select Chart Type",
            ["Individual Pollutants", "Multi-Pollutant Comparison"]
        )
        
        if chart_type == "Individual Pollutants":
            # Individual charts for each pollutant
            for param, data in pollutant_data.items():
                chart = self.charts.create_time_series_chart(data, param, selected_location_name)
                st.plotly_chart(chart, use_container_width=True)
        
        else:
            # Multi-pollutant comparison
            if len(pollutant_data) > 1:
                chart = self.charts.create_multi_pollutant_chart(pollutant_data, selected_location_name)
                st.plotly_chart(chart, use_container_width=True)
            else:
                st.info("Select multiple pollutants to see comparison chart.")
        
        # Summary statistics
        st.subheader("📊 Summary Statistics")
        
        summary_data = []
        for param, measurements in pollutant_data.items():
            values = [m['value'] for m in measurements if m.get('value') is not None]
            if values:
                pollutant_info = POLLUTANT_INFO.get(param, {})
                summary_data.append({
                    'Pollutant': pollutant_info.get('display_name', param.upper()),
                    'Count': len(values),
                    'Average': f"{sum(values)/len(values):.2f}",
                    'Minimum': f"{min(values):.2f}",
                    'Maximum': f"{max(values):.2f}",
                    'Units': pollutant_info.get('units', '')
                })
        
        if summary_data:
            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True)
    
    def render_location_comparison(self):
        """Render location comparison tab."""
        st.header("🔍 Location Comparison")
        
        # Get available locations
        locations = self.client.get_locations(
            country=st.session_state.get('selected_country'),
            city=st.session_state.get('selected_city')
        )
        
        if not locations:
            st.warning("No locations found for the selected filters.")
            return
        
        # Multi-select for locations
        location_options = {f"{loc.get('name', 'Unknown')} ({loc.get('city', 'N/A')})": loc['id'] 
                          for loc in locations[:20]}  # Limit for performance
        
        selected_location_names = st.multiselect(
            "Select Locations to Compare (max 5)",
            list(location_options.keys()),
            max_selections=5
        )
        
        if len(selected_location_names) < 2:
            st.info("Please select at least 2 locations for comparison.")
            return
        
        # Select pollutant for comparison
        comparison_param = st.selectbox(
            "Select Pollutant for Comparison",
            st.session_state.get('selected_pollutants', ['pm25']),
            format_func=lambda x: POLLUTANT_INFO[x]['display_name']
        )
        
        # Get data for selected locations
        locations_data = {}
        
        with st.spinner("Loading comparison data..."):
            for location_name in selected_location_names:
                location_id = location_options[location_name]
                measurements = self.client.get_measurements(
                    location_id=location_id,
                    parameter=comparison_param,
                    date_from=st.session_state.get('date_from'),
                    date_to=st.session_state.get('date_to'),
                    limit=500
                )
                if measurements:
                    locations_data[location_name] = {comparison_param: measurements}
        
        if not locations_data:
            st.warning("No data available for comparison.")
            return
        
        # Create comparison chart
        comparison_chart = self.charts.create_comparison_chart(locations_data, comparison_param)
        st.plotly_chart(comparison_chart, use_container_width=True)
        
        # Comparison statistics
        st.subheader("📊 Comparison Statistics")
        
        comparison_stats = []
        for location_name, location_data in locations_data.items():
            measurements = location_data.get(comparison_param, [])
            values = [m['value'] for m in measurements if m.get('value') is not None]
            
            if values:
                comparison_stats.append({
                    'Location': location_name,
                    'Measurements': len(values),
                    'Average': f"{sum(values)/len(values):.2f}",
                    'Minimum': f"{min(values):.2f}",
                    'Maximum': f"{max(values):.2f}",
                    'Latest': f"{values[-1]:.2f}" if values else "N/A"
                })
        
        if comparison_stats:
            stats_df = pd.DataFrame(comparison_stats)
            st.dataframe(stats_df, use_container_width=True)
    
    def render_about(self):
        """Render about tab."""
        st.header("ℹ️ About This Dashboard")
        
        st.markdown("""
        ### 🌍 OpenAQ Air Quality Dashboard
        
        This dashboard provides comprehensive visualization and analysis of global air quality data 
        from the OpenAQ platform, the world's largest open air quality database.
        
        #### 📊 Features
        - **Global Overview**: Interactive maps showing monitoring locations worldwide
        - **Current Conditions**: Real-time air quality measurements and AQI calculations
        - **Historical Trends**: Time series analysis of pollutant concentrations
        - **Location Comparison**: Side-by-side comparison of multiple monitoring sites
        - **Data Export**: Download capabilities for further analysis
        
        #### 🧪 Monitored Pollutants
        """)
        
        for param, info in POLLUTANT_INFO.items():
            st.markdown(f"""
            **{info['display_name']}** ({info['units']})  
            {info['description']}
            """)
        
        st.markdown("""
        #### 📈 Data Sources
        - **OpenAQ Platform**: Global air quality data aggregation
        - **Government Agencies**: Official monitoring networks
        - **Research Institutions**: Academic and scientific monitoring
        - **Community Networks**: Citizen science and low-cost sensors
        
        #### 🔧 Technical Details
        - **Framework**: Streamlit (Python)
        - **Visualization**: Plotly, Folium
        - **API**: OpenAQ REST API v3
        - **Rate Limiting**: 60 requests/minute, 2000 requests/hour
        - **Data Refresh**: Configurable caching with manual refresh
        
        #### 📝 Data Attribution
        This dashboard uses data from OpenAQ and its contributing data providers. 
        Please refer to individual measurement metadata for specific data source attribution.
        
        #### 🔗 Links
        - [OpenAQ Platform](https://openaq.org/)
        - [OpenAQ API Documentation](https://docs.openaq.org/)
        - [GitHub Repository](https://github.com/openaq/openaq-api-v2)
        
        ---
        
        **Disclaimer**: This dashboard is for informational purposes only. 
        Air quality data may vary in accuracy and timeliness depending on the source.
        """)

def main():
    """Main application entry point."""
    try:
        dashboard = AirQualityDashboard()
        dashboard.run()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        st.info("Please check your API configuration and try refreshing the page.")

if __name__ == "__main__":
    main()
