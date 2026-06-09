import requests
from datetime import datetime


def fetch_sample_data():
    """Fetch sample data from a public API using requests."""
    url = "https://jsonplaceholder.typicode.com/posts/1"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json()


def generate_log(entries):
    """Write a list of text entries to a dated log file."""
    if not isinstance(entries, list):
        raise ValueError("entries must be a list")

    filename = f"log_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(filename, "w", encoding="utf-8") as fh:
        for entry in entries:
            fh.write(f"{entry}\n")

    print(f"Log written to {filename}")
    return filename


if __name__ == "__main__":
    post = fetch_sample_data()
    log_entries = [
        f"Fetched post ID: {post.get('id')}",
        f"Title: {post.get('title')}",
        f"Body: {post.get('body')}",
    ]
    generate_log(log_entries)
