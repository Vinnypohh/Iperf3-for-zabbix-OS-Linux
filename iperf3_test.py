#!/usr/bin/env python3

import sys
import subprocess
import json

def run_iperf3(server):
    try:
        # Execută comanda iperf3 și colectează rezultatul
        result = subprocess.run(
            ['iperf3', '-c', server, '-J'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,  # Modificat aici
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        # În caz de eroare, returnează un JSON cu eroare
        return json.dumps({'error': e.stderr})

def extract_sender_speed(json_data):
    try:
        # Parsează JSON-ul
        data = json.loads(json_data)
        if 'error' in data:
            raise ValueError(data['error'])

        # Extrage viteza de trimitere
        sender_speed_bps = data['end']['sum_sent']['bits_per_second']
        # Transformă viteza în Mbps
        sender_speed_mbps = sender_speed_bps / (1024 * 1024)

        # Returnează viteza de trimitere în Mbps
        return sender_speed_mbps
    except (KeyError, TypeError, ValueError) as e:
        # În caz de eroare, returnează None
        return None

def main():
    if len(sys.argv) != 2:
        print("Usage: iperf3_test.py <server>")
        sys.exit(1)

    server = sys.argv[1]

    # Rulare iperf3 și colectare rezultat
    result = run_iperf3(server)

    # Extrage viteza de trimitere
    sender_speed_mbps = extract_sender_speed(result)

    # Verifică dacă extragerea a avut succes
    if sender_speed_mbps is not None:
        # Afișează valoarea vitezei de trimitere
        print(f"{sender_speed_mbps:.2f}")
    else:
        # Afișează un mesaj de eroare în cazul în care extragerea a eșuat
        print("Error extracting sender speed")

if __name__ == '__main__':
    main()
