
"""Map visualization utilities for air quality data."""

import folium
from folium import plugins
import pandas as pd
from typing import List, Dict, Tuple
import streamlit as st
from ..utils.config import POLLUTANT_INFO, AQI_THRESHOLDS

class AirQualityMaps:
    """Class for generating air quality maps."""
    
    @staticmethod
    def create_locations_map(locations: List[Dict], 
                           latest_data: List[Dict] = None,
                           center: Tuple[float, float] = (40.7128, -74.0060),
                           zoom: int = 2) -> folium.Map:
        """Create map showing monitoring locations."""
        m = folium.Map(location=center, zoom_start=zoom, tiles='OpenStreetMap')
        
        # Create a dictionary for quick lookup of latest measurements
        latest_lookup = {}
        if latest_data:
            for measurement in latest_data:
                location_id = measurement.get('locationId')
                parameter = measurement.get('parameter')
                if location_id and parameter:
                    if location_id not in latest_lookup:
                        latest_lookup[location_id] = {}
                    latest_lookup[location_id][parameter] = measurement
        
        # Add markers for each location
        for location in locations:
            lat = location.get('coordinates', {}).get('latitude')
            lon = location.get('coordinates', {}).get('longitude')
            location_id = location.get('id')
            
            if lat is None or lon is None:
                continue
            
            # Create popup content
            popup_content = f"""
            <div style="width: 300px;">
                <h4>{location.get('name', 'Unknown Location')}</h4>
                <p><strong>City:</strong> {location.get('city', 'N/A')}</p>
                <p><strong>Country:</strong> {location.get('country', 'N/A')}</p>
                <p><strong>Location ID:</strong> {location_id}</p>
            """
            
            # Add latest measurements if available
            if location_id in latest_lookup:
                popup_content += "<hr><h5>Latest Measurements:</h5>"
                for parameter, measurement in latest_lookup[location_id].items():
                    pollutant_info = POLLUTANT_INFO.get(parameter, {})
                    display_name = pollutant_info.get('display_name', parameter.upper())
                    units = pollutant_info.get('units', '')
                    value = measurement.get('value', 'N/A')
                    popup_content += f"<p><strong>{display_name}:</strong> {value} {units}</p>"
            
            popup_content += "</div>"
            
            # Determine marker color based on data availability and quality
            marker_color = 'blue'
            if location_id in latest_lookup:
                # Color based on PM2.5 if available (most common health indicator)
                pm25_data = latest_lookup[location_id].get('pm25')
                if pm25_data:
                    pm25_value = pm25_data.get('value', 0)
                    marker_color = AirQualityMaps._get_aqi_color(pm25_value, 'pm25')
                else:
                    marker_color = 'green'  # Has data but no PM2.5
            else:
                marker_color = 'gray'  # No recent data
            
            folium.CircleMarker(
                location=[lat, lon],
                radius=6,
                popup=folium.Popup(popup_content, max_width=350),
                tooltip=location.get('name', 'Unknown Location'),
                color='white',
                weight=2,
                fillColor=marker_color,
                fillOpacity=0.7
            ).add_to(m)
        
        # Add a legend
        legend_html = '''
        <div style="position: fixed; 
                    bottom: 50px; left: 50px; width: 200px; height: 120px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px">
        <h4>Air Quality Legend</h4>
        <p><i class="fa fa-circle" style="color:green"></i> Good (0-12 µg/m³)</p>
        <p><i class="fa fa-circle" style="color:yellow"></i> Moderate (12-35 µg/m³)</p>
        <p><i class="fa fa-circle" style="color:orange"></i> Unhealthy for Sensitive</p>
        <p><i class="fa fa-circle" style="color:red"></i> Unhealthy (55+ µg/m³)</p>
        <p><i class="fa fa-circle" style="color:gray"></i> No Recent Data</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        return m
    
    @staticmethod
    def create_heatmap(locations: List[Dict], 
                      latest_data: List[Dict],
                      parameter: str = 'pm25',
                      center: Tuple[float, float] = (40.7128, -74.0060),
                      zoom: int = 2) -> folium.Map:
        """Create heatmap for a specific pollutant."""
        m = folium.Map(location=center, zoom_start=zoom, tiles='OpenStreetMap')
        
        # Prepare data for heatmap
        heat_data = []
        
        # Create lookup for latest measurements
        latest_lookup = {}
        for measurement in latest_data:
            location_id = measurement.get('locationId')
            param = measurement.get('parameter')
            if location_id and param == parameter:
                latest_lookup[location_id] = measurement.get('value', 0)
        
        # Collect coordinates and values
        for location in locations:
            location_id = location.get('id')
            lat = location.get('coordinates', {}).get('latitude')
            lon = location.get('coordinates', {}).get('longitude')
            
            if lat is None or lon is None or location_id not in latest_lookup:
                continue
            
            value = latest_lookup[location_id]
            if value > 0:  # Only include positive values
                heat_data.append([lat, lon, value])
        
        if heat_data:
            # Add heatmap layer
            plugins.HeatMap(
                heat_data,
                min_opacity=0.2,
                max_zoom=18,
                radius=25,
                blur=15,
                gradient={
                    0.0: 'blue',
                    0.3: 'green', 
                    0.5: 'yellow',
                    0.7: 'orange',
                    1.0: 'red'
                }
            ).add_to(m)
        
        # Add title
        pollutant_info = POLLUTANT_INFO.get(parameter, {})
        display_name = pollutant_info.get('display_name', parameter.upper())
        
        title_html = f'''
        <h3 align="center" style="font-size:20px"><b>{display_name} Concentration Heatmap</b></h3>
        '''
        m.get_root().html.add_child(folium.Element(title_html))
        
        return m
    
    @staticmethod
    def _get_aqi_color(value: float, parameter: str = 'pm25') -> str:
        """Get color based on AQI thresholds."""
        thresholds = AQI_THRESHOLDS.get(parameter, AQI_THRESHOLDS['pm25'])
        
        for min_val, max_val, category, color in thresholds:
            if min_val <= value <= max_val:
                # Convert hex to CSS color names for folium
                color_map = {
                    '#00E400': 'green',
                    '#FFFF00': 'yellow', 
                    '#FF7E00': 'orange',
                    '#FF0000': 'red',
                    '#8F3F97': 'purple',
                    '#7E0023': 'darkred'
                }
                return color_map.get(color, 'blue')
        
        return 'blue'
    
    @staticmethod
    def create_clustered_map(locations: List[Dict],
                           latest_data: List[Dict] = None,
                           center: Tuple[float, float] = (40.7128, -74.0060),
                           zoom: int = 2) -> folium.Map:
        """Create map with marker clustering for better performance."""
        m = folium.Map(location=center, zoom_start=zoom, tiles='OpenStreetMap')
        
        # Create marker cluster
        marker_cluster = plugins.MarkerCluster().add_to(m)
        
        # Create lookup for latest measurements
        latest_lookup = {}
        if latest_data:
            for measurement in latest_data:
                location_id = measurement.get('locationId')
                parameter = measurement.get('parameter')
                if location_id and parameter:
                    if location_id not in latest_lookup:
                        latest_lookup[location_id] = {}
                    latest_lookup[location_id][parameter] = measurement
        
        # Add markers to cluster
        for location in locations:
            lat = location.get('coordinates', {}).get('latitude')
            lon = location.get('coordinates', {}).get('longitude')
            location_id = location.get('id')
            
            if lat is None or lon is None:
                continue
            
            # Create popup content
            popup_content = f"""
            <div style="width: 300px;">
                <h4>{location.get('name', 'Unknown Location')}</h4>
                <p><strong>City:</strong> {location.get('city', 'N/A')}</p>
                <p><strong>Country:</strong> {location.get('country', 'N/A')}</p>
            """
            
            # Add latest measurements if available
            if location_id in latest_lookup:
                popup_content += "<hr><h5>Latest Measurements:</h5>"
                for parameter, measurement in latest_lookup[location_id].items():
                    pollutant_info = POLLUTANT_INFO.get(parameter, {})
                    display_name = pollutant_info.get('display_name', parameter.upper())
                    units = pollutant_info.get('units', '')
                    value = measurement.get('value', 'N/A')
                    popup_content += f"<p><strong>{display_name}:</strong> {value} {units}</p>"
            
            popup_content += "</div>"
            
            folium.Marker(
                location=[lat, lon],
                popup=folium.Popup(popup_content, max_width=350),
                tooltip=location.get('name', 'Unknown Location'),
                icon=folium.Icon(
                    color='green' if location_id in latest_lookup else 'gray',
                    icon='info-sign'
                )
            ).add_to(marker_cluster)
        
        return m
