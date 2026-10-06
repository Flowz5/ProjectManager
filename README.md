# ⚡ Lazy-Start : Project Scaffolder & Manager

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Arch Linux](https://img.shields.io/badge/Arch_Linux-blue?style=for-the-badge&logo=archlinux&logoColor=white)
![Automation](https://img.shields.io/badge/Focus-Productivity-green?style=for-the-badge)

**Lazy-Start** est un outil CLI d'automatisation et de gestion de projets ultra-rapide.
Il initialise un environnement de développement complet en une commande : structure de dossiers, fichiers de base, git local, installation des dépendances, création du dépôt GitHub et ouverture de votre IDE.

Il s'intègre également parfaitement avec des environnements modernes (Wayland, Hyprland, Zoxide, Rofi) pour créer un workflow de productivité instantané.

---

## 🚀 Templates Disponibles (Modulaires)

L'architecture est 100% modulaire (basée sur des dossiers dans `/templates`). Les templates actuels incluent :
* 🐍 **Python** (Génère `main.py`, `.gitignore` et initialise un *venv*)
* 🦀 **Rust** (Via `cargo init`)
* 🐹 **Go** (Via `go mod init`)
* ⚛️ **React** (Génère un projet via ViteJS + `npm install`)
* ▲ **Next.js** (Squelette Next.js complet)
* ⚙️ **C++** (Structure CMake basique)
* ☕ **JavaFX** (Projet Maven + CSS)
* 🤖 **Discord Bot** (Bot Python + Docker Compose)
* 🌐 **Web Basique** (HTML5 / CSS3 / JS pur)

---

## 🛠️ Installation & Configuration

### 1. Pré-requis
* Python 3
* **GitHub CLI** (`gh`) (Optionnel, pour la création auto du repo)

```bash
sudo pacman -S github-cli
gh auth login
```

### 2. Installation de l'outil

```bash
git clone https://github.com/Flowz5/ProjectManager.git ~/ProjectManager
cd ~/ProjectManager
python -m venv venv
source venv/bin/activate
pip install rich
```

### 3. Alias CLI (`~/.zshrc`)
Pour utiliser l'outil n'importe où via la commande `new` :
```bash
alias new="$HOME/ProjectManager/venv/bin/python $HOME/ProjectManager/start.py"
```

---

## 🎯 Le Workflow Ultime (Hyprland + Rofi + Zoxide)

Au lieu de naviguer dans les dossiers avec `cd`, vous pouvez utiliser ce script pour **sauter de projet en projet, ou en créer un nouveau à la volée** !

**Pré-requis** : `zoxide`, `rofi` (ou `rofi-wayland`), `kitty`, `zellij`.

### 1. Le script `jump_project.sh`
Créez un script `~/.local/bin/jump_project.sh` et rendez-le exécutable (`chmod +x`) :

```bash
#!/bin/bash

# 1. Zoxide liste les projets, Rofi affiche l'interface
TARGET=$(zoxide query -l | rofi -dmenu -i -p "🚀 Projet (ou Créer)")

if [ -z "$TARGET" ]; then
    exit 0
fi

if [ -d "$TARGET" ]; then
    # 2A. Le projet existe : on l'ouvre directement avec Zellij
    kitty -d "$TARGET" -e zellij &
else
    # 2B. Nouveau projet : on nettoie le nom et on le crée à la racine du HOME
    CLEAN_NAME=$(echo "$TARGET" | tr '[:upper:]' '[:lower:]' | tr ' ' '_' | sed 's/[^a-z0-9_]//g')
    NEW_DIR="$HOME/$CLEAN_NAME"

    # Lance Lazy-Start (ProjectManager) puis ouvre Zellij dans le nouveau dossier
    kitty -d "$HOME" -e zsh -c "$HOME/ProjectManager/start.py '$TARGET'; cd '$NEW_DIR' 2>/dev/null && exec zellij" &
fi
```

### 2. Le raccourci Hyprland (`hyprland.conf`)
Associez le script à un raccourci clavier (ex: `Win + D`) :
```lua
hl.bind(mainMod .. " + D", hl.dsp.exec_cmd("~/.local/bin/jump_project.sh"))
```
**Résultat :** Faites `Win + D`, tapez un nom. S'il existe, vous y êtes. S'il n'existe pas, l'outil vous demande quel template utiliser, génère le code, et ouvre votre éditeur + votre multiplexeur dedans !

---

## ⚙️ Architecture & Ajout de Templates

Le code source a été refactorisé pour être **100% scalable**. Pour ajouter un nouveau template (ex: `vuejs`) :
1. Créez le dossier : `templates/vuejs/template_files/`
2. Mettez-y tous vos fichiers de base. (Le script remplacera `{name}` par le nom du projet).
3. Créez un `config.json` dans `templates/vuejs/` :
```json
{
    "dirs": ["assets", "src"],
    "commands": ["npm init vue@latest .", "npm install"],
    "description": "Mon projet VueJS"
}
```
L'outil détectera automatiquement le template `vuejs` !
