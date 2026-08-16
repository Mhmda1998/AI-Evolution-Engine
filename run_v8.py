import os
import subprocess
import sys


def main():
    if not os.getenv("GEMINI_API_KEY"):
        print()
        print("❌ GEMINI_API_KEY is not set.")
        print()
        print("Set your Gemini API key first.")
        print()
        print("Linux/macOS:")
        print("  export GEMINI_API_KEY='YOUR_KEY'")
        print()
        print("Windows PowerShell:")
        print("  $env:GEMINI_API_KEY='YOUR_KEY'")
        print()
        sys.exit(1)

    print("🔐 API key detected.")
    print("🚀 Starting V8 Real Agent Evolution...")
    print()

    subprocess.run(
        [
            sys.executable,
            "V8_Real_Agent_Evolution.py",
        ],
        check=True,
    )


if __name__ == "__main__":
    main()
