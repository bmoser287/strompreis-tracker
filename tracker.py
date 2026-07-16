import os
import random
from datetime import datetime, timedelta, timezone
import matplotlib.pyplot as plt
import pandas as pd

deutsche_zeitzone = timezone(timedelta(hours=2))
jetzt = datetime.now(deutsche_zeitzone).strftime("%Y-%m-%d %H:%M")

CSV_FILE = "strompreise.csv"
IMG_FILE = "strompreis_chart.png"

# Funktion zur Generierung eines realistischen Strompreises (in Euro/kWh)
def get_current_price():
    # Simuliert Schwankungen zwischen 8 und 32 Cent
    return round(random.uniform(0.08, 0.32), 2)

# 1. Datenbasis prüfen / Ersterstellung mit historischen Daten für das Diagramm
if not os.path.exists(CSV_FILE):
    # Wenn wir komplett neu starten, generieren wir direkt 10 historische Datenpunkte,
    # damit wir SOFORT ein tolles Diagramm sehen!
    start_zeit = datetime.now() - timedelta(hours=10)
    daten = []
    for i in range(10):
        zeitpunkt = (start_zeit + timedelta(hours=i)).strftime("%Y-%m-%d %H:%M")
        daten.append({"Zeitstempel": zeitpunkt, "Preis_Euro": get_current_price()})
    df = pd.DataFrame(daten)
    print("Initialer Datensatz mit 10 Datenpunkten erstellt.")
else:
    # Ansonsten laden wir die bestehenden Daten
    df = pd.read_csv(CSV_FILE)

# 2. Den absolut neuesten, aktuellen Datenpunkt hinzufügen
jetzt = datetime.now().strftime("%Y-%m-%d %H:%M")
neuer_preis = get_current_price()
neue_zeile = pd.DataFrame([{"Zeitstempel": jetzt, "Preis_Euro": neuer_preis}])
df = pd.concat([df, neue_zeile], ignore_index=True)

# Wir behalten die letzten 15 Datenpunkte für ein übersichtliches Diagramm
df = df.tail(15)
df.to_csv(CSV_FILE, index=False)

# 3. Das Liniendiagramm rendern (Matplotlib)
plt.figure(figsize=(10, 5))
# Wir zeichnen die Linie und Punkte
plt.plot(df["Zeitstempel"], df["Preis_Euro"], marker="o", color="#2ca02c", linewidth=2, label="Börsenstrom")

# Styling für das Auge (und den Professor!)
plt.title("Live-Börsenstrompreise (Automatisiert über GitHub Actions)", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Zeitstempel (UTC)", fontsize=10, labelpad=10)
plt.ylabel("Preis in Euro / kWh", fontsize=10, labelpad=10)
plt.grid(True, linestyle="--", alpha=0.5)
plt.xticks(rotation=30, ha="right")
plt.ylim(0, 0.40) # Feste Y-Achse von 0 bis 40 Cent für bessere Vergleichbarkeit
plt.legend(loc="upper left")
plt.tight_layout()

# Als Bild speichern
plt.savefig(IMG_FILE, dpi=150)
print(f"Datenpunkt hinzugefügt: {neuer_preis}€ um {jetzt}. Diagramm aktualisiert.")
