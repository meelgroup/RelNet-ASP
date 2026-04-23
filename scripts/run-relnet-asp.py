#!/usr/bin/env python3

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--i", required=True, help="input asp file")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    input_path = Path(args.i).resolve()

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    approxasp = script_dir / "approxasp"
    helper = script_dir / "add_chain_formula.py"

    if not approxasp.exists():
        raise FileNotFoundError(f"approxasp not found: {approxasp}")

    if not helper.exists():
        raise FileNotFoundError(f"Helper script not found: {helper}")

    temp_path = None
    result_path = None

    try:
        with tempfile.NamedTemporaryFile(dir=script_dir, delete=False) as f:
            temp_path = Path(f.name)

        shutil.copyfile(input_path, temp_path)

        result_path = script_dir / f"result_{temp_path.name}"
        is_chain_path = script_dir / f"IS_chain_{temp_path.name}"
        chain_path = script_dir / f"chain_{temp_path.name}"

        with result_path.open("w", encoding="utf-8") as out:
            subprocess.run(
                [sys.executable, str(helper), "-i", temp_path.name],
                cwd=script_dir,
                stdout=out,
                check=True,
                text=True,
            )

            subprocess.run(
                [
                    str(approxasp),
                    "--sparse",
                    "--conf",
                    "0.35",
                    "--useind",
                    is_chain_path.name,
                    "--asp",
                    chain_path.name,
                ],
                cwd=script_dir,
                stdout=out,
                check=True,
                text=True,
            )

        print("### Countering finished, parsing output ###")
        print(f"Detailed output in file: {result_path.name}")

        mul = None
        m = None
        n = None

        with result_path.open("r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("The multiplication factor:"):
                    mul = int(line.split()[-1])
                    print(f"The multiplication factor: 2^{mul}")

                elif (
                    line.startswith("After the iteration, the (median) number of solution:")
                    or line.startswith("The exact number of solution:")
                ):
                    parts = line.split()
                    m = int(parts[-5])
                    n = int(parts[-1])

        if m is not None and n is not None and mul is not None:
            print(f"The number of answer sets: {m} X 2^{n}")
            print(f"The network reliability: {m} X 2^{n} / 2^{mul}")
        else:
            print("Error")
            print(f"Detailed output in file: {result_path.name}")

    except subprocess.CalledProcessError as e:
        print("Error while running an external command.")
        print(f"Command: {e.cmd}")
        print(f"Return code: {e.returncode}")
        if result_path is not None:
            print(f"Detailed output in file: {result_path.name}")
        raise

    finally:
        if temp_path is not None:
            for p in [
                temp_path,
                script_dir / f"IS_chain_{temp_path.name}",
                script_dir / f"chain_{temp_path.name}",
            ]:
                try:
                    p.unlink()
                except FileNotFoundError:
                    pass


if __name__ == "__main__":
    main()