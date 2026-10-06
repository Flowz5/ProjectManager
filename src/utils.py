import re

def sanitize_name(name):
    """Transforme 'Mon Projet Web!' en 'mon_projet_web'"""
    name = name.lower()
    name = name.replace(" ", "_")
    name = re.sub(r'[^a-z0-9_]', '', name)
    return name
