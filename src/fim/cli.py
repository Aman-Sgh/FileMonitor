import argparse
from pathlib import Path

from src.fim.config import load_config
from src.fim.database import create_database
from src.fim.monitor import get_event_history, get_status_counts, scan_integrity
from src.fim.monitor import get_file_statuses, get_status_counts, scan_integrity

def main():
    parser = argparse.ArgumentParser(
        prog="fim",
        description="File Integrity Monitor",
    )

    parser.add_argument(
        "command",
        choices=["scan", "status", "list", "history"],
        help="Command to execute",
    )

    args = parser.parse_args()

    config_path = Path("config.yaml")
    config = load_config(config_path)

    directory = Path(config["paths"][0])
    database_path = Path("fim.db")

    connection = create_database(database_path)

    if args.command == "scan":
        stats = scan_integrity(connection, directory)

        print("Scan completed.")
        print(f"Directory: {directory}")
        print()
        print(f"Modified:  {stats['modified']}")
        print(f"Deleted:   {stats['deleted']}")
        print(f"New:       {stats['new']}")
        print(f"Unchanged: {stats['unchanged']}")

    elif args.command == "status":
        stats = get_status_counts(connection)

        print("FIM Status")
        print()
        print(f"Modified:  {stats['modified']}")
        print(f"Deleted:   {stats['deleted']}")
        print(f"New:       {stats['new']}")
        print(f"Unchanged: {stats['unchanged']}")
    
    elif args.command == "list":
        files = get_file_statuses(connection)
        
        print("FIM Files")
        print()
        for path, status in files:
            print(f"[{status}] {path}")
            
    elif args.command == "history":
        events = get_event_history(connection)
        print("FIM History")
        
        for path, event_type, timestamp in events:
            print(f"[{timestamp}] [{event_type}] {path}")

    connection.close()


if __name__ == "__main__":
    main()
    