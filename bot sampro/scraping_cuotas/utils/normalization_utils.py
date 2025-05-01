# normalization_utils.py
# 🧼 Funciones para normalizar nombres de equipos o estructuras repetidas

def normalize_team_name(name):
    """ 🧠 Convierte nombres a una forma estandarizada y consistente """
    if not name:
        return ""

    name = name.strip().lower()

    replacements = {
        "ny yankees": "new york yankees",
        "ny mets": "new york mets",
        "la dodgers": "los angeles dodgers",
        "sf giants": "san francisco giants",
        "chi cubs": "chicago cubs",
        "chi white sox": "chicago white sox",
        "tb rays": "tampa bay rays",
        "bos red sox": "boston red sox"
        # 📝 Agrega más según vayas detectando nombres alternos
    }

    for alias, standard in replacements.items():
        if alias in name:
            return standard

    # Si no está en la lista, capitaliza todo
    return " ".join(word.capitalize() for word in name.split())


def normalize_match(data_dict):
    """ 🔁 Recorre el diccionario y normaliza nombres de equipos en los partidos """
    normalized = {}

    for match_id, data in data_dict.items():
        teams = data["match"].split(" vs ")
        team1 = normalize_team_name(teams[0])
        team2 = normalize_team_name(teams[1])
        new_match_id = f"{team1}_vs_{team2}_{data['date']}"

        data["match"] = f"{team1} vs {team2}"
        normalized[new_match_id] = data

    return normalized
