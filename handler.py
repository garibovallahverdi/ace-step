import subprocess
from pathlib import Path

OUTPUT = Path("output.wav")

def generate_audio(text: str):
    cmd = [
        "acestep",
        "--text", text,
        "--out", str(OUTPUT)
    ]

    print("Running ACE-Step...")
    subprocess.run(cmd, check=True)

    if OUTPUT.exists():
        print("✅ Audio generated:", OUTPUT)
    else:
        print("❌ Failed to generate audio")

if __name__ == "__main__":
    generate_audio("Salam! Bu ACE-Step testidir 🚀")
