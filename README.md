# Multi-Supplier Price List Ingestion & Variance Alert Tool

**Archetype:** extraction

This tool ingests CSV supplier price lists, extracts structured item/price data using DeepSeek, compares them against a master baseline, and generates status records with variance details.

## How It Works

1. `supplier_extractor.py` – calls DeepSeek API to parse raw CSV content into a supplier name and items list.
2. `price_comparator.py` – compares extracted prices against master baseline, returns status and variance list.
3. `poller.py` – orchestrates reading a CSV file, extracting data, comparing, and writing output JSON.

## Inputs

- **CSV file** (supplier price list) with columns: `supplier_name,item,price`.
- **Master JSON file** – flat dict mapping item names to baseline prices, e.g. `{"WidgetA": 5.0, "GadgetB": 12.0}`.

## Output

JSON status record containing:
- `title` – supplier name
- `status` – one of:
  - `above_threshold:critical`
  - `within_threshold:good`
- `variances` – list of items with price details

## Installation

```bash
pip install -r requirements.txt
```

Set your DeepSeek API key:

```bash
export DEEPSEEK_API_KEY="sk-your-key"
```

## Run Demo

```bash
python3 run_demo.py
```

This runs a hardcoded end-to-end demo with no arguments (takes <10s, exits 0).

## Run Tests

```bash
python3 run_tests.py
```

## Dashboard Status Values

- `above_threshold:critical` – at least one item exceeds variance threshold (10%) or is missing from master.
- `within_threshold:good` – all known items within threshold and no missing items.

## Usage in Production

Call `poller.process_file(csv_path, master_path, output_path)` from your own scripts or orchestration.
