from pathlib import Path

import requests


DATA_URLS = {
    "closed_2025": (
        "https://seshat.datasd.org/get_it_done_reports/"
        "get_it_done_requests_closed_2025_datasd.csv"
    ),
    "closed_2026": (
        "https://seshat.datasd.org/get_it_done_reports/"
        "get_it_done_requests_closed_2026_datasd.csv"
    ),
    "open_requests": (
        "https://seshat.datasd.org/get_it_done_reports/"
        "get_it_done_requests_open_datasd.csv"
    ),
}

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIRECTORY = PROJECT_ROOT / "data" / "raw"


def download_file(url: str, destination: Path) -> None:
    """Download one file unless it already exists locally."""
    if destination.exists():
        print(f"Skipping existing file: {destination.name}")
        return

    print(f"Downloading: {destination.name}")

    with requests.get(url, stream=True, timeout=120) as response:
        response.raise_for_status()

        with destination.open("wb") as output_file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                output_file.write(chunk)

    print(f"Finished: {destination.name}")


def main() -> None:
    """Download the source datasets required for the 2025 analysis."""
    RAW_DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

    for dataset_name, url in DATA_URLS.items():
        destination = RAW_DATA_DIRECTORY / f"{dataset_name}.csv"
        download_file(url, destination)


if __name__ == "__main__":
    main()