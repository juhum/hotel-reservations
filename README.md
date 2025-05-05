```markdown
# Hotel Reservation System – YAML Data Processing, JSON Schema Validation, MongoDB Import, and Analysis

## Technologies and Libraries
- **Python 3.11+**
- **PyYAML** – YAML data processing
- **jsonschema** – JSON Schema validation
- **pymongo** – MongoDB integration
- **pandas** – CSV/HTML export (optional)
- **MongoDB** – NoSQL database for hotels, guests, and reservations
- **seaborn** – data visualization
- **os** – environment variables
- **python-dotenv** – load configuration from `.env`
- **datetime** – date/time handling
- **Jupyter Notebook** – data analysis and visualization

## Project Goals
- Maintain input data in YAML for readability and ease of editing.
- Validate data using JSON Schema.
- Convert YAML data to JSON format.
- Store and process data in MongoDB.
- Export data to CSV/HTML.
- Analyze data using Jupyter Notebook.

## Data Processing Architecture
**YAML → JSON → JSON Schema Validation → MongoDB / CSV / HTML / Analysis**

## Data Structure
### `hotels`
- `name`: Hotel name (e.g., "Hotel Giewont")
- `location`: Location (e.g., "Zakopane")
- `stars`: Star rating (1-5)
- `rooms`: 
  - `number`: Room number (e.g., 101)
  - `type`: Room type (e.g., "double")
  - `price`: Price per night (e.g., 400)
  - `available`: Availability status (`true`/`false`)

### `guests`
- `first_name`: Guest's first name (e.g., "Anna")
- `last_name`: Guest's last name (e.g., "Nowak")
- `email`: Contact email (e.g., "anna.nowak@example.com")
- `phone`: Phone number (e.g., "+48600100200")

### `reservations`
- `guest_email`: Guest's email (links to `guests`)
- `room_number`: Room number (links to `hotels.rooms`)
- `hotel_name`: Hotel name (links to `hotels`)
- `start_date`: Reservation start date (e.g., "2025-06-01")
- `end_date`: Reservation end date (e.g., "2025-06-07")
- `status`: Reservation status (e.g., "confirmed")

---

## Project Structure
### Root Directory
- `README.md`: Project documentation.
- `.gitignore`: Files/packages ignored by Git.
- `example.env`: Example environment configuration.
- `requirements.txt`: Required dependencies.

### `data/`
- **`processed/`**:
  - `export_guests.html`: Guests data in HTML.
  - `export_reservations.csv`: Reservations in CSV.
  - `export_rooms.csv`: Room details in CSV.
  - `json_export.json`, `json_output.json`: JSON data exports.
  - `yaml_export.yaml`: YAML data export.
- **`raw/`**:
  - `example_data.json`, `example_data.yaml`: Sample data.
  - `hotel_data.yaml`: Raw hotel data in YAML.

### `schema/`
- `hotel_reservation_schema.json`: JSON Schema for validation.

### `notebook/`
- `hotel_analysis.ipynb`: Jupyter Notebook for analysis and visualization.

### `scripts/`
- **`database/`**:
  - `export_from_mongodb.py`: Export data from MongoDB.
  - `import_to_mongodb.py`: Import data to MongoDB.
- **`export/`**:
  - `export_to_csv_html.py`: Generate CSV/HTML exports.
  - `validate_and_convert.py`: Validate and convert YAML to JSON.
- **`sql/`**:
  - `queries.sql`: SQL queries for the project.
- `queries.py`: MongoDB queries in Python.

---

## Data Validation
**Script**: `validate_and_convert.py`
1. Load YAML data.
2. Validate against `hotel_reservation_schema.json`.
3. Convert validated data to `json_output.json`.

## Data Import
**Script**: `import_to_mongodb.py`
- Clears existing data and imports `json_output.json` into MongoDB collections:
  - `hotels`
  - `guests`
  - `reservations`

## Data Export
**Script**: `export_to_csv_html.py`
- Generates:
  - `export_reservations.csv`
  - `export_rooms.csv`
  - `export_guests.html`

## Analysis and Visualization
**Notebook**: `hotel_analysis.ipynb`
- **Charts**:
  - Reservations by status.
  - Average room price per hotel.
  - Room availability across hotels.

## Example Queries
### MongoDB (`queries.py`)
- List available rooms.
- Average room price per hotel.
- Reservations for a specific guest.
- Reservation status statistics.
- Room availability per hotel.

### SQL (`queries.sql`)
- Similar queries for SQL-based analysis.

---

## Usage Example
1. **Start MongoDB**.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure `.env` with `MONGO_URI` and `DB_NAME`.
4. Validate and convert data:
   ```bash
   python scripts/export/validate_and_convert.py
   ```
5. Import data to MongoDB:
   ```bash
   python scripts/database/import_to_mongodb.py
   ```
6. Run queries using `queries.py` or `queries.sql`.
7. Export data to CSV/HTML:
   ```bash
   python scripts/export/export_to_csv_html.py
   ```
8. Analyze data in `hotel_analysis.ipynb`.
9. Export MongoDB data to JSON/YAML:
   ```bash
   python scripts/database/export_from_mongodb.py
   ```

---

## Key Takeaways
- **YAML** simplifies input data editing.
- **JSON Schema** ensures data integrity.
- **MongoDB** enables flexible storage and fast querying.
- The project is scalable and ready for expansion.
```