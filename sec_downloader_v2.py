"""
SEC EDGAR Data Acquisition Tool - v2 (Robust Version)
Downloads 10-K filings for S&P 500 companies using SEC API
With exponential backoff and connection pooling
"""

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import json
import time
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sec_download_v2.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent / 'sec-edgar-filings'
BASE_DIR.mkdir(exist_ok=True)

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Data_Analyst anshumaankarna@gmail.com'

def create_robust_session():
    """Create requests session with retry strategy"""
    session = requests.Session()
    
    retry_strategy = Retry(
        total=5,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"],
        backoff_factor=2
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    session.headers.update({'User-Agent': USER_AGENT})
    
    return session

def get_cik_list_from_file():
    """Load CIK list from SEC company tickers JSON"""
    logger.info("Fetching CIK list from SEC company tickers...")
    
    session = create_robust_session()
    
    try:
        url = "https://www.sec.gov/files/company_tickers.json"
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        cik_dict = {}
        
        for entry in data.values():
            ticker = entry['ticker'].upper()
            cik = str(entry['cik_str']).zfill(10)
            cik_dict[ticker] = cik
        
        logger.info(f"Successfully loaded {len(cik_dict)} company CIK mappings")
        
        with open('cik_list.json', 'w') as f:
            json.dump(cik_dict, f, indent=2)
        
        return cik_dict
        
    except Exception as e:
        logger.error(f"Failed to fetch CIK list: {e}")
        
        if Path('cik_list.json').exists():
            logger.info("Loading from cached cik_list.json...")
            with open('cik_list.json') as f:
                return json.load(f)
        
        return {}

def search_filings(session, cik, form_type='10-K', max_retries=3):
    """Search for 10-K filings for a company with retries"""
    
    for attempt in range(max_retries):
        try:
            url = f"https://data.sec.gov/submissions/CIK{cik}.json"
            response = session.get(url, timeout=30)
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
                        }
                        filings.append(filing)
            
            return filings
            
        except requests.exceptions.Timeout:
            wait_time = 2 ** attempt * 5
            logger.warning(f"Timeout searching CIK {cik}, retrying in {wait_time}s (attempt {attempt+1}/{max_retries})...")
            time.sleep(wait_time)
            
        except Exception as e:
            logger.warning(f"Error searching filings for CIK {cik}: {e}")
            return []
    
    return []

def download_filing(session, company_ticker, cik, accession_number, report_date):
    """Download full submission text file"""
    try:
        accession_no_formatted = accession_number.replace('-', '')
        
        url = f"https://www.sec.gov/Archives/edgar/{cik}/{accession_no_formatted}/{accession_no_formatted}.txt"
        
        response = session.get(url, timeout=30)
        
        if response.status_code == 200 and len(response.text) > 500:
            year = int(report_date[:4])
            save_dir = BASE_DIR / company_ticker / '10-K' / accession_number
            save_dir.mkdir(parents=True, exist_ok=True)
            
            file_path = save_dir / 'full-submission.txt'
            
            with open(file_path, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(response.text)
            
            logger.info(f"✓ Downloaded {company_ticker} {year} 10-K ({len(response.text)} bytes)")
            return True
        else:
            logger.debug(f"Skipped {company_ticker} {accession_number}: Status {response.status_code}")
            return False
            
    except Exception as e:
        logger.debug(f"Error downloading {company_ticker} {accession_number}: {e}")
        return False

def download_company_filings(session, ticker, cik, years=3):
    """Download 10-K filings for a company"""
    
    filings = search_filings(session, cik, '10-K')
    
    if not filings:
        return 0
    
    current_year = datetime.now().year
    target_years = [current_year - i for i in range(years)]
    
    downloaded_count = 0
    
    for filing in filings[:10]:
        try:
            report_year = int(filing['reportDate'][:4])
            
            if report_year in target_years:
                success = download_filing(
                    session,
                    ticker,
                    cik,
                    filing['accessionNumber'],
                    filing['reportDate']
                )
                
                if success:
                    downloaded_count += 1
                
                time.sleep(0.5)
        except Exception as e:
            logger.debug(f"Error processing filing for {ticker}: {e}")
    
    return downloaded_count

def main():
    logger.info("="*80)
    logger.info("SEC EDGAR 10-K FILING DOWNLOADER - v2 (Robust)")
    logger.info("="*80)
    logger.info("")
    
    session = create_robust_session()
    
    cik_dict = get_cik_list_from_file()
    
    if not cik_dict:
        logger.error("Failed to load CIK list. Exiting.")
        return
    
    selected_companies = list(cik_dict.items())[:500]
    
    total_downloaded = 0
    success_count = 0
    
    logger.info(f"Starting download of 10-K filings for {len(selected_companies)} companies...")
    logger.info(f"Request timeout: 30 seconds per request")
    logger.info(f"Expected filings: ~{len(selected_companies) * 3} (3 years per company)")
    logger.info("")
    
    start_time = time.time()
    
    for idx, (ticker, cik) in enumerate(selected_companies, 1):
        try:
            logger.info(f"[{idx}/{len(selected_companies)}] {ticker}...", extra={'ticker': ticker})
            count = download_company_filings(session, ticker, cik, years=3)
            total_downloaded += count
            
            if count > 0:
                success_count += 1
            
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"Error processing {ticker}: {e}")
            time.sleep(5)
            continue
    
    elapsed = time.time() - start_time
    
    logger.info("")
    logger.info("="*80)
    logger.info("DOWNLOAD SUMMARY")
    logger.info("="*80)
    logger.info(f"Companies processed: {len(selected_companies)}")
    logger.info(f"Companies with successful downloads: {success_count}")
    logger.info(f"Total 10-K filings downloaded: {total_downloaded}")
    logger.info(f"Time elapsed: {elapsed:.1f} seconds")
    logger.info(f"Output directory: {BASE_DIR}")
    logger.info(f"Average per company: {elapsed/len(selected_companies):.1f} seconds")
    logger.info("")

if __name__ == '__main__':
    main()
