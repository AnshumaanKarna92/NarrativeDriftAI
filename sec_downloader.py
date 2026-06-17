"""
SEC EDGAR Data Acquisition Tool
Downloads 10-K filings for S&P 500 companies using SEC API
"""

import requests
import json
import time
import csv
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sec_download.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent / 'sec-edgar-filings'
BASE_DIR.mkdir(exist_ok=True)

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Data_Analyst anshumaankarna@gmail.com'
HEADERS = {'User-Agent': USER_AGENT}

S_AND_P_500 = {
    'AAPL': '0000320193',
    'MSFT': '0000789019',
    'GOOG': '0001652044',
    'GOOGL': '0001652044',
    'AMZN': '0001018724',
    'NVDA': '0001045810',
    'META': '0001326801',
    'TSLA': '0001018724',
    'BRK.B': '0001067983',
    'JNJ': '0000200406',
    'V': '0001652860',
    'WMT': '0000104169',
    'JPM': '0000019617',
    'MA': '0001141391',
    'PG': '0000080424',
    'CSCO': '0000858877',
    'CRM': '0001108772',
    'ADBE': '0000796343',
    'INTC': '0000050104',
    'AMD': '0000002488',
    'NFLX': '0001564590',
    'PYPL': '0001633917',
    'AVGO': '0001410828',
    'ACN': '0001467373',
    'TXN': '0000097476',
    'QCOM': '0000804842',
    'ORCL': '0001652331',
    'COP': '0000023104',
    'XOM': '0000034088',
    'CVX': '0000093410',
    'VICI': '0001745275',
    'LIN': '0000009310',
    'IBM': '0000051143',
    'AXP': '0000004962',
    'MU': '0000723125',
    'APA': '0000006779',
    'INTU': '0000896878',
    'MCD': '0000063908',
    'AMAT': '0000006951',
    'BKNG': '0001075531',
    'ASML': '0000884066',
    'F': '0000037996',
    'HON': '0000773840',
    'REGN': '0001018724',
    'COST': '0000909832',
    'LLY': '0000059478',
    'AZN': '0000825991',
    'GILD': '0000882095',
    'ABNB': '0001616707',
    'HLT': '0001585153',
    'AAL': '0000006201',
    'UAL': '0000100517',
    'DAL': '0000027904',
    'BAC': '0000070858',
    'WFC': '0000072971',
    'GS': '0000886947',
    'MS': '0000789019',
    'BX': '0001285785',
    'KKR': '0001655625',
    'SPY': '0000789960',
    'SWKS': '0000004127',
    'XLNX': '0000743988',
    'MPWR': '0001035267',
    'LSCC': '0000075885',
    'LATTICE': '0000075885',
}

def get_cik_list():
    """Get CIK mappings from SEC EDGAR company search"""
    logger.info("Fetching CIK list from SEC...")
    
    cik_dict = S_AND_P_500.copy()
    
    try:
        url = "https://www.sec.gov/files/company_tickers.json"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        for entry in data.values():
            ticker = entry['ticker']
            cik = str(entry['cik_str']).zfill(10)
            cik_dict[ticker] = cik
        
        logger.info(f"Loaded {len(cik_dict)} company CIK mappings")
        return cik_dict
        
    except Exception as e:
        logger.warning(f"Could not fetch full CIK list: {e}. Using predefined list.")
        return cik_dict

def search_filings(cik, form_type='10-K'):
    """Search for 10-K filings for a company"""
    try:
        url = f"https://data.sec.gov/submissions/CIK{cik}.json"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        filings = []
        
        if 'filings' in data and 'recent' in data['filings']:
            recent = data['filings']['recent']
            
            for i in range(len(recent.get('form', []))):
                if recent['form'][i] == form_type:
                    filing = {
                        'form': recent['form'][i],
                        'filingDate': recent['filingDate'][i],
                        'reportDate': recent['reportDate'][i],
                        'accessionNumber': recent['accessionNumber'][i],
                        'primaryDocument': recent.get('primaryDocument', [''])[i] if 'primaryDocument' in recent else '',
                    }
                    filings.append(filing)
        
        return filings
        
    except Exception as e:
        logger.warning(f"Error searching filings for CIK {cik}: {e}")
        return []

