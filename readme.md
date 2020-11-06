# Attestation22
Attestation22 génère des Attestation de déplacement dérogatoire rapidement à l'aide de fichier configuration.

<img src="https://limg.app/i/9Uv6ro.gif" alt="Demo">


### Comment utiliser Attestation22
* Télécharger le fichier [exe](https://github.com/havenstd06/Attestation22/releases) (windows)
* Ouvrir **"Attestation22.exe"** dans un dossier
* Entre un nom pour le fichier configuration (note: le fichier généré est réutilisable)
* Suivre les instructions
* Votre attestation sera placé dans le dossier **"Attestations"**


### Développement
* cloner le repo: ``git clone https://github.com/Havenstd06/Attestation22``
* ``pip install -r requirements.txt``

### Définitions

#### Format
Date de naissance :  **JJ**/**MM**/**AAAA** (J = Jour | M = Mois | A = Année)

#### Liste de motif :

**travail** : Déplacements entre le domicile et le lieu d’exercice de l’activité professionnelle ou
un établissement
d’enseignement ou de formation, déplacements professionnels ne pouvant être différés ,
déplacements pour un concours ou un examen.

**achats** : Déplacements pour effectuer des achats de fournitures nécessaires à l'activité
professionnelle, des achats de première nécessité dans des établissements dont les activités
demeurent autorisées, le retrait de commande et les livraisons à domicile

**sante** : Consultations, examens et soins ne pouvant être assurés à distance et l’achat de
médicaments

**famille** : Déplacements pour motif familial impérieux, pour l'assistance aux personnes vulnérables
et précaires ou la garde d'enfants

**handicap** : Déplacement des personnes en situation de handicap et leur accompagnant

**sport_animaux** : Déplacements brefs, dans la limite d'une heure quotidienne et dans un rayon maximal
d'un kilomètre autour du domicile, liés soit à l'activité physique individuelle des personnes, à
l'exclusion de toute pratique sportive collective et de toute proximité avec d'autres personnes, soit à
la promenade avec les seules personnes regroupées dans un même domicile, soit aux besoins des
animaux de compagnie

**convocation** : Convocation judiciaire ou administrative et pour se rendre dans un service public

**missions** : Participation à des missions d'intérêt général sur demande de l'autorité administrative

**enfants** : Déplacement pour chercher les enfants à l’école et à l’occasion de leurs activités
périscolaires.
