import os
import re
import requests
import pandas as pd
from datetime import datetime
import time
from bs4 import BeautifulSoup

TICKER_SOURCE_PATH = r"C:\Users\surji\Desktop\Quant_Poject\2000_stocks_srapping_(API)\Data\Stock List.xlsx"
DOWNLOAD_DIR = r"C:\Users\surji\Desktop\Quant_Poject\Downloaded Filings"
USER_AGENT = "MyAppName your_email@example.com"
TICKER_COLUMN = "Ticker" 
OUTPUT_FILE = os.path.join(DOWNLOAD_DIR, "Parsed_DATA.xlsx")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

TARGET_VARIANTS = {
    # Assets
    "Current Assets": [
        "current assets", "total current assets", "current assets total"
    ],
    "Non-Current Assets": [
        "non-current assets", "non current assets", "long-term assets", "long term assets",
        "noncurrent assets", "total non-current assets", "total long-term assets", 
        "total long term assets", "total noncurrent assets"
    ],
    "Total Assets": [
        "total assets", "assets total", "total consolidated assets"
    ],
    "Cash and Cash Equivalents": [
        "cash and cash equivalents", "cash and equivalents", "cash & cash equivalents",
        "cash, cash equivalents, and short-term investments",
        "cash, cash equivalents and short-term investments",
        "cash and short-term investments", "cash & short-term investments"
    ],
    "Property, Plant, and Equipment (Net)": [
        "property and equipment, net", "property, plant and equipment, net",
        "property, plant & equipment, net", "property plant and equipment net",
        "pp&e", "ppe", "property and equipment net", "plant and equipment net",
        "property plant equipment net", "fixed assets net"
    ],
    "Goodwill": [
        "goodwill", "goodwill net", "goodwill and intangible assets"
    ],
    "Intangible Assets": [
        "intangible assets, net", "intangible assets net", "other intangible assets",
        "acquired intangible assets", "intangible assets", "intangibles net"
    ],
    "Accounts Receivable": [
        "accounts receivable", "accounts receivable net", "trade receivables", 
        "receivables", "trade and other receivables", "accounts receivable, net"
    ],
    "Inventory": [
        "inventory", "inventories", "finished goods", "raw materials",
        "inventory net", "total inventory"
    ],

    # Liabilities
    "Current Liabilities": [
        "current liabilities", "total current liabilities", "current liabilities total"
    ],
    "Non-Current Liabilities": [
        "non-current liabilities", "non current liabilities", "long term liabilities",
        "noncurrent liabilities", "total non-current liabilities", 
        "total long-term liabilities", "other long-term liabilities",
        "long-term liabilities", "total noncurrent liabilities"
    ],
    "Total Liabilities": [
        "total liabilities", "liabilities total", "total consolidated liabilities"
    ],
    "Short-Term Debt": [
        "short-term debt", "short term debt", "current portion of long-term debt",
        "current debt", "current borrowings", "short-term borrowings",
        "current portion of debt", "debt due within one year"
    ],
    "Long-Term Debt": [
        "long-term debt", "long term debt", "long-term borrowings",
        "long-term obligations", "noncurrent debt", "debt securities",
        "long-term debt securities", "term debt"
    ],
    "Accounts Payable": [
        "accounts payable", "trade payables", "accounts payable and accrued liabilities",
        "trade and other payables"
    ],
    "Total Debt": [
        "total debt", "total borrowings", "total debt securities"
    ],

    # Equity
    "Total Equity": [
        "total stockholders' equity", "total shareholders' equity", "total equity",
        "stockholders' equity", "shareholders' equity", "total shareholders equity",
        "total stockholders equity", "stockholders equity", "shareholders equity"
    ],
    "Treasury Stock": [
        "treasury stock", "treasury shares", "shares held in treasury"
    ],
    "Retained Earnings": [
        "retained earnings", "accumulated deficit", "accumulated earnings",
        "retained earnings (accumulated deficit)"
    ],
    "Preferred Stock": [
        "preferred stock", "preference shares", "preferred shares"
    ],
    "Common Shares Outstanding": [
        "common shares outstanding", "common stock outstanding", "ordinary shares outstanding",
        "common stock and paid-in capital", "common stock", "ordinary shares"
    ],
    "Book Value of Equity": [
        "book value of equity", "stockholders equity", "net worth"
    ],
    "Accumulated Other Comprehensive Income": [
        "accumulated other comprehensive income", "accumulated other comprehensive loss",
        "accumulated other comprehensive income (loss)", "aoci"
    ],

    # Income Statement
    "Revenue": [
        "total revenue", "revenue", "net revenue", "net sales", "total net sales",
        "sales", "total sales", "operating revenue", "service revenue"
    ],
    "Cost of Revenue": [
        "cost of revenue", "cost of sales", "cost of goods sold", "cogs",
        "cost of services", "cost of products sold"
    ],
    "Gross Profit": [
        "gross margin", "gross profit", "gross income"
    ],
    "Operating Income (EBIT)": [
        "operating income", "income from operations", "operating profit",
        "earnings before interest and taxes", "ebit", "operating earnings"
    ],
    "Net Income": [
        "net income", "net earnings", "net income (loss)", "net profit",
        "profit for the year", "profit attributable to shareholders"
    ],
    "Research and Development Expense": [
        "research and development", "r&d expense", "research and development expense",
        "research and development costs"
    ],
    "Income Before Tax": [
        "income before income taxes", "income before tax", "earnings before tax",
        "profit before tax", "income before provision for income taxes"
    ],
    "Income Tax Expense": [
        "provision for income taxes", "income tax expense", "income taxes",
        "tax expense", "income tax provision"
    ],
    "Comprehensive Income": [
        "comprehensive income", "total comprehensive income", "comprehensive earnings"
    ],

    # Cash Flow
    "Operating Cash Flow": [
        "net cash from operations", "net cash provided by operating activities",
        "operating cash flow", "cash flows from operating activities",
        "net cash from operating activities"
    ],
    "Capital Expenditures (CapEx)": [
        "additions to property and equipment", "purchases of property and equipment",
        "capital expenditures", "capex", "capital investments", "capital additions"
    ],
    "Depreciation & Amortization": [
        "depreciation, amortization, and other", "depreciation and amortization",
        "amortization", "depreciation", "depreciation expense"
    ],
    "Free Cash Flow": [
        "free cash flow", "cash flow from operations less capex"
    ],
    "NOPAT": [
        "nopat", "net operating profit after tax", "net operating profit"
    ]
}

