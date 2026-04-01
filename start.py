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
            "README.md": "# {name}\n\nProjet Python classique."
        },
        "commands": ["python -m venv venv"]
    },
    "web": {
        "dirs": ["assets/img", "assets/css", "assets/js"],
        "files": {
            "index.html": "<!DOCTYPE html>\n<html lang='fr'>\n<head>\n    <meta charset='UTF-8'>\n    <title>{name}</title>\n    <link rel='stylesheet' href='assets/css/style.css'>\n</head>\n<body>\n    <h1>Welcome to {name}</h1>\n    <script src='assets/js/app.js'></script>\n</body>\n</html>",
            "assets/css/style.css": "body {{ font-family: sans-serif; background-color: #1a1a1a; color: white; }}", 
            "assets/js/app.js": "console.log('App loaded');",
            "README.md": "# {name}\n\nSite web HTML/CSS/JS statique."
        },
        "commands": []
    },
    "discord-bot": {
        "dirs": ["cogs", "data"],
        "files": {
            "bot.py": "import os\nimport discord\nfrom discord.ext import commands\nfrom dotenv import load_dotenv\n\nload_dotenv()\nTOKEN = os.getenv('DISCORD_TOKEN')\n\nintents = discord.Intents.default()\nintents.message_content = True\nbot = commands.Bot(command_prefix='!', intents=intents)\n\n@bot.event\nasync def on_ready():\n    print(f'Connecté en tant que {{bot.user}}')\n\nbot.run(TOKEN)",
            "requirements.txt": "discord.py\npython-dotenv\nrequests",
            ".env": "DISCORD_TOKEN=ton_token_ici",
            ".gitignore": "__pycache__/\nvenv/\n.env\ndata/\n*.sqlite3",
            "Dockerfile": "FROM python:3.9-slim\nWORKDIR /app\nCOPY requirements.txt .\nRUN pip install -r requirements.txt\nCOPY . .\nCMD [\"python\", \"bot.py\"]",
            "docker-compose.yml": "services:\n  {name}-bot:\n    build: .\n    container_name: {name}_container\n    restart: unless-stopped",
            "README.md": "# Bot Discord : {name}\n\nPour lancer : `docker compose up -d --build`"
        },
        "commands": ["python -m venv venv"]
    },
    "fastapi": {
        "dirs": ["app/routers", "app/models", "tests"],
        "files": {
            "app/main.py": "from fastapi import FastAPI\n\napp = FastAPI(title='{name}')\n\n@app.get('/')\ndef read_root():\n    return {{'message': 'API en ligne !'}}",
            "requirements.txt": "fastapi\nuvicorn\npydantic",
            ".gitignore": "__pycache__/\nvenv/\n.env",
            "run.sh": "#!/bin/bash\n# Lancer le serveur de développement\nuvicorn app.main:app --reload",
            "README.md": "# API : {name}\n\nLancer avec : `./run.sh`"
        },
        "commands": ["python -m venv venv", "chmod +x run.sh"]
    },
    "javafx": {
        "dirs": ["src/main/java/com/app", "src/main/resources/com/app"],
        "files": {
            "pom.xml": "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<project xmlns=\"http://maven.apache.org/POM/4.0.0\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"\n  xsi:schemaLocation=\"http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd\">\n  <modelVersion>4.0.0</modelVersion>\n  <groupId>com.app</groupId>\n  <artifactId>{name}</artifactId>\n  <version>1.0.0</version>\n  <properties>\n    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>\n    <maven.compiler.source>21</maven.compiler.source>\n    <maven.compiler.target>21</maven.compiler.target>\n  </properties>\n  <dependencies>\n    <dependency>\n      <groupId>org.openjfx</groupId>\n      <artifactId>javafx-controls</artifactId>\n      <version>21</version>\n    </dependency>\n  </dependencies>\n  <build>\n    <plugins>\n      <plugin>\n        <groupId>org.openjfx</groupId>\n        <artifactId>javafx-maven-plugin</artifactId>\n        <version>0.0.8</version>\n        <configuration>\n          <mainClass>com.app/com.app.App</mainClass>\n        </configuration>\n      </plugin>\n      <plugin>\n        <groupId>org.codehaus.mojo</groupId>\n        <artifactId>exec-maven-plugin</artifactId>\n        <version>3.1.0</version>\n        <configuration>\n          <mainClass>com.app.App</mainClass>\n        </configuration>\n      </plugin>\n    </plugins>\n  </build>\n</project>",
            "src/main/java/com/app/App.java": "package com.app;\n\nimport javafx.application.Application;\nimport javafx.scene.Scene;\nimport javafx.scene.control.Label;\nimport javafx.scene.layout.StackPane;\nimport javafx.stage.Stage;\n\npublic class App extends Application {{\n    @Override\n    public void start(Stage stage) {{\n        var javaVersion = SystemInfo.javaVersion();\n        var javafxVersion = SystemInfo.javafxVersion();\n        var label = new Label(\"Hello, JavaFX \" + javafxVersion + \", running on Java \" + javaVersion + \".\");\n        var scene = new Scene(new StackPane(label), 640, 480);\n        \n        try {{\n            scene.getStylesheets().add(getClass().getResource(\"style.css\").toExternalForm());\n        }} catch(Exception e) {{\n            System.out.println(\"CSS par défaut\");\n        }}\n\n        stage.setScene(scene);\n        stage.show();\n    }}\n\n    public static void main(String[] args) {{\n        launch();\n    }}\n}}",
            "src/main/java/com/app/SystemInfo.java": "package com.app;\n\npublic class SystemInfo {{\n    public static String javaVersion() {{\n        return System.getProperty(\"java.version\");\n    }}\n    public static String javafxVersion() {{\n        return System.getProperty(\"javafx.version\");\n    }}\n}}",
            "src/main/java/module-info.java": "module com.app {{\n    requires javafx.controls;\n    exports com.app;\n}}",
            "src/main/resources/com/app/style.css": ".root {{ -fx-background-color: #1e1e2e; }}\n.label {{ -fx-text-fill: white; -fx-font-size: 16px; }}",
            "run.sh": "#!/bin/bash\npkill -9 java 2>/dev/null\nexport GDK_BACKEND=x11\nexport _JAVA_AWT_WM_NONREPARENTING=1\nexport JAVA_TOOL_OPTIONS=\"-Dprism.order=sw\"\necho \"🚀 Lancement JavaFX...\"\nmvn clean compile exec:java -Dexec.mainClass=\"com.app.App\"",
            "README.md": "# Application JavaFX : {name}\n\nPour lancer sous Linux/Hyprland sans crash :\n`./run.sh`"
        },
        "commands": ["chmod +x run.sh"]
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
# Récupère dynamiquement la liste des templates disponibles (python, web, discord-bot, etc.)
    available_templates = list(TEMPLATES.keys())
    
    parser.add_argument("--type", choices=available_templates, default="python", help="Type de projet")
    parser.add_argument("--github", "-gh", action="store_true", help="Créer le dépôt sur GitHub automatiquement")
    
    args = parser.parse_args()
    
    project_name = args.name
    project_type = args.type
    use_github = args.github

    # Mode Interactif
    # Mode Interactif
    if not project_name:
        console.print(f"[bold]Création d'un projet...[/bold]")
        
        # Demander le type si ce n'est pas le défaut "python" qu'on veut
        project_type = Prompt.ask("👉 [bold green]Type de projet ?[/bold green]", choices=available_templates, default="python")
        
        while not project_name:
            project_name = Prompt.ask("👉 [bold green]Nom du projet ?[/bold green]")
            
        if not use_github:
            github_ask = Prompt.ask("Voulez-vous créer le repo GitHub ?", choices=["y", "n"], default="n")
            if github_ask == "y":
                use_github = True

    create_project(project_name, project_type, use_github)

if __name__ == "__main__":
    main()