#!/usr/bin/env python3
"""
Einfacher Port-Scanner

Änderung: Wenn das Script ohne Argumente gestartet wird, zeigt es die Hilfe/Usage
und startet keinen Scan. Wenn --target angegeben ist, wird gescannt.

Wichtig: Scanne nur Hosts, für die du Erlaubnis hast!
"""

import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from typing import List, Tuple
import sys
import time

# -------------------------
# Hilfsfunktionen
# -------------------------
def parse_ports(ports_str: str) -> List[int]:
    """
    Parst eine Port-String wie:
      "1-1024" -> alle Ports 1 bis 1024
      "22,80,443" -> [22,80,443]
      "22-25,80,443,8000-8005"
    Gibt eine sortierte, einzigartige Liste mit ints zurück.
    """
    ports = set()
    parts = ports_str.split(',')
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if '-' in p:
            try:
                start, end = p.split('-', 1)
                start = int(start)
                end = int(end)
                if start > end:
                    start, end = end, start
                for port in range(start, end + 1):
                    if 1 <= port <= 65535:
                        ports.add(port)
            except ValueError:
                raise argparse.ArgumentTypeError(f"Ungültiger Portbereich: {p}")
        else:
            try:
                port = int(p)
                if 1 <= port <= 65535:
                    ports.add(port)
            except ValueError:
                raise argparse.ArgumentTypeError(f"Ungültiger Port: {p}")
    return sorted(ports)

def is_port_open(target_ip: str, port: int, timeout: float) -> bool:
    """Return True wenn TCP connect zu (target_ip, port) erfolgreich ist."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target_ip, port))
            return result == 0
    except Exception:
        return False

# -------------------------
# Scanner Logik
# -------------------------
def scan_ports(target: str,
               ports: List[int],
               timeout: float = 0.5,
               threads: int = 100,
               delay: float = 0.0) -> List[Tuple[int, str]]:
    """
    Scannt die angegebenen Ports auf target.
    Liefert Liste mit (port, 'open'/'closed').
    """
    # versuche hostname zu IP aufzulösen
    try:
        target_ip = socket.gethostbyname(target)
    except socket.gaierror as e:
        raise RuntimeError(f"Hostname konnte nicht aufgelöst werden: {e}")

    results = []
    # benutze ThreadPoolExecutor für parallele Checks
    with ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_port = {}
        for port in ports:
            future = executor.submit(is_port_open, target_ip, port, timeout)
            future_to_port[future] = port
            if delay > 0:
                time.sleep(delay)
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            try:
                open_state = future.result()
                status = 'open' if open_state else 'closed'
                results.append((port, status))
            except Exception as exc:
                results.append((port, f'error:{exc}'))
    # sortiere nach Portnummer
    results.sort(key=lambda x: x[0])
    return results

# -------------------------
# CLI / Argparse
# -------------------------
def build_arg_parser():
    parser = argparse.ArgumentParser(
        description='Einfacher TCP Port-Scanner (nur für Tests).',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--target', '-t', required=False, default=None,
                        help='Zielhost (IP oder Domain). Beispiel: --target 127.0.0.1')
    parser.add_argument('--ports', '-p', required=False, default='1-1024',
                        help='Ports: z.B. "1-1024" oder "22,80,443" oder kombiniert')
    parser.add_argument('--timeout', type=float, default=0.5,
                        help='Socket-Timeout in Sekunden (Default: 0.5)')
    parser.add_argument('--threads', type=int, default=100,
                        help='Anzahl paralleler Threads (Default: 100)')
    parser.add_argument('--output', '-o', default=None,
                        help='Optional: Speichere Ergebnis in Datei')
    parser.add_argument('--delay', type=float, default=0.0,
                        help='Optionaler Delay (Sekunden) zwischen Task-Starts (Default: 0.0)')
    parser.add_argument('--top', action='store_true',
                        help='Scanne nur \"Top common ports\" (schneller). Ignoriert --ports wenn gesetzt')
    return parser

# kleine Liste mit häufigen Ports
TOP_COMMON_PORTS = [22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389, 5900, 8080]

def print_results(target: str, results: List[Tuple[int, str]], started_at: datetime, output_file: str = None):
    lines = []
    header = f"Port-Scan Ergebnisse für {target} — Start: {started_at.isoformat(sep=' ')}"
    lines.append(header)
    lines.append('-' * len(header))
    open_ports = [p for p, s in results if s == 'open']
    if open_ports:
        lines.append(f"Offene Ports: {', '.join(str(p) for p in open_ports)}")
    else:
        lines.append("Keine offenen TCP-Ports gefunden in der gescannten Range.")
    lines.append("")
    lines.append("Detaillierte Ergebnisse:")
    for port, status in results:
        lines.append(f"  {port:5d} : {status}")
    text = '\n'.join(lines)
    print(text)
    if output_file:
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(text)
            print(f"\nErgebnisse in '{output_file}' gespeichert.")
        except Exception as e:
            print(f"Fehler beim Schreiben in Datei: {e}", file=sys.stderr)

# -------------------------
# Main Einstieg
# -------------------------
def main():
    parser = build_arg_parser()

    # Wenn das Script ohne Argumente gestartet wird, zeige Hilfe und Beispiele und beende.
    if len(sys.argv) == 1:
        parser.print_help()
        print("\nBeispiel:")
        print("  python3 port_scanner.py --target 127.0.0.1")
        print("  python3 port_scanner.py --target example.com --ports 22,80,443 --threads 100")
        print("\nHinweis: Scanne nur Hosts, für die du Erlaubnis hast.")
        sys.exit(0)

    args = parser.parse_args()

    # kurzer Hinweis
    print("Hinweis: Scanne nur Hosts, für die du Erlaubnis hast. Illegale Scans vermeiden.")
    print(f"Ziel: {args.target}")

    # Wenn kein target angegeben (z.B. nur andere args), zeige Fehler und help
    if not args.target:
        print("Fehler: Kein --target angegeben.\n", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    # Ports entscheiden
    if args.top:
        ports = TOP_COMMON_PORTS
        print(f"Scanne Top-Ports: {ports}")
    else:
        try:
            ports = parse_ports(args.ports)
            if not ports:
                raise ValueError("Keine gültigen Ports aus --ports erhalten.")
        except Exception as e:
            print(f"Fehler beim Parsen von Ports: {e}", file=sys.stderr)
            sys.exit(1)

    # scan starten
    started_at = datetime.now()
    try:
        results = scan_ports(target=args.target,
                             ports=ports,
                             timeout=args.timeout,
                             threads=args.threads,
                             delay=args.delay)
    except RuntimeError as e:
        print(f"Fehler: {e}", file=sys.stderr)
        sys.exit(2)
    except KeyboardInterrupt:
        print("\nAbbruch durch Benutzer.")
        sys.exit(130)

    print_results(args.target, results, started_at, output_file=args.output)

if __name__ == "__main__":
    main()
