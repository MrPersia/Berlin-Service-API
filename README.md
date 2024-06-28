# Berlin Service API

Dieses Projekt stellt eine API zur Verfügung, die die Servicedienstleistungen der Stadt Berlin bereitstellt. Die API wurde mit FastAPI entwickelt und nutzt eine SQL-Datenbank zur Speicherung der Daten. Die Daten werden mithilfe von BeautifulSoup und der Requests Library von der offiziellen Website der Stadt Berlin gesammelt.

## Projektübersicht

Das Projekt umfasst folgende Hauptkomponenten:

- **main.py**: Der Haupteinstiegspunkt der Anwendung. Hier wird die FastAPI-App initialisiert und gestartet.
- **models.py**: Definiert die Datenbankmodelle und enthält Funktionen zur Initialisierung der Datenbank.
- **views.py**: Beinhaltet die API-Endpunkte und die Logik zur Verarbeitung der Anfragen.
- **controllers.py**: Enthält die Logik zur Datenextraktion und -verarbeitung von der Website.


## Installation

### Voraussetzungen

Stellen Sie sicher, dass die folgenden Softwarepakete auf Ihrem System installiert sind:

- Python 3.7 oder höher
- pip (Python package installer)

### Abhängigkeiten installieren

Verwenden Sie den folgenden Befehl, um alle erforderlichen Bibliotheken zu installieren:

```sh
pip install fastapi uvicorn sqlmodel requests beautifulsoup4 sqlalchemy passlib python-jose
```

## Datenbank einrichten

Führen Sie den folgenden Befehl aus, um die Datenbank zu initialisieren und die erforderlichen Tabellen zu erstellen:

```sh
python -c "from models import create_db_and_tables; create_db_and_tables()"
```


## Anwendung starten

Starten Sie die FastAPI-Anwendung mit uvicorn:

```sh
uvicorn main:app --reload
```


### Services

- **GET /ALL-SERVICES**: Gibt die Titel aller Services sowie ihre ID zurück.
- **GET /SERVICE/{service_id}**: Gibt die Details zu einem Service zurück.
- **GET /ALL-SERVICES?DIGITAL-SERVICE=TRUE/FALSE**: Filtert nach Online- oder Offline-Services.
- **GET /ALL-SERVICES?RESPONSIBLE-OFFICE=...**: Filtert nach dem zuständigen Amt.
- **GET /ALL-FORMS**: Gibt alle Adressen von Formularen zurück.

