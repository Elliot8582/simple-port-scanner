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
3. (Optional) Erstelle ein virtuelles Environment:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux / macOS
venv\Scripts\activate     # Windows
```

## Nutzung / Beispiele
Grundsyntax:

```bash
python3 port_scanner.py --target <ZIEL> [--ports <PORTS>] [--threads <N>] [--timeout <S>] [--output <DATEI>]
```

Ein paar Beispiele:

```bash
# Scanne localhost, Ports 1-1024 (Default)
python3 port_scanner.py --target 127.0.0.1

# Scanne nur Top-Ports (schneller)
python3 port_scanner.py --target example.com --top

# Scanne bestimmte Ports
python3 port_scanner.py --target 192.168.1.10 --ports 22,80,443

# Scanne mit weniger Timeout und mehr Threads
python3 port_scanner.py --target example.com --ports 1-1024 --threads 200 --timeout 0.3

# Speichere Ergebnis in Datei
python3 port_scanner.py --target 10.0.0.5 --ports 22,80 --output scan_ergebnis.txt
```

## Hinweise zur Benutzung / Legal
**Wichtig:** Scanne nur Hosts, für die du ausdrückliche Erlaubnis hast. Nicht autorisiertes Scannen kann illegal sein und rechtliche Folgen haben. Nutze dieses Tool nur in Testumgebungen oder auf Systemen, die du besitzt oder für die du freigegeben wurdest.

## Vorschläge für Erweiterungen (für dein Portfolio)
- Banner grabbing (kurzes `recv()` nach connect, um Service-Infos zu lesen)
- JSON-Ausgabe für einfache Integration in andere Tools
- UDP-Scan (komplizierter)
- Web-UI oder kleine Flask-App zur Visualisierung
- CI-Tests gegen eine lokale Test-VM

## Mitmachen / Beiträge
Wenn du etwas verbessern willst, erstelle gerne einen Pull Request. Beschreibe in der PR, was du geändert hast und warum.

## Lizenz
Füge hier deine Lizenz ein (z.B. MIT). Wenn du keine Lizenz angibst, gilt das Standard-Copyright.

## Kontakt
Z.B. `dein-name` auf GitHub — oder passe es an deine Angaben an.

---

Viel Erfolg mit deinem Portfolio! Wenn du willst, kann ich jetzt noch:

- die Datei `results_example.txt` mit einer Demo-Ausgabe erzeugen
- `port_scanner.py` so erweitern, dass es Banner liest
- eine `LICENSE` (MIT) für dich erstellen

Sag mir, was du als Nächstes möchtest.
