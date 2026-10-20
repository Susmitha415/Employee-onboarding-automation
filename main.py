import csv
import logging
from pathlib import Path

from validator import validate_employee
from template_processor import populate_template
from file_manager import create_employee_file

#Project directories

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "employees.csv"
TEMPLATE_FILE = BASE_DIR / "templates" / "onboarding_template.txt"
OUTPUT_DIR = BASE_DIR / "output"
REPORT_DIR = BASE_DIR / "reports"
LOG_DIR = BASE_DIR / "logs"

def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOG_DIR / "onboarding.log"
    logging.basicConfig(
        filename=str(log_file),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
        force=True,
    )

def main():
    setup_logging()
    logging.info("Employee onboarding process started")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists():
        logging.error("CSV file not found: %s", DATA_FILE)
        print(f"CSV file not found: {DATA_FILE}")
        return

    if not TEMPLATE_FILE.exists():
        logging.error("Template file not found: %s", TEMPLATE_FILE)
        print(f"Template file not found: {TEMPLATE_FILE}")
        return

    with TEMPLATE_FILE.open("r", encoding="utf-8") as file:
        template_text = file.read()

    seen_ids = set()
    valid_count = 0
    invalid_count = 0
    report_lines = []

    with DATA_FILE.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)

        for row_number, record in enumerate(reader, start=2):
            employee, errors = validate_employee(record, seen_ids)

            if errors:
                invalid_count += 1
                message = (
                    f"Row {row_number}: "
                    f"{', '.join(errors)}"
                )
                report_lines.append(message)
                logging.warning(message)
                continue

            try:
                content = populate_template(
                    template_text, employee
                )

                output_file = create_employee_file(
                    OUTPUT_DIR, employee, content
                )

                valid_count += 1
                message = (
                    f"Row {row_number}: Generated {output_file}"
                )
                report_lines.append(message)
                logging.info(message)

            except (OSError, ValueError) as error:
                invalid_count += 1
                message = f"Row {row_number}: Processing failed: {error}"
                report_lines.append(message)
                logging.exception(message)

    summary = [
        "EMPLOYEE ONBOARDING PROCESSING SUMMARY",
        "======================================",
        f"Successfully processed: {valid_count}",
        f"Invalid or failed records: {invalid_count}",
        "",
        *report_lines,
    ]

    report_file = REPORT_DIR / "processing_summary.txt"
    report_file.write_text(
        "\n".join(summary), encoding="utf-8"
    )
    logging.info("Processing summary saved to: %s", report_file)
    print("\n".join(summary))
    print(f"\nSummary saved to: {report_file}")
    print(f"Log saved to: {LOG_DIR / 'onboarding.log'}")
    logging.info(
        "Employee onboarding process completed. Sucessful:%s,Failed:%s",
        valid_count,
        invalid_count
    )
if __name__ == "__main__":
    main()