EXCLUSION_PATTERNS = {
    "Total Assets": ["deferred tax assets", "other assets", "current assets", "non-current assets"],
    "Total Liabilities": ["deferred tax liabilities", "other liabilities", "current liabilities", "non-current liabilities"],
    "Total Equity": ["stockholders' deficit", "shareholders' deficit", "equity method"],
    "Revenue": ["deferred revenue", "unearned revenue", "other revenue"],
    "Net Income": ["other comprehensive income", "loss", "deficit"],
    "Operating Income (EBIT)": ["non-operating income", "other income"],
    "Cash and Cash Equivalents": ["restricted cash", "cash flows"],
    "Current Assets": ["non-current assets", "total assets"],
    "Current Liabilities": ["non-current liabilities", "total liabilities"],
    "Short-Term Debt": ["long-term debt", "total debt"],
    "Long-Term Debt": ["short-term debt", "current portion"],
    "Comprehensive Income": ["other comprehensive income", "accumulated other comprehensive"]
}


def read_tickers_from_excel(path, column_name):
    df = pd.read_excel(path)
    return df[column_name].dropna().unique().tolist()
TICKERS = read_tickers_from_excel(TICKER_SOURCE_PATH, TICKER_COLUMN)
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

def get_cik_mapping():
    url = "https://www.sec.gov/files/company_tickers.json"
    resp = requests.get(url, headers={'User-Agent': USER_AGENT})
    resp.raise_for_status()
    data = resp.json()
    df = pd.DataFrame.from_dict(data, orient='index')
    df['ticker'] = df['ticker'].str.upper()
    df['cik_str'] = df['cik_str'].apply(lambda x: str(x).zfill(10))
    return df

