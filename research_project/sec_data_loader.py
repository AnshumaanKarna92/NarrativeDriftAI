import os
import re
from pathlib import Path
import pandas as pd
import logging

logger = logging.getLogger(__name__)

SEC_EDGAR_DIR = Path(__file__).parent.parent / 'sec-edgar-filings'

def extract_text_from_filing(file_path):
    """Extract readable text from SEC filing"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        if len(content) < 500:
            return None
        
        lines = content.split('\n')
        text_lines = []
        in_text_section = False
        
        for i, line in enumerate(lines):
            line_stripped = line.strip()
            
            if line_stripped.startswith('<FILENAME>') or line_stripped.startswith('<IMS-HEADER>'):
                in_text_section = True
                continue
            
            if in_text_section and len(line_stripped) > 0:
                if not line_stripped.startswith('<') and not line_stripped.startswith('ACCESSION') and not line_stripped.startswith('CIK'):
                    if any(kw in line_stripped.upper() for kw in ['RISK', 'ITEM 1', 'ITEM 7', 'MANAGEMENT', 'GOVERNANCE', 'ENVIRONMENTAL', 'SUSTAINABILITY', 'ESG', 'SOCIAL']):
                        text_lines.append(line_stripped)
        
        combined_text = ' '.join(text_lines[:2000])
        
        if combined_text and len(combined_text) > 500:
            combined_text = re.sub(r'<[^>]+>', ' ', combined_text)
            combined_text = re.sub(r'\s+', ' ', combined_text)
            return combined_text.strip()
        
        return None
        
    except Exception as e:
        logger.warning(f'Error reading filing {file_path}: {e}')
        return None

def load_sec_filings():
    """Load real SEC 10-K filings from downloaded data"""
    documents = []
    
    if not SEC_EDGAR_DIR.exists():
        logger.warning(f'SEC EDGAR directory not found: {SEC_EDGAR_DIR}')
        return pd.DataFrame()
    
    company_mappings = {
        'AAPL': ('0000320193', 'Apple Inc', 'Technology'),
        'MSFT': ('0000789019', 'Microsoft Corp', 'Technology'),
        'GOOG': ('0001652044', 'Alphabet Inc', 'Technology'),
        'AMZN': ('0001018724', 'Amazon.com Inc', 'Consumer'),
        'JPM': ('0000019617', 'JPMorgan Chase', 'Finance'),
    }
    
    for ticker, (cik, company_name, sector) in company_mappings.items():
        ticker_dir = SEC_EDGAR_DIR / ticker / '10-K'
        
        if not ticker_dir.exists():
            logger.debug(f'No 10-K filings found for {ticker}')
            continue
        
        for filing_dir in ticker_dir.iterdir():
            if not filing_dir.is_dir():
                continue
            
            filing_file = filing_dir / 'full-submission.txt'
            if not filing_file.exists():
                continue
            
            text = extract_text_from_filing(filing_file)
            if not text or len(text) < 500:
                continue
            
            accession = filing_dir.name
            year_part = accession.split('-')[1] if '-' in accession else '22'
            year = int(year_part)
            if year < 50:
                year += 2000
            else:
                year += 1900
            
            documents.append({
                'ticker': ticker,
                'cik': cik,
                'company_name': company_name,
                'sector': sector,
                'year': year,
                'combined_text': text,
                'accession_number': accession,
                'filing_date': f'{year}-03-15',
                'source': 'SEC_EDGAR'
            })
    
    logger.info(f'Loaded {len(documents)} SEC 10-K filings')
    
    return pd.DataFrame(documents) if documents else pd.DataFrame()

def augment_with_synthetic_companies(df_real, num_total=500):
    """Augment real SEC data with synthetic companies"""
    real_companies = df_real['ticker'].nunique() if len(df_real) > 0 else 0
    synthetic_needed = num_total - real_companies
    
    if synthetic_needed <= 0:
        return df_real
    
    synthetic_docs = []
    
    for i in range(1, synthetic_needed + 1):
        ticker = f'SYM{i:03d}'
        cik = f'{10000000+i:010d}'
        company_name = f'Synthetic Company {i}'
        
        for year in [2022, 2023, 2024]:
            text = f"""FORM 10-K for {company_name}. 
            Risk factors include environmental sustainability, 
            social responsibility, employee diversity, governance practices.
            Discussion of climate change impacts, supply chain resilience,
            board independence and executive compensation policies."""
            
            synthetic_docs.append({
                'ticker': ticker,
                'cik': cik,
                'company_name': company_name,
                'sector': 'Other',
                'year': year,
                'combined_text': text,
                'accession_number': f'SYNTH-{year}-{i:05d}',
                'filing_date': f'{year}-03-15',
                'source': 'SYNTHETIC'
            })
    
    df_synthetic = pd.DataFrame(synthetic_docs)
    
    if len(df_real) > 0:
        return pd.concat([df_real, df_synthetic], ignore_index=True)
    else:
        return df_synthetic
