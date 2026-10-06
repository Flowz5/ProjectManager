import os
import argparse
from rich.console import Console
from rich.prompt import Prompt
from .creator import create_project

console = Console()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_available_templates():
    templates_dir = os.path.join(BASE_DIR, "templates")
    if not os.path.exists(templates_dir):
        return []
    return [d for d in os.listdir(templates_dir) if os.path.isdir(os.path.join(templates_dir, d))]

def main():
    parser = argparse.ArgumentParser(description="Générateur de projet rapide (Lazy-Start).")
    parser.add_argument("name", nargs="?", help="Nom du projet")
    
    available_templates = get_available_templates()
    if not available_templates:
        available_templates = ["python"]
        
    parser.add_argument("--type", choices=available_templates, default="python", help="Type de projet")
    parser.add_argument("--github", "-gh", action="store_true", help="Créer le dépôt sur GitHub automatiquement")
    
    args = parser.parse_args()
    
    project_name = args.name
    project_type = args.type
    use_github = args.github

    # Mode Interactif
    if not project_name:
        console.print(f"[bold]Création d'un projet...[/bold]")
        project_type = Prompt.ask("👉 [bold green]Type de projet ?[/bold green]", choices=available_templates, default="python")
        while not project_name:
            project_name = Prompt.ask("👉 [bold green]Nom du projet ?[/bold green]")
            
        if not use_github:
            github_ask = Prompt.ask("Voulez-vous créer le repo GitHub ?", choices=["y", "n"], default="n")
            if github_ask == "y":
                use_github = True

    create_project(project_name, project_type, use_github, BASE_DIR)

if __name__ == "__main__":
    main()
