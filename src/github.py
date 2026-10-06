import subprocess
import shutil
from rich.console import Console

console = Console()

def setup_github(project_path, project_name):
    """Crée le repo sur GitHub et push le code"""
    if not shutil.which("gh"):
        console.print("[bold red]❌ Erreur : GitHub CLI ('gh') n'est pas installé.[/bold red]")
        console.print("Installe-le avec : sudo pacman -S github-cli")
        return

    console.print(f"[bold yellow]☁️ Création du dépôt GitHub '{project_name}'...[/bold yellow]")
    
    try:
        cmd = f"gh repo create {project_name} --public --source=. --remote=origin --push"
        subprocess.run(cmd, shell=True, cwd=project_path, check=True)
        console.print("[bold green]✅ Dépôt GitHub créé et synchronisé ![/bold green]")
        subprocess.run("gh repo view --web", shell=True, cwd=project_path)
    except subprocess.CalledProcessError:
        console.print("[bold red]❌ Erreur GitHub (Le nom existe peut-être déjà ?)[/bold red]")
