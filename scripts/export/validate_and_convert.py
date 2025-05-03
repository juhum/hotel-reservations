import yaml
import json
import datetime
from jsonschema import validate, ValidationError

def convert_dates(obj):
    if isinstance(obj, dict):
        return {k: convert_dates(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_dates(item) for item in obj]
    elif isinstance(obj, datetime.date):
        return obj.isoformat()
    else:
        return obj

# Wczytanie YAML
with open("data/raw/hotel_data.yaml", "r", encoding="utf-8") as file:
    yaml_data = yaml.safe_load(file)

# Konwersja dat na stringi ISO
yaml_data = convert_dates(yaml_data)

# Wczytanie JSON Schema
with open("data/schema/hotel_reservation_schema.json", "r", encoding="utf-8") as file:
    schema = json.load(file)

# Walidacja
try:
    validate(instance=yaml_data, schema=schema)
    print("✅ YAML poprawnie zwalidowany!")
except ValidationError as e:
    print("❌ Błąd walidacji:")
    print(e)

# Zapis do JSON
with open("data/processed/json_output.json", "w", encoding="utf-8") as file:
    json.dump(yaml_data, file, indent=2, ensure_ascii=False)
