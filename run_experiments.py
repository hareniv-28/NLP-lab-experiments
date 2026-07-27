from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

# Change the sample input values here if you want different test data.
experiments = [
    ("experiment1", ["This is a simple example sentence.\n"]),
    ("experiment2", ["This is a sample sentence for POS tagging.\n"]),
    ("experiment3", ["2\nAI is changing the world.\nTechnology improves daily life.\nAI\ntechnology\n"]),
    ("experiment4", ["3\nMachine learning is useful.\nDeep learning is powerful.\nSearch engines find information.\nmachine learning\n"]),
    ("experiment5", ["Microsoft announced a new product in London.\n2\n"]),
    ("experiment6", ["This treatment helps reduce symptoms.\n1\n"]),
]

for name, inputs in experiments:
    folder = ROOT / name
    script = folder / f"{name}.py"
    output_path = folder / "output.txt"

    result = subprocess.run(
        [sys.executable, str(script)],
        input="".join(inputs),
        text=True,
        capture_output=True,
        timeout=180,
    )

    if result.returncode == 0:
        output_path.write_text(result.stdout, encoding="utf-8")
        print(f"Generated {output_path}")
    else:
        error_text = result.stderr.strip() or "Unknown error"
        output_path.write_text(
            f"Execution failed.\n\n{error_text}",
            encoding="utf-8",
        )
        print(f"Failed {name}: {error_text}")
