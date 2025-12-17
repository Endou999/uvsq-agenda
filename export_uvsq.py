import requests
import datetime
import html
import re
from ics import Calendar, Event
from zoneinfo import ZoneInfo

# --- CONFIGURATION MULTI-GROUPES ---
# On met ici la liste de TOUS les groupes qu'on veut surveiller en même temps.
# Le script va fusionner les événements de S5 (Examens) et S6 (Futur semestre).
MY_GROUPS = [
    "S5 LDD MP PSC",  # Pour finir le semestre actuel
    "S6 LDDMP PSC"   # Pour le semestre qui commence le 19 janvier
]

BASE_URL = "https://edt.uvsq.fr/Home/GetCalendarData"

def extract_name_from_line(line):
    """ Nettoie le nom de la matière (Version Corrigée : Anti-deux-points) """
    bracket_match = re.search(r'\[(.*?)\]', line)
    if bracket_match:
        content = bracket_match.group(1)
        if len(content) < 15: 
            line = line.replace(bracket_match.group(0), "")
        else:
            line = content

    parts = line.split('-')
    best_part = ""
    for part in parts:
        p = part.strip()
        p = re.sub(r'\b[A-Z]{3,4}\d{3}[A-Z0-9]*\b', '', p)
        
        # --- MODIFICATION ICI ---
        # On enlève les parenthèses ET la ponctuation parasite (: . -) au début/fin
        p = p.replace("(", "").replace(")", "").strip(" :.-")
        
        # Filtres de qualité
        if len(p) > 3 and not re.search(r'\d{1,2}[hH:]\d{0,2}', p) and "TEMPS" not in p.upper():
            if len(p) > len(best_part):
                best_part = p         
    return best_part.strip()

def get_event_type(category, full_text):
    """ Trie les événements dans les bonnes cases """
    cat_up = category.upper()
    if "EXAMEN" in cat_up or "CONTRÔLE" in cat_up or "PARTIEL" in cat_up: return "EXAM"
    if "TD" in cat_up or "TRAVAUX DIRIGÉS" in cat_up: return "TD"
    if "TP" in cat_up or "TRAVAUX PRATIQUES" in cat_up: return "TP"
    if "CM" in cat_up or "COURS MAGISTRAUX" in cat_up or "AMPHI" in cat_up: return "CM"
    return "AUTRE"

def get_edt():
    print(f"--- Récupération V10 (Fusion S5 + S6) ---")
    
    # Préparation des calendriers (vides au début)
    cals = {
        "EXAM": Calendar(),
        "TD": Calendar(),
        "TP": Calendar(),
        "CM": Calendar(),
        "AUTRE": Calendar()
    }
    
    start_date = datetime.date.today()
    end_date = start_date + datetime.timedelta(days=180) # 6 mois devant nous

    # --- BOUCLE SUR CHAQUE GROUPE (S5 puis S6) ---
    for group_id in MY_GROUPS:
        print(f"Téléchargement du groupe : {group_id}...")
        
        payload = {
            "start": start_date.strftime("%Y-%m-%d"),
            "end": end_date.strftime("%Y-%m-%d"),
            "resType": "103",
            "calView": "agendaWeek",
            "federationIds": group_id,
            "colourScheme": "3"
        }

        try:
            response = requests.post(BASE_URL, data=payload)
            response.raise_for_status()
            data = response.json()
            print(f"   -> {len(data)} événements trouvés.")

            for item in data:
                e = Event()
                
                # Nettoyage texte
                raw_desc = item.get("description", "") or item.get("text", "")
                full_text = html.unescape(raw_desc).replace("\r", "").replace("<br />", "\n").replace("<br>", "\n")
                lines = [line.strip() for line in full_text.split('\n') if line.strip()]
                category = lines[0] if lines else "Cours"
                
                # Recherche Matière
                final_subject = ""
                for line in lines:
                    upper = line.upper()
                    if "TEMPS" in upper or "AVEC" in upper or re.search(r'^\d', line): continue
                    if re.search(r'[A-Z]{3,4}\d{3}', upper):
                        candidate = extract_name_from_line(line)
                        if candidate:
                            final_subject = candidate
                            break
                
                # Secours
                if not final_subject:
                    for line in lines:
                        if line == category: continue
                        if len(line) > 5 and "AMPHI" not in line and "SALLE" not in line and "S5" not in line and "S6" not in line and not re.search(r'\d', line):
                            final_subject = line
                            break

                # Typage
                evt_type = get_event_type(category, full_text)
                short_type = category
                if "Contrôle Continu" in category: short_type = "CC"
                elif "Examen" in category: short_type = "Exam"
                elif "Réunion" in category: short_type = "Réunion"
                elif "Travaux Dirigés" in category: short_type = "TD"
                elif "Cours Magistraux" in category: short_type = "CM"

                # Titre Final
                if final_subject: e.name = f"{final_subject} ({short_type})"
                else: e.name = short_type

                # On recrée la description en collant les lignes non-vides
                e.description = "\n".join(lines)
                
                # Salle
                found_room = ""
                for line in lines:
                    if any(x in line.upper() for x in ["AMPHI", "SALLE", "FERMAT", "DESCARTES", "D'ALEMBERT", "BUFFON", "JOLIOT", "E303", "RC14"]):
                        found_room = line
                        break
                if found_room: e.location = found_room
                elif "location" in item: e.location = item.get("location")

                # Dates & Fuseau
                fmt = "%Y-%m-%dT%H:%M:%S"
                dt_start = datetime.datetime.strptime(item.get("start"), fmt)
                dt_end = datetime.datetime.strptime(item.get("end"), fmt)
                e.begin = dt_start.replace(tzinfo=ZoneInfo("Europe/Paris"))
                e.end = dt_end.replace(tzinfo=ZoneInfo("Europe/Paris"))
                
                # Ajout dans le pot commun
                cals[evt_type].events.add(e)

        except Exception as err:
            print(f"   ERREUR sur {group_id} : {err}")

    # --- SAUVEGARDE GLOBALE ---
    files_generated = []
    for type_name, cal_obj in cals.items():
        filename = f"UVSQ_{type_name}.ics"
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(cal_obj.serialize_iter())
        files_generated.append(filename)
        
    print(f"\nSuccès total ! Fichiers générés : {', '.join(files_generated)}")

if __name__ == "__main__":
    get_edt()