def find_cik(ticker, cik_df):
    ticker_norm = ticker.replace('.', '-').upper()
    row = cik_df[cik_df['ticker'] == ticker_norm]
    if not row.empty:
        return row.iloc[0]['cik_str'], row.iloc[0]['title']

    row = cik_df[cik_df['ticker'] == ticker.upper()]
    if not row.empty:
        return row.iloc[0]['cik_str'], row.iloc[0]['title']
    
    partial_matches = cik_df[cik_df['ticker'].str.startswith(ticker.split('.')[0].upper())]
    if not partial_matches.empty:
        best_row = partial_matches.iloc[0]
        print(f"\u26a0\ufe0f Auto-fallback matched '{ticker}' → '{best_row['ticker']}' ({best_row['title']})")
        return best_row['cik_str'], best_row['title']

    print(f"\u274c No CIK for {ticker}")
    return None, None

def download_latest_filing(cik):
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    resp = requests.get(url, headers={'User-Agent': USER_AGENT})
    resp.raise_for_status()
    data = resp.json()
    filings = data['filings']['recent']
    
    form_priority = ['10-K', '20-F', '10-Q', '6-K'] 

    for form_type in form_priority:
        for i in range(len(filings['form'])):
            form = filings['form'][i]
            if form == form_type:
                accession = filings['accessionNumber'][i].replace('-', '')
                doc = filings['primaryDocument'][i]
                filing_date = filings['filingDate'][i]
                file_url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession}/{doc}"
                print(f"📥 Downloading {form} on {filing_date}")
                r = requests.get(file_url, headers={'User-Agent': USER_AGENT})
                r.raise_for_status()
                return r.text, form, filing_date
    raise Exception("No suitable filing found")

