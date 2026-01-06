import os
import sys
import argparse
import subprocess
from rich.console import Console

console = Console()

# --- CONFIGURATION ---
BASE_DIR = "/home/leo/Projets"  # Ton dossier racine
EDITOR = "code"                 # Ton éditeur (code, nvim, nano...)

TEMPLATES = {
    "python": {
        "dirs": ["src", "tests", "docs"],
        "files": {
            "main.py": "def main():\n    print('Hello World')\n\nif __name__ == '__main__':\n    main()",
            "requirements.txt": "",
            ".gitignore": "__pycache__/\nvenv/\n.env",
            "README.md": "# {name}\n\nProject created automatically."
        },
        "commands": ["python -m venv venv"] # Commande à lancer après création
    },
    "web": {
        "dirs": ["assets/img", "assets/css", "assets/js"],
        "files": {
            "index.html": "<!DOCTYPE html>\n<html lang='fr'>\n<head>\n    <meta charset='UTF-8'>\n    <title>{name}</title>\n    <link rel='stylesheet' href='assets/css/style.css'>\n</head>\n<body>\n    <h1>Welcome to {name}</h1>\n    <script src='assets/js/app.js'></script>\n</body>\n</html>",
            "assets/css/style.css": "body { font-family: sans-serif; }",
            "assets/js/app.js": "console.log('App loaded');",
            "README.md": "# {name}\n\nSite web généré."
        },
        "commands": []
    }
}

def create_project(name, project_type):
    target_dir = os.path.join(BASE_DIR, project_type.capitalize(), name)
    
    # 1. Création du dossier principal
    if os.path.exists(target_dir):
        console.print(f"[bold red]❌ Le dossier '{target_dir}' existe déjà ![/bold red]")
        sys.exit(1)
    
    os.makedirs(target_dir)
    console.print(f"[green]📁 Dossier créé : {target_dir}[/green]")

    template = TEMPLATES.get(project_type)

    # 2. Création des sous-dossiers
    for d in template["dirs"]:
        os.makedirs(os.path.join(target_dir, d), exist_ok=True)

    # 3. Création des fichiers
    for filename, content in template["files"].items():
        file_path = os.path.join(target_dir, filename)
        with open(file_path, "w") as f:
            f.write(content.format(name=name))
    
    # 4. Exécution des commandes (ex: création du venv)
    for cmd in template["commands"]:
        console.print(f"[yellow]⚙️ Exécution : {cmd}...[/yellow]")
        subprocess.run(cmd, shell=True, cwd=target_dir)

    # 5. Git Init
    subprocess.run("git init", shell=True, cwd=target_dir, stdout=subprocess.DEVNULL)
    console.print("[cyan]🐙 Git initialisé.[/cyan]")

    # 6. Ouvrir VS Code
    console.print(f"[bold blue]🚀 Ouverture de {EDITOR}...[/bold blue]")
    subprocess.Popen([EDITOR, target_dir])

def main():
    parser = argparse.ArgumentParser(description="Générateur de projet rapide.")
    parser.add_argument("name", help="Nom du projet")
    parser.add_argument("--type", choices=["python", "web"], default="python", help="Type de projet")
    
    args = parser.parse_args()
    create_project(args.name, args.type)

if __name__ == "__main__":
    main()