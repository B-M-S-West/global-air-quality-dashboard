
# OpenAQ Air Quality Dashboard

A comprehensive Python-only air quality dashboard using the OpenAQ API to visualize global air pollution data.

## 🌍 Features

- **Global Overview**: Interactive maps showing monitoring locations worldwide
- **Current Conditions**: Real-time air quality measurements and AQI calculations  
- **Historical Trends**: Time series analysis of pollutant concentrations
- **Location Comparison**: Side-by-side comparison of multiple monitoring sites
- **Data Export**: Download capabilities for further analysis

## 🧪 Monitored Pollutants

- **PM2.5**: Fine particulate matter (≤ 2.5 micrometers)
- **PM10**: Inhalable particulate matter (≤ 10 micrometers)
- **NO₂**: Nitrogen dioxide
- **O₃**: Ground-level ozone
- **CO**: Carbon monoxide
- **SO₂**: Sulfur dioxide
- **BC**: Black Carbon

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAQ API key (free registration at [openaq.org](https://openaq.org/))

### Installation

1. **Clone or download this project**
   ```bash
   cd ~/openaq_python_dashboard
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API key**
   ```bash
   cp .env.example .env
   # Edit .env file and add your OpenAQ API key
   ```

5. **Run the dashboard**
   ```bash
   streamlit run openaq_dash/ui/app.py
   ```

6. **Open your browser**
   - Navigate to `http://localhost:8501`

## 📁 Project Structure

```
openaq_python_dashboard/
├── openaq_dash/
│   ├── api/
│   │   └── client.py          # OpenAQ API client with rate limiting
│   ├── ui/
│   │   └── app.py            # Main Streamlit application
│   ├── plots/
│   │   ├── charts.py         # Chart generation utilities
│   │   └── maps.py           # Map visualization utilities
│   └── utils/
│       └── config.py         # Configuration and constants
├── tests/                    # Test files (future)
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# OpenAQ API Configuration
OPENAQ_API_KEY=your_api_key_here
OPENAQ_BASE_URL=https://api.openaq.org/v3
```

### API Key Setup

1. Visit [OpenAQ Developer Portal](https://openaq.org/developers/)
2. Sign up for a free account
3. Generate your API key
4. Add the key to your `.env` file

## 🎛️ Dashboard Usage

### Global Overview Tab
- View monitoring locations on interactive maps
- Filter by country and city
- Choose between location markers, heatmaps, or clustered views
- See real-time data availability

### Current Conditions Tab
- View latest measurements for all pollutants
- See Air Quality Index (AQI) calculations
- Export current data as CSV
- Detailed pollutant information and health implications

### Historical Trends Tab
- Select specific monitoring locations
- Analyze time series data for individual pollutants
- Compare multiple pollutants over time
- Customizable date ranges (24 hours to 30 days)

### Location Comparison Tab
- Compare up to 5 monitoring locations
- Side-by-side pollutant analysis
- Statistical comparisons (average, min, max)
- Export comparison data

## 🔧 Technical Details

### Rate Limiting
- **Free Tier**: 60 requests/minute, 2000 requests/hour
- Built-in rate limiting with automatic backoff
- Intelligent caching to minimize API calls

### Data Caching
- 5-minute cache timeout for real-time data
- Longer caching for static metadata
- Manual refresh capability

### Performance Optimizations
- Streamlit caching for expensive operations
- Pagination for large datasets
- Efficient API query patterns

## 📊 Data Sources

The dashboard aggregates data from multiple sources through OpenAQ:

- **Government Agencies**: Official regulatory monitoring networks
- **Research Institutions**: Academic and scientific monitoring projects  
- **Community Networks**: Citizen science and low-cost sensor deployments

## 🛠️ Development

### Adding New Features

1. **API Extensions**: Modify `openaq_dash/api/client.py`
2. **Visualizations**: Add charts to `openaq_dash/plots/charts.py`
3. **Maps**: Extend mapping in `openaq_dash/plots/maps.py`
4. **UI Components**: Update `openaq_dash/ui/app.py`

### Testing

```bash
# Run tests (when implemented)
python -m pytest tests/

# Check code style
flake8 openaq_dash/
```

## 📝 Data Attribution

This dashboard uses data from OpenAQ and its contributing data providers. When using or sharing data from this dashboard, please provide appropriate attribution to both OpenAQ and the original data providers.

## 🔗 Useful Links

- [OpenAQ Platform](https://openaq.org/)
- [OpenAQ API Documentation](https://docs.openaq.org/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Plotly Documentation](https://plotly.com/python/)

## 📄 License

This project is open source. Please refer to OpenAQ's terms of service for data usage guidelines.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## ⚠️ Disclaimer

This dashboard is for informational purposes only. Air quality data may vary in accuracy and timeliness depending on the source. Always refer to official government sources for health advisories and regulatory compliance.
