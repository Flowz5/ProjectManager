import os
import sys
import json
import shutil
import subprocess
from rich.console import Console
from .utils import sanitize_name
from .github import setup_github

console = Console()
EDITOR = os.environ.get("EDITOR", "code")

def create_project(raw_name, project_type, use_github, base_dir):
    clean_name = sanitize_name(raw_name)
    if clean_name != raw_name.lower():
        console.print(f"[dim]Note : Nom du dossier normalisé en '{clean_name}'[/dim]")
        
    target_dir = os.path.join(os.getcwd(), clean_name)
    if os.path.exists(target_dir):
        console.print(f"[bold red]❌ Le dossier '{target_dir}' existe déjà ![/bold red]")
        sys.exit(1)
    
    # Check template
    template_dir = os.path.join(base_dir, "templates", project_type)
    if not os.path.exists(template_dir):
        console.print(f"[bold red]❌ Template '{project_type}' introuvable ![/bold red]")
        sys.exit(1)
        
    with open(os.path.join(template_dir, "config.json"), "r") as f:
        config = json.load(f)

    os.makedirs(target_dir)
    console.print(f"[green]📁 Dossier créé : {target_dir}[/green]")

    # Create empty dirs specified in config
    for d in config.get("dirs", []):
        os.makedirs(os.path.join(target_dir, d), exist_ok=True)

    # Copy files and replace {name}
    template_files_dir = os.path.join(template_dir, "template_files")
    if os.path.exists(template_files_dir):
        for root, _, files in os.walk(template_files_dir):
            for file in files:
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, template_files_dir)
                dest_path = os.path.join(target_dir, rel_path)
                
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                # Replace content
                with open(src_path, "r") as f_in:
                    content = f_in.read()
                content = content.replace("{name}", clean_name)
                with open(dest_path, "w") as f_out:
                    f_out.write(content)

    # Commands
    for cmd in config.get("commands", []):
        console.print(f"[yellow]⚙️ Exécution : {cmd}...[/yellow]")
        subprocess.run(cmd, shell=True, cwd=target_dir)

    # Git Init
    subprocess.run("git init", shell=True, cwd=target_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run("git branch -M main", shell=True, cwd=target_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run("git add .", shell=True, cwd=target_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run('git commit -m "Initial commit by Lazy-Start"', shell=True, cwd=target_dir, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    console.print("[cyan]🐙 Git local initialisé.[/cyan]")

    # GitHub
    if use_github:
        setup_github(target_dir, clean_name)

    # Open IDE
    console.print(f"[bold blue]🚀 Ouverture de {EDITOR}...[/bold blue]")
    subprocess.Popen([EDITOR, target_dir])
