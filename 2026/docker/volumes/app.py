import time
from pathlib import Path


DATA_DIR = Path("/data")
REFRESH_SECONDS = 5


def list_files() -> None:
    print(f"Files mounted in {DATA_DIR}:")

    files = sorted(path for path in DATA_DIR.iterdir() if path.is_file())

    if not files:
        print("No files found. Mount a folder into /data and try again.")
        return

    for file_path in files:
        size = file_path.stat().st_size
        print(f"- {file_path.name} ({size} bytes)")


def main() -> None:
    while True:
        list_files()
        print(f"Container still running. Refreshing in {REFRESH_SECONDS} seconds...\n")
        time.sleep(REFRESH_SECONDS)


if __name__ == "__main__":
    main()
