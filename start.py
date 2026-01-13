import os
import sys
import argparse
import subprocess
import re
import shutil
from rich.console import Console
from rich.prompt import Prompt

console = Console()

# --- CONFIGURATION ---
CURRENT_DIR = os.getcwd()  
EDITOR = "code" # Assure-toi que VS Code est installé (code) ou change pour "nano"/"vim"

TEMPLATES = {
    "python": {
        "dirs": ["assets"],
        "files": {
            "main.py": "def main():\n    print('Hello World')\n\nif __name__ == '__main__':\n    main()",
            "requirements.txt": "",
            ".gitignore": "__pycache__/\nvenv/\n.env",
            "README.md": "# {name}\n\nProject created automatically."
        },
        "commands": ["python -m venv venv"]
    },
    "web": {
        "dirs": ["assets/img", "assets/css", "assets/js"],
        "files": {
            "index.html": "<!DOCTYPE html>\n<html lang='fr'>\n<head>\n    <meta charset='UTF-8'>\n    <title>{name}</title>\n    <link rel='stylesheet' href='assets/css/style.css'>\n</head>\n<body>\n    <h1>Welcome to {name}</h1>\n    <script src='assets/js/app.js'></script>\n</body>\n</html>",
            "assets/css/style.css": "body {{ font-family: sans-serif; }}", 
            "assets/js/app.js": "console.log('App loaded');",
            "README.md": "# {name}\n\nSite web généré."
        },
        "commands": []
    }
}

# --- FONCTION 1 : SANITIZATION (NETTOYAGE DU NOM) ---
def sanitize_name(name):
    """Transforme 'Mon Projet Web!' en 'mon_projet_web'"""
    name = name.lower()
    name = name.replace(" ", "_")
    name = re.sub(r'[^a-z0-9_]', '', name)
    return name

# --- FONCTION 2 : GITHUB AUTOMATION ---
def setup_github(project_path, project_name):
    """Crée le repo sur GitHub et push le code"""
    
    # Vérification pour FEDORA
    if not shutil.which("gh"):
        console.print("[bold red]❌ Erreur : GitHub CLI ('gh') n'est pas installé.[/bold red]")
        console.print("Installe-le avec : sudo dnf install gh") # <--- MODIFICATION ICI
        return

    console.print(f"[bold yellow]☁️ Création du dépôt GitHub '{project_name}'...[/bold yellow]")
    
    try:
        # Création et push en une ligne
        cmd = f"gh repo create {project_name} --public --source=. --remote=origin --push"
        subprocess.run(cmd, shell=True, cwd=project_path, check=True)
        
        console.print("[bold green]✅ Dépôt GitHub créé et synchronisé ![/bold green]")
        
        # Ouvre la page du repo
        subprocess.run("gh repo view --web", shell=True, cwd=project_path)
        
    except subprocess.CalledProcessError:
        console.print("[bold red]❌ Erreur GitHub (Le nom existe peut-être déjà ?)[/bold red]")

def create_project(raw_name, project_type, use_github):
    # 1. Nettoyage du nom
    clean_name = sanitize_name(raw_name)
    
    if clean_name != raw_name.lower():
        console.print(f"[dim]Note : Nom du dossier normalisé en '{clean_name}'[/dim]")
        
    target_dir = os.path.join(CURRENT_DIR, clean_name)
    
    # 2. Vérification existence
    if os.path.exists(target_dir):
        console.print(f"[bold red]❌ Le dossier '{target_dir}' existe déjà ![/bold red]")
        sys.exit(1)
    
    # 3. Création dossier
    os.makedirs(target_dir)
    console.print(f"[green]📁 Dossier créé : {target_dir}[/green]")

    template = TEMPLATES.get(project_type)

    # 4. Structure & Fichiers
    for d in template["dirs"]:
        os.makedirs(os.path.join(target_dir, d), exist_ok=True)

    for filename, content in template["files"].items():
        file_path = os.path.join(target_dir, filename)
        with open(file_path, "w") as f:
            f.write(content.format(name=clean_name))
    
    # 5. Commandes (venv)
    for cmd in template["commands"]:
        console.print(f"[yellow]⚙️ Exécution : {cmd}...[/yellow]")
        subprocess.run(cmd, shell=True, cwd=target_dir)

    # 6. Git Init (Local)
    subprocess.run("git init", shell=True, cwd=target_dir, stdout=subprocess.DEVNULL)
    subprocess.run("git branch -M main", shell=True, cwd=target_dir, stdout=subprocess.DEVNULL)
    subprocess.run("git add .", shell=True, cwd=target_dir, stdout=subprocess.DEVNULL)
    subprocess.run('git commit -m "Initial commit by Lazy-Start"', shell=True, cwd=target_dir, stdout=subprocess.DEVNULL)
    console.print("[cyan]🐙 Git local initialisé.[/cyan]")

    # 7. GitHub (Optionnel)
    if use_github:
        setup_github(target_dir, clean_name)

    # 8. Ouverture IDE
    console.print(f"[bold blue]🚀 Ouverture de {EDITOR}...[/bold blue]")
    subprocess.Popen([EDITOR, target_dir])

def main():
    parser = argparse.ArgumentParser(description="Générateur de projet rapide.")
    
    parser.add_argument("name", nargs="?", help="Nom du projet")
    parser.add_argument("--type", choices=["python", "web"], default="python", help="Type de projet")
    parser.add_argument("--github", "-gh", action="store_true", help="Créer le dépôt sur GitHub automatiquement")
    
    args = parser.parse_args()
    
    project_name = args.name
    project_type = args.type
    use_github = args.github

    # Mode Interactif
    if not project_name:
        console.print(f"[bold]Création d'un projet [cyan]{project_type.upper()}[/cyan][/bold]")
        while not project_name:
            project_name = Prompt.ask("👉 [bold green]Nom du projet ?[/bold green]")
            
        if not use_github:
            github_ask = Prompt.ask("Voulez-vous créer le repo GitHub ?", choices=["y", "n"], default="n")
            if github_ask == "y":
                use_github = True

    create_project(project_name, project_type, use_github)

if __name__ == "__main__":
    main()