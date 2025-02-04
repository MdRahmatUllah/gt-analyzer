# Corporate Structure Visualization Tool

A powerful visualization tool designed to analyze and display corporate structures, hierarchies, and relationships using interactive maps, networks, and statistical views.

## Features

- Interactive map visualization
- Corporate hierarchy visualization
- Network relationship views
- Statistical analysis and distribution views
- Tabular data presentation
- Filtering capabilities by country and ownership share
- Support for Excel/CSV data import

## Project Structure

```
Corporate Structure Visualization Tool/
├── src/               # Source code
│   ├── views/         # Different visualization views
│   │   ├── map_view.py
│   │   ├── statistics_view.py
│   │   ├── hierarchy_views.py
│   │   ├── network_views.py
│   │   └── distribution_views.py
│   ├── components/    # Reusable UI components
│   ├── logic/         # Business logic and data processing
│   └── app.py         # Main application file
├── data/             # Sample data and datasets
└── tests/            # Unit tests
```

## Data Structure

The application expects data in Excel/CSV format with the following structure:

1. **Company Information**
   - Company names
   - Location/Country
   - Ownership percentages
   - Additional metadata

2. **Relationships**
   - Parent-child company relationships
   - Ownership stakes
   - Cross-company connections

## Setup and Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/corporate-structure-viz.git
cd corporate-structure-viz
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run src/app.py
```

2. Using the application:
   - Upload your Excel/CSV file using the sidebar
   - Apply filters for countries and minimum share percentage
   - Toggle person/company visibility
   - Explore different visualization views:
     - Map View: Geographical distribution
     - Hierarchy View: Corporate structure
     - Network View: Relationship visualization
     - Distribution View: Statistical analysis
     - Table View: Raw data exploration

## Required Data Format

Your Excel/CSV file should contain the following minimum information:
- Company names
- Country/Location information
- Ownership percentages
- Parent-child relationships

## Troubleshooting

### Python Version Compatibility
This project works best with Python 3.11. If you encounter dependency issues with other Python versions, follow these steps:

1. Install Python 3.11:
```bash
# Using winget on Windows
winget install Python.Python.3.11
```

2. Create a new virtual environment with Python 3.11:
```bash
# Deactivate existing environment if any
deactivate

# Create new environment
py -3.11 -m venv .venv-py311

# Activate new environment
.\.venv-py311\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Common Issues

1. **CMake Error with pyarrow installation**
   If you encounter CMake-related errors while installing dependencies:
   ```bash
   # Install CMake using winget
   winget install Kitware.CMake
   ```
   
2. **Visual C++ Build Tools Error**
   If you get errors related to building wheels:
   ```bash
   # Install Visual Studio Build Tools
   winget install Microsoft.VisualStudio.2022.BuildTools
   ```

3. **Package Version Conflicts**
   If you experience version conflicts, the following package versions are known to work well together:
   ```
   streamlit<1.30.0
   pandas<2.1.0
   numpy<1.25.0
   ```
   These version constraints are already included in the requirements.txt file.

### Still Having Issues?
If you continue to experience problems:
1. Make sure you're using Python 3.11
2. Try creating a fresh virtual environment
3. Ensure all system dependencies (CMake, Build Tools) are installed
4. Check if your Python installation is added to PATH

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Your Name - your.email@example.com
Project Link: https://github.com/yourusername/corporate-structure-viz
