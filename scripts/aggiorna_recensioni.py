"""Aggiorna reviews.json con valutazione, numero di recensioni e le recensioni
che Google restituisce (al massimo 5, scelte da Google) tramite Places API (New).

Variabili d'ambiente (GitHub > Settings > Secrets and variables > Actions):
  GOOGLE_PLACES_API_KEY  chiave API con "Places API (New)" abilitata
  GOOGLE_PLACE_ID        facoltativo: se manca, lo cerca e lo stampa nel log
"""
import json, os, sys, urllib.request, datetime

KEY = os.environ.get("GOOGLE_PLACES_API_KEY")
PLACE_ID = os.environ.get("GOOGLE_PLACE_ID")
FILE = os.path.join(os.path.dirname(__file__), "..", "reviews.json")
if not KEY:
    sys.exit("Manca GOOGLE_PLACES_API_KEY")

def call(url, fields, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 method="POST" if body else "GET",
                                 headers={"X-Goog-Api-Key": KEY, "X-Goog-FieldMask": fields,
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

if not PLACE_ID:
    res = call("https://places.googleapis.com/v1/places:searchText", "places.id,places.displayName,places.formattedAddress",
               {"textQuery": "Faccin Auto di Massimo Faccin, Via Monte Ortigara 72, Cornedo Vicentino", "languageCode": "it"})
    places = res.get("places", [])
    if not places:
        sys.exit("Attività non trovata: imposta GOOGLE_PLACE_ID a mano")
    PLACE_ID = places[0]["id"]
    print(f"Place ID trovato: {PLACE_ID} ({places[0]['displayName']['text']}, {places[0]['formattedAddress']})")
    print("Salvalo nel secret GOOGLE_PLACE_ID per non cercarlo ogni volta.")

d = call(f"https://places.googleapis.com/v1/places/{PLACE_ID}?languageCode=it", "rating,userRatingCount,reviews")
google = []
for r in d.get("reviews", []):
    testo = (r.get("originalText") or r.get("text") or {}).get("text", "").strip()
    if not testo:
        continue
    google.append({"nome": r.get("authorAttribution", {}).get("displayName", "Cliente"),
                   "stelle": int(r.get("rating", 5)), "testo": testo,
                   "quando": r.get("relativePublishTimeDescription", ""), "data": r.get("publishTime", "")})
google.sort(key=lambda x: x["data"], reverse=True)

with open(FILE, encoding="utf-8") as f:
    old = json.load(f)
new = {"aggiornato": datetime.date.today().isoformat(),
       "valutazione": d.get("rating", old.get("valutazione")),
       "totale": d.get("userRatingCount", old.get("totale")),
       "google": google}
if {k: v for k, v in new.items() if k != "aggiornato"} == {k: v for k, v in old.items() if k != "aggiornato"}:
    print("Nessuna novità")
    sys.exit(0)
with open(FILE, "w", encoding="utf-8") as f:
    json.dump(new, f, ensure_ascii=False, indent=2)
print(f"Aggiornato: {new['valutazione']} su {new['totale']} recensioni, {len(google)} testi")
