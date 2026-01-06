
# ⚡ Lazy-Start : Project Scaffolder

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Fedora](https://img.shields.io/badge/Fedora-Linux-blue?style=for-the-badge&logo=fedora&logoColor=white)
![Automation](https://img.shields.io/badge/Focus-Productivity-green?style=for-the-badge)

**Lazy-Start** est un outil CLI (Command Line Interface) d'automatisation pour développeurs.
Il permet d'initialiser un environnement de développement complet en une seule commande : structure de dossiers, fichiers de base, environnement virtuel, git local et création du dépôt distant GitHub.

---

## 🚀 Fonctionnalités Clés

* **Templates Intelligents** :
    * 🐍 **Python** : Crée l'arborescence, `main.py`, `.gitignore` et **initialise automatiquement le venv**.
    * 🌐 **Web** : Génère un squelette HTML5 / CSS3 / JS prêt à l'emploi.
* **GitHub Integration** : Crée le dépôt public sur votre compte GitHub, lie le remote et push le premier commit (via flag `--github`).
* **Auto-Sanitization** : Nettoie automatiquement les noms de projets (ex: "Mon Super Projet!" ➡️ `mon_super_projet`).
* **Workflow Rapide** : Initialise Git, configure la branche `main` et **ouvre VS Code** automatiquement.

---

## 🛠️ Installation

### 1. Pré-requis
* Python 3
* **GitHub CLI** (`gh`) pour l'intégration distante.

Sur Fedora :
```bash
sudo dnf install gh
gh auth login  # À faire une seule fois pour connecter votre compte

```

### 2. Installation du script

```bash
# Cloner le dépôt
git clone [https://github.com/VOTRE_USERNAME/ProjectManager.git](https://github.com/VOTRE_USERNAME/ProjectManager.git)
cd ProjectManager

# Créer l'environnement virtuel pour le script lui-même
python -m venv venv
source venv/bin/activate

# Installer la librairie d'interface (Rich)
pip install rich

```

### 3. Configuration (Alias)

Pour utiliser la commande `new` partout, ajoutez cet alias dans votre `.bashrc` ou `.zshrc` :

```bash
# Remplacez /chemin/vers/ par votre vrai chemin
alias new="/chemin/vers/ProjectManager/venv/bin/python /chemin/vers/ProjectManager/start.py"

```

---

## 📘 Guide d'Utilisation

L'outil s'utilise via l'alias `new`. Le projet est toujours créé dans le **dossier courant** de votre terminal.

### 1. Mode Interactif (Recommandé)

Lancez la commande sans argument pour être guidé.

```bash
new

```

* ❓ **Questions :** Nom du projet ? Création GitHub (O/N) ?
* ℹ️ **Défaut :** Crée un projet Python si le type n'est pas précisé.

### 2. Commandes Rapides

| Action | Commande | Description |
| --- | --- | --- |
| **Projet Python** | `new MonScript` | Crée un projet Python + Venv localement. |
| **Projet Web** | `new MonSite --type web` | Crée un projet HTML/CSS/JS localement. |
| **Full GitHub** | `new MonProjet --github` | Crée le projet local + **Repo GitHub distant** + Push. |
| **Raccourci** | `new MonProjet -gh` | Idem que ci-dessus (alias court). |

### 3. Exemple de flux (Workflow)

```bash
# 1. Je vais dans mon dossier de travail
cd ~/Documents/Dev

# 2. Je lance la création d'un projet web avec hébergement GitHub
new "Portfolio 2026" --type web -gh

# Résultat :
# > Dossier 'portfolio_2026' créé (nom nettoyé).
# > Fichiers HTML/CSS générés.
# > Repo GitHub 'portfolio_2026' créé et synchronisé.
# > VS Code s'ouvre.

```

---

## ⚙️ Structure du Projet

Le script repose sur un dictionnaire de templates extensible dans `start.py`.

```python
TEMPLATES = {
    "python": { "dirs": [...], "files": {...}, "commands": ["python -m venv venv"] },
    "web": { ... }
}

```

*Vous pouvez facilement ajouter des templates (C++, Java, Node.js) en modifiant ce dictionnaire.*