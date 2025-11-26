
from typing import List, Dict
from collections import defaultdict
from pathlib import Path
import json
import csv
import sqlite3
from parse import Session

def summarize_sessions(sessions: List[Session]) -> Dict:
    """
    Aggregate statistics from the DUT sessions.

    Returns a dictionary structured as:
    {
        'total_tests': int,
        'total_passed': int,
        'total_failed': int,
        'total_skipped': int,
        'total_execution_time': float,
        'average_execution_time': float,
        'overall_pass_rate': float,  # percentage
        'dut_stats': {
            'DUT_A': {
                'passed': int,
                'failed': int,
                'skipped': int,
                'total': int,
                'execution_time': float,
                'average_execution_time': float,
                'pass_rate': float
            },
            ...
        }
    }
    """
    #Declare all the counters
    total_tests = 0
    total_passed = 0
    total_failed = 0
    total_skipped = 0
    total_execution_time = 0.0

    #Declare dictionary so store statistics for each individual DUT
    dut_stats: Dict[str, Dict[str, float]] = {}

    #Iterate for all the tests in each session
    for session in sessions:
        stats = defaultdict(int)
        dut_execution_time = 0.0
        #Increase counters for status and execution time
        for test in session.tests:
            stats[test.status] += 1
            dut_execution_time += test.duration

        #Get total tests done in each DUT
        stats['total'] = len(session.tests)

        #Computes average execution time and pass rate of each individual DUT
        avg_exec_time = dut_execution_time / stats['total'] if stats['total'] > 0 else 0.0
        pass_rate = (stats.get('passed', 0) / stats['total'] * 100) if stats['total'] > 0 else 0.0

        #Store stats per each individual DUT
        dut_stats[session.dut] = {
            'passed': stats.get('passed', 0),
            'failed': stats.get('failed', 0),
            'skipped': stats.get('skipped', 0),
            'total': stats['total'],
            'execution_time': dut_execution_time,
            'average_execution_time': avg_exec_time,
            'pass_rate': pass_rate
        }

        #Update overall values
        total_tests += stats['total']
        total_passed += stats.get('passed', 0)
        total_failed += stats.get('failed', 0)
        total_skipped += stats.get('skipped', 0)
        total_execution_time += dut_execution_time

    overall_pass_rate = (total_passed / total_tests * 100) if total_tests else 0.0
    overall_avg_exec_time = (total_execution_time / total_tests) if total_tests else 0.0

   #Return the overall values and the stats per individual DUT
    return {
    "overall": {
        "total_tests": total_tests,
        "passed": total_passed,
        "failed": total_failed,
        "skipped": total_skipped,
        "execution_time": total_execution_time,
        "average_execution_time": overall_avg_exec_time,
        "pass_rate": overall_pass_rate
    },
    "dut_stats": dut_stats
}

def save_summary_json(summary: Dict, output_path: Path):
    """
    Save the summary dictionary as a JSON file.
    """
    with output_path.open('w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)


def save_summary_csv(summary: Dict, output_path: Path):
    """
    Save DUT-level summary in CSV format including:
    passed, failed, skipped, total, pass_rate (%), execution_time, average_execution_time.

    If include_overall is True, appends a row with overall totals.
    """

    dut_stats = summary.get('dut_stats', {})

    with output_path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        #Write CSV headers
        writer.writerow([
            'DUT', 'passed', 'failed', 'skipped', 'total',
            'pass_rate (%)', 'execution_time', 'average_execution_time'
        ])

    #Write stats per each DUT
        for dut, stats in dut_stats.items():
            writer.writerow([
                dut,
                stats.get('passed', 0),
                stats.get('failed', 0),
                stats.get('skipped', 0),
                stats.get('total', 0),
                round(stats.get('pass_rate', 0.0), 2),
                round(stats.get('execution_time', 0.0), 2),
                round(stats.get('average_execution_time', 0.0), 2)
            ])

        #Write overall stats
        writer.writerow([
            'ALL',
            summary.get('total_passed', 0),
            summary.get('total_failed', 0),
            summary.get('total_skipped', 0),
            summary.get('total_tests', 0),
            round(summary.get('overall_pass_rate', 0.0), 2),
            round(summary.get('total_execution_time', 0.0), 2),
            round(summary.get('average_execution_time', 0.0), 2)
        ])

def save_summary_sqlite(summary: dict, db_path: Path):
    """
    Save aggregated summary metrics into a SQLite database.
    This allows Grafana to use the DB as a data source.
    """
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create table for per-DUT metrics
    c.execute("""
        CREATE TABLE IF NOT EXISTS dut_summary (
            dut TEXT PRIMARY KEY,
            passed INTEGER,
            failed INTEGER,
            skipped INTEGER,
            total INTEGER,
            execution_time REAL,
            avg_execution_time REAL,
            pass_rate REAL
        )
    """)

    # Insert per-DUT stats
    for dut, stats in summary["dut_stats"].items():
        c.execute("""
            INSERT OR REPLACE INTO dut_summary
            (dut, passed, failed, skipped, total, execution_time, avg_execution_time, pass_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            dut,
            stats["passed"],
            stats["failed"],
            stats["skipped"],
            stats["total"],
            stats["execution_time"],
            stats["average_execution_time"],
            stats["pass_rate"]
        ))

    # Optionally, save overall summary
    c.execute("""
        CREATE TABLE IF NOT EXISTS overall_summary (
            id INTEGER PRIMARY KEY,
            total_tests INTEGER,
            passed INTEGER,
            failed INTEGER,
            skipped INTEGER,
            execution_time REAL,
            avg_execution_time REAL,
            pass_rate REAL
        )
    """)
    overall = summary["overall"]
    c.execute("DELETE FROM overall_summary")  # Only keep latest
    c.execute("""
        INSERT INTO overall_summary
        (total_tests, passed, failed, skipped, execution_time, avg_execution_time, pass_rate)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        overall["total_tests"],
        overall["passed"],
        overall["failed"],
        overall["skipped"],
        overall["execution_time"],
        overall["average_execution_time"],
        overall["pass_rate"]
    ))

    conn.commit()
    conn.close()
