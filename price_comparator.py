STATUS_ABOVE_THRESHOLD = "above_threshold:critical"
STATUS_WITHIN_THRESHOLD = "within_threshold:good"
VARIANCE_THRESHOLD = 0.1
PROCESSOR_TITLE_FIELD = "supplier_name"

def compare_prices(supplier_items: list[dict], master_prices: dict[str, float], threshold: float = VARIANCE_THRESHOLD) -> dict:
    title = ""
    variances = []
    overall_critical = False

    for item in supplier_items:
        supplier_name = item.get(PROCESSOR_TITLE_FIELD, "")
        if supplier_name and not title:
            title = supplier_name
        item_name = item.get("item", "")
        supplier_price = item.get("price", 0.0)
        if item_name in master_prices:
            master_price = master_prices[item_name]
            diff_percent = abs(supplier_price - master_price) / master_price if master_price != 0 else None
            if diff_percent is not None and diff_percent > threshold:
                overall_critical = True
        else:
            master_price = None
            diff_percent = None
            overall_critical = True
        variances.append({
            "item": item_name,
            "supplier_price": supplier_price,
            "master_price": master_price,
            "diff_percent": diff_percent
        })

    status = STATUS_ABOVE_THRESHOLD if overall_critical else STATUS_WITHIN_THRESHOLD
    return {
        "title": title,
        "status": status,
        "variances": variances
    }
