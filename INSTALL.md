# Installation Guide

## Quick Start

### 1. Prerequisites
- Python 3.8 or higher
- Chrome browser installed
- Internet connection

### 2. Installation Steps

#### Option A: Using pip (Recommended)
```bash
# Clone the repository
git clone https://github.com/Chirag819/scrapper.git
cd scrapper

# Install dependencies
pip install -r requirements.txt
```

#### Option B: Using setup.py
```bash
# Clone the repository
git clone https://github.com/Chirag819/scrapper.git
cd scrapper

# Install the package
pip install -e .
```

#### Option C: Using virtual environment (Recommended for development)
```bash
# Clone the repository
git clone https://github.com/Chirag819/scrapper.git
cd scrapper

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
python main.py --help
```

### 4. First Run
```bash
python main.py --company "Slack" --start-date "2024-01-01" --end-date "2025-12-31" --source "capterra"
```

## Troubleshooting

### Chrome Driver Issues
- Ensure Chrome browser is installed
- The script will automatically download compatible ChromeDriver
- If issues persist, try updating Chrome browser

### Permission Errors
- Ensure you have write permissions for the output directory
- On Linux/macOS: `chmod 755 output/`

### Network Issues
- Check internet connection
- Verify firewall settings
- Try with different network

### Python Version Issues
- Ensure Python 3.8+ is installed
- Check with: `python --version`

## Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/Chirag819/scrapper.git
cd scrapper
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows
```

### 3. Install Development Dependencies
```bash
pip install -r requirements.txt
pip install pytest black flake8 mypy
```

### 4. Run Tests
```bash
pytest
```

### 5. Code Formatting
```bash
black .
flake8 .
mypy .
```

## Docker Installation (Optional)

### 1. Create Dockerfile
```dockerfile
FROM python:3.11-slim

# Install Chrome dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    curl \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py", "--help"]
```

### 2. Build and Run
```bash
docker build -t saas-scraper .
docker run -it saas-scraper --company "Slack" --start-date "2024-01-01" --end-date "2025-12-31" --source "capterra"
```

## Platform-Specific Notes

### Windows
- Ensure Chrome is installed in default location
- Use PowerShell or Command Prompt
- May need to run as administrator for some operations

### macOS
- Install Chrome from official website
- May need to allow Chrome in Security & Privacy settings
- Use Terminal or iTerm2

### Linux
- Install Chrome: `wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -`
- Add repository: `echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" | sudo tee /etc/apt/sources.list.d/google-chrome.list`
- Install: `sudo apt update && sudo apt install google-chrome-stable`

## Support

For installation issues:
1. Check the troubleshooting section above
2. Create an issue in the repository
3. Contact support at [your-email@domain.com]
