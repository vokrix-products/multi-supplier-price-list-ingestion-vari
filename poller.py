import json
import logging
from supplier_extractor import extract_from_csv
from price_comparator import compare_prices

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_file(csv_path: str, master_path: str, output_path: str | None = None) -> dict:
    with open(csv_path, 'r') as f:
        raw_content = f.read()
    extracted = extract_from_csv(raw_content)
    supplier_name = extracted.get("supplier_name", "")
    items = extracted.get("items", [])
    for item in items:
        item["supplier_name"] = supplier_name
    with open(master_path, 'r') as f:
        master_prices = json.load(f)
    record = compare_prices(items, master_prices)
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(record, f, indent=2)
    return record