def download_filing(company_ticker, cik, accession_number, filing_date, report_date):
    """Download full submission text file for a filing"""
    try:
        accession_no_formatted = accession_number.replace('-', '')
        
        url = f"https://www.sec.gov/cgi-bin/viewer?action=view&cik={cik}&accession_number={accession_number}&xbrl_type=v"
        
        alt_url = f"https://www.sec.gov/Archives/edgar/{cik}/{accession_no_formatted}/{accession_no_formatted}.txt"
        
        response = requests.get(alt_url, headers=HEADERS, timeout=15)
        
        if response.status_code == 404:
            url = f"https://www.sec.gov/cgi-bin/viewer?action=view&cik={cik}&accession_number={accession_number}"
            response = requests.get(url, headers=HEADERS, timeout=15)
        
        if response.status_code == 200:
            year = int(report_date[:4])
            save_dir = BASE_DIR / company_ticker / '10-K' / accession_number
            save_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = save_dir / 'full-submission.txt'
            
            with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(response.text)
            
            logger.info(f"Downloaded {company_ticker} {year} 10-K (Accession: {accession_number})")
            return True
        else:
            logger.warning(f"Failed to download {company_ticker} {accession_number}: Status {response.status_code}")
            return False
            
    except Exception as e:
        logger.warning(f"Error downloading {company_ticker} {accession_number}: {e}")
        return False

def download_company_filings(ticker, cik, years=3):
    """Download 10-K filings for a company for specified years"""
    logger.info(f"Processing {ticker} (CIK: {cik})...")
    
    filings = search_filings(cik, '10-K')
    
    if not filings:
        logger.warning(f"No 10-K filings found for {ticker}")
        return 0
    
    current_year = datetime.now().year
    target_years = [current_year - i for i in range(years)]
    
    downloaded_count = 0
    
    for filing in filings[:10]:
        report_year = int(filing['reportDate'][:4])
        
        if report_year in target_years:
            success = download_filing(
                ticker,
                cik,
                filing['accessionNumber'],
                filing['filingDate'],
                filing['reportDate']
            )
            
            if success:
                downloaded_count += 1
            
            time.sleep(0.5)
    
    return downloaded_count

def main():
    logger.info("="*80)
    logger.info("SEC EDGAR 10-K FILING DOWNLOADER")
    logger.info("="*80)
    logger.info("")
    
    cik_dict = get_cik_list()
    
    selected_companies = list(cik_dict.items())[:500]
    
    total_downloaded = 0
    success_count = 0
    
    logger.info(f"Starting download of 10-K filings for {len(selected_companies)} companies...")
    logger.info("Years: 2023, 2024, 2025, 2026")
    logger.info("")
    
    for idx, (ticker, cik) in enumerate(selected_companies, 1):
        try:
            logger.info(f"[{idx}/{len(selected_companies)}] Processing {ticker}...")
            count = download_company_filings(ticker, cik, years=4)
            total_downloaded += count
            
            if count > 0:
                success_count += 1
            
            time.sleep(1)
            
        except Exception as e:
            logger.error(f"Error processing {ticker}: {e}")
            continue
    
    logger.info("")
    logger.info("="*80)
    logger.info("DOWNLOAD SUMMARY")
    logger.info("="*80)
    logger.info(f"Companies processed: {len(selected_companies)}")
    logger.info(f"Companies with successful downloads: {success_count}")
    logger.info(f"Total 10-K filings downloaded: {total_downloaded}")
    logger.info(f"Output directory: {BASE_DIR}")
    logger.info("")

if __name__ == '__main__':
    main()
