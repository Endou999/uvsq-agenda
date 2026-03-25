# UVSQ Agenda Auto-Sync (Celcat)

Ce dépôt permet de récupérer automatiquement l'emploi du temps de l'UVSQ (géré via Celcat) et de l'importer dans des applications comme Google Calendar ou Apple Calendar.

**Intérêts principaux du script :**

  * **Nettoyage de l'emploi du temps :** L'algorithme filtre chaque créneau pour supprimer le charabia et n'afficher que les informations utiles.
  * **Localisation précise :** La salle exacte est extraite et assignée directement au champ "Lieu" de l'événement.
  * **Code couleur par type de cours :** Le script sépare l'emploi du temps en plusieurs fichiers distincts (`CM`, `TD`, `TP`, `EXAM`, `AUTRE`). Cela permet d'attribuer une couleur différente à chaque type de cours dans votre agenda. Il faut donc importer chaque fichier séparément.

## Installation et Configuration

### 1\. Forker le projet

Cliquez sur le bouton **Fork** en haut à droite de ce dépôt pour le copier sur votre propre compte GitHub.

### 2\. Configurer vos groupes et filtrer vos options

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

-----

### Exemple : Trouver votre groupe exact sur Celcat

Pour que le script fonctionne, vous devez entrer l'identifiant de groupe exact de Celcat dans la variable `MY_GROUPS`. Voici comment le trouver.

#### Étape 1 : Effectuer la recherche

Allez sur la page de recherche de Celcat UVSQ. Dans le champ "Ressources", tapez votre recherche (dans mon cas, `s6 lddmp`).

<img width="1678" height="1024" alt="image" src="https://github.com/user-attachments/assets/503ecf08-59c7-40c6-8854-16a2726430d0" />

#### Étape 2 : Identifier l'intitulé complet

Dans les résultats de recherche, identifiez la chaîne de caractères qui correspond à votre groupe.

Dans mon exemple, l'intitulé complet affiché est :
`L3 Double Diplôme Mathématiques Physique parcours PSC S6 ( S6 LDDMP PSC ) (S6 LDDMP PSC)`

<img width="1910" height="1071" alt="image" src="https://github.com/user-attachments/assets/23d59b22-ae25-4f3e-b656-c5f4d65c0762" />

#### Étape 3 : Extraire l'identifiant du groupe

La partie que vous devez copier est l'identifiant court situé entre parenthèses, **sans** les parenthèses elles-mêmes. C'est cet identifiant précis que Celcat utilise pour lier votre emploi du temps.

<img width="1653" height="476" alt="image" src="https://github.com/user-attachments/assets/2354e2fa-bd9c-4800-a89a-31a181b503bc" />

#### Étape 4 : Application dans le code

Pour cet exemple, l'identifiant exact à utiliser est `S6 LDDMP PSC`. Vous devez l'ajouter à votre fichier `export_uvsq.py` comme suit :

```python
MY_GROUPS = [
    "S6 LDDMP PSC",  # Groupe extrait de Celcat pour le Semestre 6
    # "S5 LDDMP PSC", # (Exemple si vous devez ajouter un autre semestre)
]
```

-----

### 3\. Activer l'automatisation

1.  Allez dans l'onglet **Actions** de votre dépôt GitHub.
2.  Autorisez l'exécution des workflows.
3.  Le workflow `Update UVSQ Calendars` s'exécutera automatiquement toutes les 2 heures.

### 4\. Importer dans Google Calendar

Le script met à jour plusieurs fichiers à la racine (`UVSQ_CM.ics`, `UVSQ_TD.ics`, etc.). Répétez cette procédure pour **chaque fichier** afin de configurer vos couleurs :

1.  Ouvrez un fichier `.ics` dans GitHub.
2.  Cliquez sur le bouton **Raw** en haut à droite.
3.  Copiez l'URL de la page.
4.  Dans Google Calendar, allez dans **Autres agendas** \> **+** \> **À partir de l'URL**.
5.  Collez l'URL et validez.
6.  Changez la couleur du calendrier nouvellement ajouté dans Google Calendar.
