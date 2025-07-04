
"""OpenAQ API client with rate limiting and caching."""

import requests
import time
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import streamlit as st
from utils.config import Config

class OpenAQClient:
    """OpenAQ API client with built-in rate limiting and caching."""
    
    def __init__(self):
        self.base_url = Config.OPENAQ_BASE_URL
        self.api_key = Config.OPENAQ_API_KEY
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': self.api_key,
            'User-Agent': 'OpenAQ-Python-Dashboard/1.0'
        })
        
        # Rate limiting tracking
        self.last_request_time = 0
        self.requests_this_minute = 0
        self.minute_start = time.time()
    
    def _check_rate_limit(self):
        """Check and enforce rate limits."""
        current_time = time.time()
        
        # Reset minute counter if needed
        if current_time - self.minute_start >= 60:
            self.requests_this_minute = 0
            self.minute_start = current_time
        
        # Check if we need to wait
        if self.requests_this_minute >= Config.REQUESTS_PER_MINUTE:
            wait_time = 60 - (current_time - self.minute_start)
            if wait_time > 0:
                time.sleep(wait_time)
                self.requests_this_minute = 0
                self.minute_start = time.time()
    
    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """Make API request with rate limiting."""
        self._check_rate_limit()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.get(url, params=params or {})
            self.requests_this_minute += 1
            
            # Handle rate limit response
            if response.status_code == 429:
                reset_time = int(response.headers.get('x-ratelimit-reset', 60))
                time.sleep(reset_time)
                response = self.session.get(url, params=params or {})
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {str(e)}")
            return {}
    
    @st.cache_data(ttl=Config.CACHE_TIMEOUT)
    def get_countries(_self) -> List[Dict]:
        """Get list of available countries."""
        data = _self._make_request('countries')
        return data.get('results', [])
    
    @st.cache_data(ttl=Config.CACHE_TIMEOUT)
    def get_cities(_self, country: str = None) -> List[Dict]:
        """Get list of available cities."""
        params = {}
        if country:
            params['countries'] = country
        
        data = _self._make_request('cities', params)
        return data.get('results', [])
    
    @st.cache_data(ttl=Config.CACHE_TIMEOUT)
    def get_locations(_self, country: str = None, city: str = None, 
                     bbox: Tuple[float, float, float, float] = None) -> List[Dict]:
        """Get list of monitoring locations."""
        params = {'limit': 1000}
        
        if country:
            params['countries'] = country
        if city:
            params['cities'] = city
        if bbox:
            params['bbox'] = f"{bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]}"
        
        data = _self._make_request('locations', params)
        return data.get('results', [])
    
    @st.cache_data(ttl=Config.CACHE_TIMEOUT)
    def get_parameters(_self) -> List[Dict]:
        """Get list of available parameters (pollutants)."""
        data = _self._make_request('parameters')
        return data.get('results', [])
    
    def get_latest_measurements(self, location_ids: List[int] = None, 
                              countries: List[str] = None,
                              parameters: List[str] = None) -> List[Dict]:
        """Get latest measurements."""
        params = {'limit': 1000}
        
        if location_ids:
            params['locations'] = ','.join(map(str, location_ids))
        if countries:
            params['countries'] = ','.join(countries)
        if parameters:
            params['parameters'] = ','.join(parameters)
        
        data = self._make_request('latest', params)
        return data.get('results', [])
    
    def get_measurements(self, location_id: int = None, 
                        parameter: str = None,
                        date_from: datetime = None,
                        date_to: datetime = None,
                        limit: int = 1000) -> List[Dict]:
        """Get historical measurements."""
        params = {'limit': limit, 'sort': 'datetime'}
        
        if location_id:
            params['locations'] = location_id
        if parameter:
            params['parameters'] = parameter
        if date_from:
            params['date_from'] = date_from.isoformat()
        if date_to:
            params['date_to'] = date_to.isoformat()
        
        data = self._make_request('measurements', params)
        return data.get('results', [])
    
    def get_location_measurements_aggregated(self, location_id: int, 
                                           parameter: str,
                                           period: str = 'hour',
                                           date_from: datetime = None,
                                           date_to: datetime = None) -> List[Dict]:
        """Get aggregated measurements for a location."""
        endpoint = f"locations/{location_id}/measurements/{period}s"
        params = {'parameters': parameter}
        
        if date_from:
            params['date_from'] = date_from.isoformat()
        if date_to:
            params['date_to'] = date_to.isoformat()
        
        data = self._make_request(endpoint, params)
        return data.get('results', [])

# Global client instance
@st.cache_resource
def get_openaq_client():
    """Get cached OpenAQ client instance."""
    try:
        Config.validate_api_key()
        return OpenAQClient()
    except ValueError as e:
        st.error(str(e))
        st.stop()
