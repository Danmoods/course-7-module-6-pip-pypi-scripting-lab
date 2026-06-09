from datetime import datetime
import os

def generate_log(data):
    # Validate input
    if not isinstance(data, list):
        raise ValueError("data must be a list")

    # Generate filename for today's date
    today = datetime.now().strftime("%Y%m%d")
    filename = f"log_{today}.txt"

    # Write entries to file (one per line). For empty list, create empty file.
    with open(filename, "w", encoding="utf-8") as fh:
        for entry in data:
            fh.write(f"{entry}\n")

    # Print confirmation and return filename for callers/tests
    print(f"Log written to {filename}")
    return filename
