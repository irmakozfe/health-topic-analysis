# Health Topic Analysis

## Project Overview

This project analyzes health-related news articles from reliable online sources to determine which health topics are most frequently discussed in the media.  
The main goal is to identify and compare data from various web sources using Python-based analytical tools and visualize on a low-code platform. 

RSS feeds were chosen because they provide structured, continuously updated information that can be easily processed and compared.

---

## Data Sources

The following sources were selected for this analysis:

- **Spiegel Gesundheit** – Covers health, nutrition, and mental health topics.  
- **Tagesschau Gesundheit** – National news focusing on healthcare and social issues.  
- **World Health Organization (WHO)** – Provides official global health updates.  
- **Deutsches Ärzteblatt** – Professional medical news focusing on policy and system discussions.

---

## Methodology

- **Data Collection:** RSS feeds fetched automatically using Python (`feedparser`).  
- **Data Cleaning:** Performed with `pandas` to standardize and filter content.  
- **Topic Categorization:** Keyword-based classification into themes such as *Covid*, *Vaccination*, *Depression*, *Addiction*, and *Nutrition*.  
- **Data Export:** Processed results stored as CSV files for further visualization.  
- **Visualization:** Topic and source distribution displayed in **AppSheet**. 

---

## Technologies Used

| Category | Tools |
|-----------|-------|
| Programming | Python |
| Libraries | feedparser, pandas, os, datetime |
| Visualization | AppSheet | Knime | Power BI
| Documentation | LaTeX (Overleaf) |

---

## Output Example

The exported CSV file contains the following columns:

| source | published | topic | title | summary | link |
|--------|------------|--------|--------|----------|------|

