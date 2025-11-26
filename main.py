from pathlib import Path
import argparse
from parse import load_sessions
from aggregate import summarize_sessions, save_summary_json, save_summary_csv, save_summary_sqlite

def main():
    # -------------------------
    # Command-line argument parsing
    # -------------------------
    parser = argparse.ArgumentParser(description="QA Test Reporting System")
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Folder containing JSON test session files or a single JSON file"
    )
    parser.add_argument(
        "--json",
        type=str,
        default="summary.json",
        help="Output JSON file path"
    )
    parser.add_argument(
        "--csv",
        type=str,
        default="summary.csv",
        help="Output CSV file path"
    )
    parser.add_argument(
        "--sqlite",
        type=str,
        default="",
        help="Path to output SQLite summary database."
    )
    args = parser.parse_args()

    # -------------------------
    # Gather input files
    # -------------------------
    input_path = Path(args.input)
    if input_path.is_dir():
        files = list(input_path.glob("*.json"))
    else:
        files = [input_path]

    if not files:
        print("No JSON files found in input path.")
        return

    # -------------------------
    # Load sessions from all files
    # -------------------------
    try:
        sessions = load_sessions(files)
    except Exception as e:
        print(f"Error loading sessions: {e}")
        return

    if not sessions:
        print("No sessions loaded from the JSON files.")
        return

    # -------------------------
    # Aggregate / summarize sessions
    # -------------------------
    summary = summarize_sessions(sessions)



    # -------------------------
    # Save reports
    # -------------------------
    output_json = Path(args.json)
    output_csv = Path(args.csv)

    save_summary_json(summary, output_json)
    save_summary_csv(summary, output_csv)
    if args.sqlite:
        save_summary_sqlite(summary, Path(args.sqlite))
        print(f"Saved SQLite summary to {args.sqlite}")
 


    print(f"✅ Summary saved successfully!")
    print(f"   JSON -> {output_json.resolve()}")
    print(f"   CSV  -> {output_csv.resolve()}")


if __name__ == "__main__":
    main()
