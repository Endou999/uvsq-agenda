# UVSQ Agenda Auto-Sync (Celcat)

Ce dépôt permet de récupérer automatiquement l'emploi du temps de l'UVSQ (géré via Celcat) et de l'importer dans des applications comme Google Calendar ou Apple Calendar.

**Intérêts principaux du script :**
* **Nettoyage de l'emploi du temps :** L'algorithme filtre chaque créneau pour supprimer le charabia et n'afficher que les informations utiles.
* **Localisation précise :** La salle exacte est extraite et assignée directement au champ "Lieu" de l'événement.
* **Code couleur par type de cours :** Le script sépare l'emploi du temps en plusieurs fichiers distincts (`CM`, `TD`, `TP`, `EXAM`, `AUTRE`). Cela permet d'attribuer une couleur différente à chaque type de cours dans votre agenda. Il faut donc importer chaque fichier séparément.

## Installation et Configuration

### 1. Forker le projet
Cliquez sur le bouton **Fork** en haut à droite de ce dépôt pour le copier sur votre propre compte GitHub.

### 2. Configurer vos groupes et filtrer vos options
Dans votre dépôt, ouvrez le fichier `export_uvsq.py` et modifiez les variables de configuration au début du fichier :

* **`MY_GROUPS`** : Insérez les groupes correspondant à votre formation. Utilisez l'intitulé exact de Celcat.

    ```python
    MY_GROUPS = [
        "VOTRE_GROUPE_SEMESTRE_1",
        "VOTRE_GROUPE_SEMESTRE_2"
    ]
    ```

* **`BLACKLIST`** : Ajoutez les mots-clés des matières ou options que vous n'avez pas choisies. Les événements contenant ces mots seront ignorés.

    ```python
    BLACKLIST = [
        "MOT_CLE_OPTION_1"
    ]
    ```

Validez vos modifications avec un **Commit**.

---

### Exemple : Trouver votre identifiant de groupe exact sur Celcat

Lorsque vous affichez votre emploi du temps sur Celcat, vous voyez un intitulé long sous vos résultats de recherche ou en haut de la page.

Dans l'exemple ci-dessous, l'intitulé complet affiché est :
`L3 Double Diplôme Mathématiques Physique parcours PSC S6 ( S6 LDDMP PSC ) (S6 LDDMP PSC)`

<img width="1653" height="476" alt="image" src="https://github.com/user-attachments/assets/f725fe1a-fe5d-4a2c-b416-3fcff657f649" />

La **seule** partie que vous devez copier est l'identifiant court situé **entre les premières parenthèses**, sans les parenthèses elles-mêmes. 

Pour cet exemple, la chaîne de caractères à utiliser est `S6 LDDMP PSC`. Vous devez l'ajouter au fichier `export_uvsq.py` comme suit :

```python
MY_GROUPS = [
    "S6 LDDMP PSC",  # Groupe extrait de Celcat pour le Semestre 6
]
```

---

### 3. Activer l'automatisation
1. Allez dans l'onglet **Actions** de votre dépôt GitHub.
2. Autorisez l'exécution des workflows.
3. Le workflow `Update UVSQ Calendars` s'exécutera automatiquement toutes les 2 heures.

### 4. Importer dans Google Calendar
Le script met à jour plusieurs fichiers à la racine (`UVSQ_CM.ics`, `UVSQ_TD.ics`, etc.). Répétez cette procédure pour **chaque fichier** afin de configurer vos couleurs :

1. Ouvrez un fichier `.ics` dans GitHub.
2. Cliquez sur le bouton **Raw** en haut à droite.
3. Copiez l'URL de la page.
4. Dans Google Calendar, allez dans **Autres agendas** > **+** > **À partir de l'URL**.
5. Collez l'URL et validez.
6. Changez la couleur du calendrier nouvellement ajouté dans Google Calendar.
```
