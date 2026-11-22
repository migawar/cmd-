import argparse
import os
import subprocess
import sys
import urllib.request


def main():
    # Maak de argument parser aan
    parser = argparse.ArgumentParser(description="CMD+")

    # Voeg de parameter 'func' toe (verplicht door required=True)
    parser.add_argument('--func', type=str, required=True,
                        help="Func name.")

    # Parse de argumenten die vanuit PowerShell worden meegegeven
    args = parser.parse_args()

    # Bepaal de bestandsnaam op basis van de --func waarde
    bestandsnaam = f"{args.func}.py"

    # Controleer of het bestand al lokaal bestaat
    if os.path.exists(bestandsnaam):
        print(f"'{bestandsnaam}' already downloaded. Operating...\n")
    else:
        # Als het er niet is, probeer het te downloaden
        url = f"https://github.com/migawar/cmd-/raw/main/{bestandsnaam}"

        try:
            print(f"'{bestandsnaam}' not found. Downloading {url}...")
            urllib.request.urlretrieve(url, bestandsnaam)
            print(f"Succes! Downloaded '{bestandsnaam}'.\n")
        except Exception as e:
            print(f"ERROR: {e}")
            return

    # Voer het bestand uit via subprocess
    try:
        subprocess.run([sys.executable, bestandsnaam])
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
