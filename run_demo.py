import json
import tempfile
import os
from poller import process_file

def main():
    csv_content = "supplier_name,item,price\nAcmeCorp,WidgetA,5.50\nAcmeCorp,GadgetB,13.00"
    master_prices = {"WidgetA": 5.0, "GadgetB": 12.0}
    tmp_dir = tempfile.gettempdir()
    csv_path = os.path.join(tmp_dir, "supplier_demo.csv")
    master_path = os.path.join(tmp_dir, "master_demo.json")
    with open(csv_path, 'w') as f:
        f.write(csv_content)
    with open(master_path, 'w') as f:
        json.dump(master_prices, f)
    result = process_file(csv_path, master_path)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
