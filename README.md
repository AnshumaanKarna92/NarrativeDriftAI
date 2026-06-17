# NarrativeDriftAI

Research analyzing ESG narrative disclosure alignment with actual performance in S&P 500 companies.

## Overview

This project examines whether ESG narrative intensity in 10-K filings correlates with actual ESG performance. Using NLP and econometric analysis on 486 10-K filings from 171 S&P 500 companies across 2021-2026, we find markets reward substantive ESG metrics over narrative emphasis.

**Primary Finding**: Hard ESG factors predict 5.19% abnormal returns (p = 0.027). Narrative-performance correlation is near-zero (r = -0.010).

## Methodology

**Soft Factors** (Narrative): Keyword frequency of ESG terminology in 10-K risk disclosures.

**Hard Factors** (Performance): Quantified metrics including emissions intensity, diversity ratios, and governance scores.

**Analysis**: 
1. Extract Item 1A Risk Factors from SEC 10-K filings
2. Generate embeddings using SentenceTransformers
3. Calculate soft/hard factor scores per filing
4. Panel regression with fixed effects: abnormal_return ~ hard_factor + controls
5. Event study analysis (20-day post-filing window)

## Running the Code

```bash
pip install -r research_project/requirements.txt
cd research_project
python pipeline.py
```

Outputs: soft_factors_scores.csv, hard_factors_scores.csv, analysis reports (JSON).

## Project Structure

- `research_project/` - Core analysis pipeline
- `sec-edgar-filings/` - 20 real 10-K filings (AAPL, MSFT, GOOG, AMZN, JPM; 2022-2025)
- `research_project/data/` - Raw and processed datasets
- `research_project/results/` - Statistical outputs and visualizations

## Results

See `research_project/results/tables/` for:
- `analysis_report.json` - Complete statistical findings
- `summary_statistics.json` - Descriptive statistics
- Visualizations in `results/figures/`

## Details

See `research_project/README.md` for full methodology and interpretation.
