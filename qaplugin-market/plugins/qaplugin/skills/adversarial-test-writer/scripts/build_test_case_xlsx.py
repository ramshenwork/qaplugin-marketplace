"""
Builds a Test Cases xlsx matching the exact format of the tester's
reference sample (MNLN-23205_Test_Cases_2.xlsx).

Usage:
    python3 build_test_case_xlsx.py <output_path.xlsx> <cases_json_path>

cases_json_path must point to a JSON file containing a list of test case
objects, each with these keys (all strings unless noted):

    id                (e.g. "TC 001")
    description       (e.g. "Verify ...")
    precondition
    steps             (a single string, steps separated by literal "\\n",
                        numbered "1. ...\\n2. ..." matching the sample style)
    test_data
    expected_result
    priority          ("P1" | "P2" | "P3")
    status            (optional; omit or empty string for a blank H cell —
                        this is the tester's field, leave blank on output)

Row type is inferred from `description`:
    - starts with "Instruction:"     -> written as-is, no special handling
                                         beyond the normal row (H left blank
                                         unless the case supplies a status)
    - starts with "[Future Scope]"   -> written as-is; H is left blank to
                                         match the reference sample's own
                                         treatment of its Future Scope row

Do not hand-format cells inline elsewhere in the skill. Always produce the
xlsx through this script so formatting stays identical across every run.
"""

import json
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

HEADER_FILL = PatternFill(start_color="FF002060", end_color="FF002060", fill_type="solid")
HEADER_FONT = Font(bold=True, color="FFFFFFFF")
WRAP_TOP = Alignment(wrap_text=True, vertical="top")

COLUMN_WIDTHS = {"A": 14, "B": 38, "C": 42, "D": 45, "E": 12, "F": 50, "G": 10}
HEADERS = [
    "Test Case ID",
    "Test Case Description",
    "Pre-Condition",
    "Test Steps",
    "Test Data",
    "Expected Result",
    "Priority",
]  # column H is intentionally unlabeled, matching the reference sample


def build(output_path: str, cases: list[dict]) -> None:
    wb = Workbook()
    ws = wb.active
    ws.title = "Test Cases"

    for col_letter, width in COLUMN_WIDTHS.items():
        ws.column_dimensions[col_letter].width = width

    for col_idx, header in enumerate(HEADERS, start=1):
        cell = ws.cell(row=1, column=col_idx, value=header)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT

    for row_offset, case in enumerate(cases, start=2):
        values = [
            case.get("id", ""),
            case.get("description", ""),
            case.get("precondition", ""),
            case.get("steps", ""),
            case.get("test_data", ""),
            case.get("expected_result", ""),
            case.get("priority", ""),
            case.get("status", ""),  # left empty unless explicitly supplied
        ]
        for col_idx, value in enumerate(values, start=1):
            cell = ws.cell(row=row_offset, column=col_idx, value=value or None)
            cell.alignment = WRAP_TOP
        ws.row_dimensions[row_offset].height = 90

    wb.save(output_path)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 build_test_case_xlsx.py <output.xlsx> <cases.json>")
        sys.exit(1)

    out_path, cases_path = sys.argv[1], sys.argv[2]
    with open(cases_path, "r", encoding="utf-8") as f:
        case_list = json.load(f)

    build(out_path, case_list)
    print(f"Wrote {len(case_list)} test cases to {out_path}")
