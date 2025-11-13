# Einfacher Port-Scanner

Kurz: Ein kleines Lernprojekt für dein Cybersecurity-Portfolio. Dieser Scanner prüft, welche TCP-Ports auf einem Ziel offen sind.

---

## Was ist das?
Ein einfacher TCP Port-Scanner geschrieben in Python. Er ist als Lernprojekt gedacht und hilft dir, Grundlagen von Netzwerk-Scanning, `socket` und Multithreading zu üben.

## Features
- CLI mit `argparse`
- Paralleles Scannen mit `ThreadPoolExecutor`
- Flexible Port-Angabe (`1-1024`, `22,80,443`, oder gemischt)
- Optionaler Thread-Count, Timeout und Delay
- Ergebnis optional in Datei speichern
- Kurzer legaler Hinweis (nur mit Erlaubnis scannen)

## Dateien im Repo
- `port_scanner.py` — der Python-Scanner (Hauptdatei)
- `README.md` — diese Datei
- `LICENSE` — (optional) Lizenzdatei, z.B. MIT
- `results_example.txt` — (optional) Beispielausgabe

## Voraussetzungen
- Python 3.7+
- Nur Standardbibliothek wird genutzt (keine extra Pakete nötig)

## Installation / Vorbereitung
1. Klone das Repository oder lade die Dateien herunter.
2. Stelle sicher, dass Python installiert ist.


## Nutzung / Beispiele

```bash
python3 portscanner.py --target <ZIEL> [--ports <PORTS>] [--threads <N>] [--timeout <S>] [--output <DATEI>]
```

Ein paar Beispiele:

```bash
# Scanne localhost, Ports 1-1024 (Default)
python3 portscanner.py --target 127.0.0.1

# Scanne nur Top-Ports (schneller)
python3 portscanner.py --target example.com --top

# Scanne bestimmte Ports
python3 portscanner.py --target 192.168.1.10 --ports 22,80,443

# Scanne mit weniger Timeout und mehr Threads
python3 portscanner.py --target example.com --ports 1-1024 --threads 200 --timeout 0.3

# Speichere Ergebnis in Datei
python3 portscanner.py --target 10.0.0.5 --ports 22,80 --output scan_ergebnis.txt
```

## Hinweise zur Benutzung / Legal
**Wichtig:** Scanne nur Hosts, für die du ausdrückliche Erlaubnis hast. Nicht autorisiertes Scannen kann illegal sein und rechtliche Folgen haben. Nutze dieses Tool nur in Testumgebungen oder auf Systemen, die du besitzt oder für die du freigegeben wurdest.

