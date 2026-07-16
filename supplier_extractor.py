import os
import json
import logging
from openai import OpenAI

EXTRACTION_MODEL = "deepseek-v4-flash"
EXTRACTION_BASE_URL = "https://api.deepseek.com/v1"
PROCESSOR_TITLE_FIELD = "supplier_name"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_from_csv(csv_content: str) -> dict:
    try:
        api_key = os.environ.get("DEEPSEEK_API_KEY")
        if not api_key:
            logger.error("DEEPSEEK_API_KEY not set")
            return {"supplier_name": "", "items": []}
        client = OpenAI(api_key=api_key, base_url=EXTRACTION_BASE_URL)
        prompt = f"""Extract structured data from this supplier price list CSV. The CSV has columns: supplier_name,item,price.
Return JSON with keys: "{PROCESSOR_TITLE_FIELD}" (string, the supplier name from the supplier_name column), "items" (list of objects with "item" string and "price" float).
CSV content:
{csv_content}"""
        response = client.chat.completions.create(
            model=EXTRACTION_MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        content = response.choices[0].message.content
        parsed = json.loads(content)
        if PROCESSOR_TITLE_FIELD not in parsed:
            parsed[PROCESSOR_TITLE_FIELD] = ""
        if "items" not in parsed:
            parsed["items"] = []
        for item in parsed.get("items", []):
            if "price" in item:
                try:
                    item["price"] = float(item["price"])
                except (ValueError, TypeError):
                    item["price"] = 0.0
        return parsed
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        return {"supplier_name": "", "items": []}
