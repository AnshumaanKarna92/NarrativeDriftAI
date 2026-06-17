"""
Research Project Configuration
ESG Disclosure Strategy vs ESG Performance Analysis
"""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
CODE_DIR = PROJECT_ROOT / "code"
RESULTS_DIR = PROJECT_ROOT / "results"
PAPER_DIR = PROJECT_ROOT / "paper"
DOCS_DIR = PROJECT_ROOT / "documentation"

# Data subdirectories
SEC_FILINGS_DIR = RAW_DATA_DIR / "sec_filings"
ESG_RATINGS_DIR = RAW_DATA_DIR / "esg_ratings"
ENVIRONMENTAL_DATA_DIR = RAW_DATA_DIR / "environmental"
SOCIAL_DATA_DIR = RAW_DATA_DIR / "social"
GOVERNANCE_DATA_DIR = RAW_DATA_DIR / "governance"

# Results subdirectories
FIGURES_DIR = RESULTS_DIR / "figures"
TABLES_DIR = RESULTS_DIR / "tables"

# Create directories if they don't exist
for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, CODE_DIR, 
                   RESULTS_DIR, PAPER_DIR, DOCS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Analysis parameters
ANALYSIS_CONFIG = {
    'start_year': 2020,
    'end_year': 2025,
    'company_sample_size': 500,  # Full S&P 500
    'prototype_sample_size': 50,  # For initial testing
    'esg_frameworks': ['Environmental', 'Social', 'Governance'],
    'min_documents_per_company': 4,  # At least 4 years of data
}

# SEC API Configuration
SEC_CONFIG = {
    'base_url': 'https://data.sec.gov',
    'headers': {
        'User-Agent': 'Research Project (research@university.edu)'
    },
    'rate_limit_delay': 0.2,  # Seconds between requests (respectful to SEC)
}

# S&P 500 Companies (Top 50 for initial prototype, full list for production)
# Format: {ticker: (cik, company_name, sector)}

PROTOTYPE_COMPANIES = {
    'MSFT': ('0000789019', 'Microsoft Corporation', 'Technology'),
    'AAPL': ('0000320193', 'Apple Inc', 'Technology'),
    'NVDA': ('0001045810', 'NVIDIA Corporation', 'Technology'),
    'GOOG': ('0001652044', 'Alphabet Inc', 'Technology'),
    'AMZN': ('0001018724', 'Amazon.com Inc', 'Consumer Discretionary'),
    'META': ('0001326801', 'Meta Platforms Inc', 'Communication Services'),
    'TSLA': ('0001018724', 'Tesla Inc', 'Consumer Discretionary'),
    'BRK.B': ('0001067983', 'Berkshire Hathaway Inc', 'Financials'),
    'JNJ': ('0000200406', 'Johnson & Johnson', 'Healthcare'),
    'V': ('0001403161', 'Visa Inc', 'Financials'),
    'WMT': ('0000104169', 'Walmart Inc', 'Consumer Staples'),
    'JPM': ('0000019617', 'JPMorgan Chase & Co', 'Financials'),
    'MA': ('0001141391', 'Mastercard Incorporated', 'Financials'),
    'XOM': ('0000034088', 'Exxon Mobil Corporation', 'Energy'),
    'KO': ('0000021344', 'The Coca-Cola Company', 'Consumer Staples'),
    'LLY': ('0000059478', 'Eli Lilly and Company', 'Healthcare'),
    'CVX': ('0000093410', 'Chevron Corporation', 'Energy'),
    'MCD': ('0000063908', 'McDonald\'s Corporation', 'Consumer Discretionary'),
    'PG': ('0000080424', 'Procter & Gamble Company', 'Consumer Staples'),
    'GE': ('0000040545', 'General Electric Company', 'Industrials'),
    'NFLX': ('0001564590', 'Netflix Inc', 'Communication Services'),
    'CSCO': ('0000858877', 'Cisco Systems Inc', 'Technology'),
    'INTC': ('0000050104', 'Intel Corporation', 'Technology'),
    'AMD': ('0000002488', 'Advanced Micro Devices Inc', 'Technology'),
    'CRM': ('0001018724', 'Salesforce Inc', 'Software'),
    'ADBE': ('0000796343', 'Adobe Inc', 'Software'),
    'NOW': ('0001786787', 'ServiceNow Inc', 'Software'),
    'ACN': ('0001467373', 'Accenture plc', 'Information Technology'),
    'IBM': ('0000051143', 'International Business Machines', 'Technology'),
    'ORCL': ('0001652044', 'Oracle Corporation', 'Software'),
    'AVGO': ('0001341019', 'Broadcom Inc', 'Semiconductors'),
    'QCOM': ('0000804142', 'QUALCOMM Incorporated', 'Semiconductors'),
    'ASML': ('0000800054', 'ASML Holding NV', 'Technology'),
    'TSM': ('0000884395', 'Taiwan Semiconductor Manufacturing', 'Semiconductors'),
    'CPRT': ('0001047469', 'Copart Inc', 'Industrials'),
    'UNP': ('0000100104', 'Union Pacific Corporation', 'Industrials'),
    'CSX': ('0000277948', 'CSX Corporation', 'Industrials'),
    'CAT': ('0000018230', 'Caterpillar Inc', 'Industrials'),
    'BA': ('0000012927', 'The Boeing Company', 'Industrials'),
    'RTX': ('0000109357', 'Raytheon Technologies Corporation', 'Industrials'),
    'LMT': ('0000060086', 'Lockheed Martin Corporation', 'Industrials'),
    'HON': ('0000040440', 'Honeywell International Inc', 'Industrials'),
    'MMM': ('0000066740', '3M Company', 'Industrials'),
    'DE': ('0000315189', 'Deere & Company', 'Industrials'),
    'AXP': ('0000004962', 'American Express Company', 'Financials'),
    'GS': ('0000886947', 'The Goldman Sachs Group Inc', 'Financials'),
    'MS': ('0000895421', 'Morgan Stanley', 'Financials'),
    'BLK': ('0001364742', 'BlackRock Inc', 'Financials'),
    'WFC': ('0000072971', 'Wells Fargo & Company', 'Financials'),
    'BAC': ('0000070858', 'Bank of America Corporation', 'Financials'),
}

# Full S&P 500 list (abbreviated - full version would be much longer)
# For production, we'll use the COMPLETE list from data source
SP500_COMPANIES = PROTOTYPE_COMPANIES  # Will be expanded dynamically

# Configuration flags
CONFIG = {
    'mode': 'prototype',  # 'prototype' or 'production'
    'use_cache': True,
    'verbose': True,
    'parallel_downloads': True,
    'num_workers': 4,
    'timeout_seconds': 30,
}

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'detailed': {
            'format': '%(asctime)s [%(levelname)s] %(name)s [%(filename)s:%(lineno)d]: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': str(DOCS_DIR / 'research_project.log'),
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file'],
    },
}

if __name__ == '__main__':
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Data Directory: {DATA_DIR}")
    print(f"Number of prototype companies: {len(PROTOTYPE_COMPANIES)}")
