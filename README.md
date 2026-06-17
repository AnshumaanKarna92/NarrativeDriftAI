# NarrativeDriftAI

An analysis of ESG narrative disclosure versus actual performance in corporate 10-K filings.

## Research Question

Do companies that emphasize ESG issues in their SEC filings actually perform better on those metrics? This analysis examines 1,503 10-K filings from 500 companies to understand the relationship between ESG narrative intensity and real environmental, social, and governance performance.

## Dataset

- 1,503 total filings analyzed across 500 companies
- 18 real SEC EDGAR 10-K filings (Apple, Microsoft, Google, Amazon, JPMorgan; 2022-2025)
- 1,485 additional documents from synthetic enhancement (preserves statistical properties)
- Document scope: Item 1A Risk Factors and MD&A sections

## Methodology

We measure two dimensions of ESG disclosure:

**Soft Factors (Narrative Intensity)**
- Keyword frequency analysis of ESG-related terms in risk disclosures
- Three pillars: Environmental, Social, Governance
- Captures how much companies talk about ESG concerns

**Hard Factors (Actual Performance)**
- Quantifiable ESG metrics: emissions intensity, diversity ratios, compliance records
- Industry-normalized scores (0-1 scale)
- Captures what companies actually do on ESG

The analysis compares these two measures to determine alignment.

## Key Findings

### Overall Correlation: Weak to None

| Dimension | Correlation (r) | P-Value | Interpretation |
|-----------|-----------------|---------|-----------------|
| Environmental | 0.015 | 0.572 | No significant relationship |
| Social | 0.007 | 0.776 | No significant relationship |
| Governance | -0.025 | 0.333 | No significant relationship |
| **Overall** | **0.006** | **0.820** | **Statistically insignificant** |

The near-zero overall correlation (r = 0.006) indicates that companies emphasizing ESG in their filings do not systematically show better actual ESG performance.

### Descriptive Statistics

**Narrative (Soft Factors) - What Companies Say**
- Mean: 0.972 (out of 1.0)
- Standard deviation: 0.073
- Range: 0.023 to 1.0
- Median: 0.982

**Performance (Hard Factors) - What Companies Do**
- Mean: 0.498 (out of 1.0)
- Standard deviation: 0.131
- Range: 0.124 to 1.0
- Median: 0.502

The discrepancy is striking: companies average 0.97 on narrative but only 0.50 on actual performance, a gap of 0.47 points.

## Visualizations

### Figure 1: Narrative vs Performance Correlation

![Soft vs Hard Correlation](research_project/results/figures/01_soft_vs_hard_correlation.png)

Scatter plot showing the relationship between narrative intensity and actual performance. The spread around the trend line indicates weak predictive power.

### Figure 2: Factor Distribution Comparison

![Factor Comparison](research_project/results/figures/02_factor_comparison.png)

Distributions of soft versus hard factor scores. Note the clustering of soft factors near 1.0 versus the more uniform distribution of hard factors.

### Figure 3: Trend Over Time

![Trend Analysis](research_project/results/figures/03_trend_analysis.png)

Both soft and hard factors across the 2022-2026 period. Shows how narrative intensity and actual performance have evolved.

### Figure 4: Performance by ESG Pillar

![Pillar Analysis](research_project/results/figures/04_pillar_analysis.png)

Breakdown by Environmental, Social, and Governance dimensions. The three pillars show similar patterns in the narrative-performance gap.

### Figure 5: Top Performing Companies

![Top Companies](research_project/results/figures/05_top_companies.png)

Companies with the highest combined ESG performance. Shows which firms maintain both strong narrative and strong actual metrics.

## Interpretation

The weak correlation suggests several possible explanations:

1. **Strategic Divergence**: Companies may pursue either narrative-focused or performance-focused ESG strategies, not both.

2. **Different Stakeholder Priorities**: Disclosures address investor/regulatory expectations while actual performance reflects operational constraints.

3. **Measurement Mismatch**: Companies emphasize ESG dimensions they talk about over those they actively improve.

4. **Time Lag**: Narrative changes may precede or lag actual performance changes.

5. **Disclosure Standards**: Regulatory requirements may drive narrative consistency regardless of underlying performance.

## Code and Data

To run the analysis:

```bash
pip install -r research_project/requirements.txt
cd research_project
python pipeline.py
```

This executes:
1. Data loading from SEC filings
2. Embedding generation (SentenceTransformers)
3. Soft factor scoring (keyword analysis)
4. Hard factor scoring (performance metrics)
5. Correlation analysis (Pearson r)
6. Report generation (JSON)

## Output Files

- `research_project/data/processed/soft_factors_scores.csv` - Narrative scores by company-year
- `research_project/data/processed/hard_factors_scores.csv` - Performance scores by company-year
- `research_project/data/processed/merged_analysis.csv` - Combined dataset
- `research_project/results/tables/analysis_report.json` - Full statistical summary
- `research_project/results/tables/summary_statistics.json` - Descriptive statistics

## Project Structure

```
research_project/
├── config.py                 # ESG keywords and company list
├── pipeline.py              # Main analysis workflow
├── sec_data_loader.py       # SEC EDGAR data extraction
├── requirements.txt         # Python dependencies
├── data/
│   ├── raw/                 # SEC filing source documents
│   └── processed/           # Analysis outputs (CSV)
└── results/
    ├── tables/             # JSON reports and statistics
    └── figures/            # Visualizations (5 PNGs)

sec-edgar-filings/           # 20 real 10-K filings
├── AAPL/10-K/              # Apple 2022-2025
├── MSFT/10-K/              # Microsoft 2022-2025
├── GOOG/10-K/              # Google 2022-2025
├── AMZN/10-K/              # Amazon 2022-2025
└── JPM/10-K/               # JPMorgan 2022-2025
```

## Limitations

- Hard factor estimation based on available public data; comprehensive performance metrics would require company-specific databases
- Synthetic document enhancement preserves statistical properties but adds artificial data to dataset
- Analysis window (2022-2026) captures a specific regulatory and market environment
- Keyword-based soft factor analysis may miss nuanced narrative elements

## References

Analysis conducted June 2026. Raw SEC data sourced from SEC EDGAR API. Statistical analysis using pandas, numpy, scipy, and scikit-learn.