def save_filing(content, ticker, form, date):
    filename = f"{ticker}_{form}_{date.replace('-', '')}.html"
    path = os.path.join(DOWNLOAD_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path



def clean_text(text):
    if not text:
        return 
    text = text.replace('\xa0', ' ').replace('\n', ' ').replace('\t', ' ')
    text = re.sub(r'\s+', ' ', text) 
    text = text.strip().lower()
    text = re.sub(r'^\$\s*', '', text)  
    text = re.sub(r'\s*\$\s*$', '', text)  
    return text


def extract_numeric(text):
    if not text:
        return None

    text = text.replace(',', '').replace('$', '')
    if '(' in text and ')' in text:
        text = text.replace('(', '-').replace(')', '')
    
    matches = re.findall(r'-?\d+(?:\.\d+)?', text)
    
    if matches:
        try:
            return float(matches[0])
        except ValueError:
            return None
    return None

def is_likely_financial_table(table):
    text = table.get_text().lower()
    financial_indicators = [
        'assets', 'liabilities', 'equity', 'income', 'revenue', 'cash',
        'debt', 'current', 'total', 'million', 'thousand', '$'
    ]
    return sum(indicator in text for indicator in financial_indicators) >= 3

def should_exclude_match(target, cell_text, matched_variant):
    if target not in EXCLUSION_PATTERNS:
        return False
    
    exclusion_patterns = EXCLUSION_PATTERNS[target]
    for pattern in exclusion_patterns:
        if pattern.lower() in cell_text.lower():
            print(f"🚫 Excluding '{cell_text}' for {target} (matches exclusion pattern: '{pattern}')")
            return True
    
    return False

def calculate_match_score(cell_text, variant, target):
    cell_text = cell_text.lower().strip()
    variant = variant.lower().strip()
    
    if cell_text == variant:
        return 100
    
    if should_exclude_match(target, cell_text, variant):
        return 0
    if len(variant.split()) > 1:  # Multi-word targets
        variant_words = set(variant.split())
        cell_words = set(cell_text.split())
        
        extra_words = cell_words - variant_words
        if extra_words:
            specificity_words = {'other', 'foreign', 'unrealized', 'current', 'non-current', 'noncurrent'}
            if extra_words.intersection(specificity_words):
                return 0  # Reject overly specific matches
    
    if variant in cell_text:
        coverage_ratio = len(variant) / len(cell_text)
        base_score = 85 * coverage_ratio
    
        if cell_text.startswith(variant) or cell_text.endswith(variant):
            base_score += 10
            
        return min(base_score, 95)  
    
    elif cell_text in variant:
        coverage_ratio = len(cell_text) / len(variant)
        return 70 * coverage_ratio
    variant_words = set(variant.split())
    cell_words = set(cell_text.split())
    
    common_words = variant_words.intersection(cell_words)
    if common_words:
        word_match_ratio = len(common_words) / len(variant_words)
        return 60 * word_match_ratio
    
    return 0

def find_best_match_in_row(row_cells, target_variants, target_name):
    best_match = None
    best_score = 0
    best_variant = None
    
    for i, cell in enumerate(row_cells):
        cell_text = clean_text(cell.get_text(" ", strip=True))
        
        # Skip empty cells
        if not cell_text:
            continue
        for variant in target_variants:
            score = calculate_match_score(cell_text, variant, target_name)
            
            if score > best_score:
                best_score = score
                best_match = i
                best_variant = variant
    
    return best_match, best_score, best_variant

def extract_value_from_row(row_cells, label_cell_index):
    for i in range(label_cell_index + 1, len(row_cells)):
        text = clean_text(row_cells[i].get_text(" ", strip=True))
        value = extract_numeric(text)
        if value is not None:
            return value

    for i, cell in enumerate(row_cells):
        if i == label_cell_index:
            continue
        text = clean_text(cell.get_text(" ", strip=True))
        if re.search(r'[\d\)$]', text):  
            value = extract_numeric(text)
            if value is not None:
                return value
    return None

def find_hierarchical_matches(table, target, variants):
    rows = table.find_all('tr')
    matches = []

    for row_idx, row in enumerate(rows):
        cells = row.find_all(['td', 'th'])
        if len(cells) < 2:
            continue
        cell_texts = [clean_text(c.get_text(" ", strip=True)) for c in cells]
        row_text_combined = " ".join(cell_texts)
        if any(term in row_text_combined for term in ['continued', 'schedule', 'note']):
            continue

        match_index, score, matched_variant = find_best_match_in_row(cells, variants, target)

        if match_index is not None and score >= 60:
            value = extract_value_from_row(cells, match_index)
            if value is not None:
                matches.append({
                    'row_idx': row_idx,
                    'score': score,
                    'value': value,
                    'label': cells[match_index].get_text(" ", strip=True),
                    'variant': matched_variant
                })

    if not matches:
        return None
        matches.sort(key=lambda x: (x['score'], x['row_idx']), reverse=True)
    best = matches[0]
    print(f"🎯 Best match for {target}: {best['value']} | Label: {best['label']} | Score: {best['score']:.1f}")
    return best['value']



def find_vertical_match(table, target, variants):
    rows = table.find_all('tr')
    if len(rows) < 2:
        return None

    grid = []
    for row in rows:
        cells = row.find_all(['td', 'th'])
        grid.append([clean_text(cell.get_text(" ", strip=True)) for cell in cells])

    num_rows = len(grid)
    num_cols = max(len(row) for row in grid)
    for row in grid:
        while len(row) < num_cols:
            row.append("")

    usd_col_indices = []
    for col_idx in range(num_cols):
        col_text_top = " ".join([grid[i][col_idx] for i in range(min(3, num_rows))])
        if any(curr in col_text_top for curr in ["us$", "usd", "$"]) and "percentage" not in col_text_top:
            usd_col_indices.append(col_idx)

    if not usd_col_indices:
        return None

    best_value = None
    best_score = 0
    for row in grid:
        for label_idx, cell_text in enumerate(row):
            for variant in variants:
                score = calculate_match_score(cell_text, variant, target)
                if score > best_score:
                    for usd_col in usd_col_indices:
                        if usd_col < len(row):
                            candidate = row[usd_col]
                            if "%" in candidate or "percentage" in candidate.lower():
                                continue
                            value = extract_numeric(candidate)
                            if value is not None and value > 100:  # avoid matching percentages
                                best_value = value
                                best_score = score

    if best_value is not None:
        print(f"📈 US$ vertical match for {target}: {best_value}")
    return best_value




def parse_html_precise(filepath):
    with open(filepath, encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')
    
    tables = soup.find_all('table')
    print(f"🔍 Found {len(tables)} tables")

    financial_tables = [t for t in tables if is_likely_financial_table(t)]
    print(f"📊 {len(financial_tables)} tables appear to contain financial data")
    
    found = {key: 'N/A' for key in TARGET_VARIANTS.keys()}
    match_details = {}  
    unique_tables = []
    seen_texts = set()
    for table in financial_tables:
        text = clean_text(table.get_text(" ", strip=True))
        if not text or text in seen_texts:
            continue
        seen_texts.add(text)
        unique_tables.append(table)
    financial_tables = unique_tables
    
    for table_idx, table in enumerate(financial_tables):
        print(f"📋 Processing table {table_idx + 1}")
        for target, variants in TARGET_VARIANTS.items():
            if found[target] != 'N/A':
                continue
            value = find_hierarchical_matches(table, target, variants)

            if value is None:
                value = find_vertical_match(table, target, variants)

            if value is not None:
                found[target] = value
                match_details[target] = {
                    'table': table_idx + 1,
                    'value': value
                }
                print(f"✅ Found {target}: {value}")
    try:
        if found['Total Debt'] == 'N/A':
            short_debt = found.get("Short-Term Debt", 0) if found.get("Short-Term Debt") != 'N/A' else 0
            long_debt = found.get("Long-Term Debt", 0) if found.get("Long-Term Debt") != 'N/A' else 0
            if short_debt != 0 or long_debt != 0:
                found["Total Debt"] = float(short_debt) + float(long_debt)
                print(f"📊 Calculated Total Debt: {found['Total Debt']}")
                
        if found['Free Cash Flow'] == 'N/A':
            ocf = found.get("Operating Cash Flow", 0) if found.get("Operating Cash Flow") != 'N/A' else 0
            capex = found.get("Capital Expenditures (CapEx)", 0) if found.get("Capital Expenditures (CapEx)") != 'N/A' else 0
            if ocf != 0 and capex != 0:
                found["Free Cash Flow"] = float(ocf) - abs(float(capex))  # CapEx is usually negative
                print(f"📊 Calculated Free Cash Flow: {found['Free Cash Flow']}")
                
        if found['Gross Profit'] == 'N/A':
            revenue = found.get("Revenue", 0) if found.get("Revenue") != 'N/A' else 0
            cost_of_revenue = found.get("Cost of Revenue", 0) if found.get("Cost of Revenue") != 'N/A' else 0
            if revenue != 0 and cost_of_revenue != 0:
                found["Gross Profit"] = float(revenue) - float(cost_of_revenue)
                print(f"📊 Calculated Gross Profit: {found['Gross Profit']}")
                
    except Exception as e:
        print(f"⚠️ Error in calculations: {e}")
    
    # Print summary of what was found
    found_count = sum(1 for v in found.values() if v != 'N/A')
    print(f"\n📈 Extracted {found_count}/{len(TARGET_VARIANTS)} financial metrics")
    
    return found

def process_all_tickers():
    cik_df = get_cik_mapping()
    all_data = []

    for ticker in TICKERS:
        print(f"\n📊 Processing {ticker}")
        try:
            cik, company = find_cik(ticker, cik_df)
            if not cik:
                print(f"❌ No CIK for {ticker}")
                continue
            content, form, date = download_latest_filing(cik)
            path = save_filing(content, ticker, form, date)
            data = parse_html_precise(path)

            record = {"Company": company, "Ticker": ticker, "Filing Date": date, "Filing Type": form}
            record.update(data)
            all_data.append(record)
            time.sleep(1)  # respectful delay
        except Exception as e:
            print(f"⚠️ Error for {ticker}: {e}")

    if all_data:
        df = pd.DataFrame(all_data)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file = os.path.join(DOWNLOAD_DIR, f"financials_{timestamp}.xlsx")
        df.to_excel(file, index=False)
        print(f"\n✅ All data saved to: {file}")
        
        # Print comprehensive summary of what was found
        print("\n📈 Comprehensive Extraction Summary:")
        print("=" * 50)
        
        # Group by category
        categories = {
            "Balance Sheet - Assets": ["Current Assets", "Total Assets", "Goodwill", "Intangible Assets", 
                                     "Property, Plant, and Equipment (Net)", "Cash and Cash Equivalents", 
                                     "Accounts Receivable", "Inventory"],
            "Balance Sheet - Liabilities": ["Current Liabilities", "Total Liabilities", "Short-Term Debt", 
                                          "Long-Term Debt", "Total Debt", "Accounts Payable"],
            "Balance Sheet - Equity": ["Total Equity", "Treasury Stock", "Retained Earnings", "Preferred Stock", 
                                     "Common Shares Outstanding", "Book Value of Equity", 
                                     "Accumulated Other Comprehensive Income"],
            "Income Statement": ["Revenue", "Net Income", "Operating Income (EBIT)", "Income Before Tax", 
                               "Income Tax Expense", "Research and Development Expense", "Cost of Revenue", 
                               "Gross Profit", "Comprehensive Income"],
            "Cash Flow Statement": ["Operating Cash Flow", "Capital Expenditures (CapEx)", 
                                  "Depreciation & Amortization", "Free Cash Flow"]
        }
        
        for category, fields in categories.items():
            print(f"\n{category}:")
            found_in_category = 0
            for field in fields:
                if field in TARGET_VARIANTS:
                    found_count = sum(1 for row in all_data if row.get(field) != 'N/A')
                    status = "✅" if found_count > 0 else "❌"
                    print(f"  {status} {field}: {found_count}/{len(all_data)} companies")
                    if found_count > 0:
                        found_in_category += 1
            print(f"  📊 Category Success: {found_in_category}/{len(fields)} fields found")
        
        # Overall statistics
        total_possible = len(TARGET_VARIANTS) * len(all_data)
        total_found = sum(1 for row in all_data for key in TARGET_VARIANTS.keys() if row.get(key) != 'N/A')
        success_rate = (total_found / total_possible) * 100
        print(f"\n🎯 Overall Success Rate: {success_rate:.1f}% ({total_found}/{total_possible} data points)")
        
        # Show companies with most/least data
        company_scores = []
        for row in all_data:
            found_count = sum(1 for key in TARGET_VARIANTS.keys() if row.get(key) != 'N/A')
            company_scores.append((row['Company'], found_count))
        
        company_scores.sort(key=lambda x: x[1], reverse=True)
        print(f"\n🏆 Data Coverage by Company:")
        for company, count in company_scores:
            percentage = (count / len(TARGET_VARIANTS)) * 100
            print(f"  {company}: {count}/{len(TARGET_VARIANTS)} ({percentage:.1f}%)")
        
        print("=" * 50)
    else:
        print("❌ No data extracted")

def append_to_master_excel(new_data, output_file):
    new_df = pd.DataFrame(new_data)
    if os.path.exists(output_file):
        existing_df = pd.read_excel(output_file)
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)
    else:
        combined_df = new_df
    combined_df.to_excel(output_file, index=False)
    print(f"\n✅ Data appended to: {output_file}")

def process_all_tickers():
    cik_df = get_cik_mapping()
    all_data = []

    for ticker in TICKERS:
        print(f"\n📊 Processing {ticker}")
        try:
            cik, company = find_cik(ticker, cik_df)
            if not cik:
                continue
            content, form, date = download_latest_filing(cik)
            path = save_filing(content, ticker, form, date)
            data = parse_html_precise(path)

            record = {"Company": company, "Ticker": ticker, "Filing Date": date, "Filing Type": form}
            record.update(data)
            all_data.append(record)
            time.sleep(1)
        except Exception as e:
            print(f"⚠️ Error for {ticker}: {e}")

    if all_data:
        append_to_master_excel(all_data, OUTPUT_FILE)

if __name__ == "__main__":
    print("🚀 Starting financial data extraction")
    process_all_tickers()


