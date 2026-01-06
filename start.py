import os
import sys
import argparse
import subprocess
from rich.console import Console
from rich.prompt import Prompt

console = Console()

# --- CONFIGURATION ---
CURRENT_DIR = os.getcwd()  
EDITOR = "code"

TEMPLATES = {
    "python": {
        "dirs": ["src", "tests", "docs"],
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

def create_project(name, project_type):
    target_dir = os.path.join(CURRENT_DIR, name)
    
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
    
    # 4. Exécution des commandes (ex: venv)
    for cmd in template["commands"]:
        console.print(f"[yellow]⚙️ Exécution : {cmd}...[/yellow]")
        subprocess.run(cmd, shell=True, cwd=target_dir)

    # 5. Git Init
    subprocess.run("git init", shell=True, cwd=target_dir, stdout=subprocess.DEVNULL)
    # Configuration de la branche main pour éviter le message d'avertissement (au cas où)
    subprocess.run("git branch -M main", shell=True, cwd=target_dir, stdout=subprocess.DEVNULL)
    console.print("[cyan]🐙 Git initialisé.[/cyan]")

    # 6. Ouvrir VS Code
    console.print(f"[bold blue]🚀 Ouverture de {EDITOR}...[/bold blue]")
    subprocess.Popen([EDITOR, target_dir])

def main():
    parser = argparse.ArgumentParser(description="Générateur de projet rapide.")
    
    # nargs="?" signifie que l'argument est OPTIONNEL
    parser.add_argument("name", nargs="?", help="Nom du projet")
    parser.add_argument("--type", choices=["python", "web"], default="python", help="Type de projet")
    
    args = parser.parse_args()
    
    project_name = args.name
    project_type = args.type

    # Si aucun nom n'est fourni, on le demande de façon interactive
    if not project_name:
        console.print(f"[bold]Création d'un projet [cyan]{project_type.upper()}[/cyan][/bold]")
        while not project_name:
            project_name = Prompt.ask("👉 [bold green]Comment veux-tu appeler le projet ?[/bold green]")
            if not project_name:
                console.print("[red]Le nom ne peut pas être vide ![/red]")

    create_project(project_name, project_type)

if __name__ == "__main__":
    main()