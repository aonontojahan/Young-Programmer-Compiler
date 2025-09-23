from __future__ import annotations
import argparse
from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class SymbolInfo:
    name: str
    sym_type: str

    def __repr__(self) -> str:
        return f"<{self.name}, {self.sym_type}>"

class ScopeTable:
# preserves insertion order
    def __init__(self) -> None:
        self.symbols: Dict[str, SymbolInfo] = {}

    def insert(self, name: str, sym_type: str) -> bool:
# Return True if inserted, False if already exists.
        if name in self.symbols:
            return False
        self.symbols[name] = SymbolInfo(name, sym_type)
        return True

    def lookup(self, name: str) -> Optional[SymbolInfo]:
# Return SymbolInfo if found, else None.
        return self.symbols.get(name)

    def print_table_lines(self) -> List[str]:
# Return list of string representations of symbols.
        return [repr(sym) for sym in self.symbols.values()]


def process_file(input_path: str, output_path: str) -> None:
    scope = ScopeTable()
    output_lines: List[str] = []

    with open(input_path, "r", encoding="utf-8") as fin:
        for lineno, raw_line in enumerate(fin, start=1):
            line = raw_line.strip()
            if not line:
                continue  # skip empty lines

            parts = line.split()
            cmd = parts[0]

            if cmd == "I":
                # Insert: remaining tokens -> name and type (type can be multi-word)
                if len(parts) < 3:
                    # malformed insert; ignore or you may log an error
                    continue
                name = parts[1]
                sym_type = " ".join(parts[2:])
                success = scope.insert(name, sym_type)
                if not success:
                    output_lines.append(f"Line {lineno}: {name} is already declared")

            elif cmd == "L":
                # Lookup
                if len(parts) < 2:
                    continue
                name = parts[1]
                found = scope.lookup(name)
                if found is None:
                    output_lines.append(f"Line {lineno}: {name} is not an identified symbol")
                # NOTE: successful lookups produce no output in sample

            elif cmd == "P":
                # Print the scope table
                output_lines.append(f"Line {lineno}:")
                table_lines = scope.print_table_lines()
                output_lines.extend(table_lines)

            elif cmd == "Q":
                # Quit — stop processing further lines
                break

            else:
                # Unknown command — ignore or optionally log
                continue

    # Write output file
    with open(output_path, "w", encoding="utf-8", newline="\n") as fout:
        for ol in output_lines:
            fout.write(ol + "\n")

    print(f"Processing finished. Output written to: {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Scope Table processor")
    parser.add_argument("input_file", nargs="?", default="input.txt", help="Input commands file (default: input.txt)")
    parser.add_argument("output_file", nargs="?", default="output.txt", help="Output results file (default: output.txt)")
    args = parser.parse_args()

    process_file(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
