# Développer un petit jeu de Quarto avec Pygame #

Quarto est un jeu classique, sur un plateau carré de 4 fois 4 cases.

Les joueurs disposent de 16 pièces qui présentent 4 attributs binaires :

*  bloc/cylindre
*  grand/petit
*  plein/creux
*  clair/foncé

Pour gagner il faut être le premier à signaler un alignement de quatre
pièces sur le plateau de jeu, qui possèdent ensemble une caractéristique
commune : par exemple quatre pièces grandes dans une ligne, ou quatre
pièces creuses dans une colonne, ou encore quatre pièces claires dans 
une diagonale du plateau de jeu.

Chaque joueur pose une pièce à son tour.

Vous pouvez [télécharger un notice pédagogique](https://www.gigamic.com/files/news/articles/documents/fiche-pedagogique_quarto-fr.pdf) pour ce jeu.

# La bibliothèque Pygame #

``pygame`` est un module Python qui permet de gérer des « jeux de
plates-formes », typiquement des jeux dans un univers en deux
dimensions, où se déplacent des objets et personnages divers.

Un programme utilisant pygame commencera par la ligne

```python
import pygame
```

ou, par commodité,

```python
import pygame as pg
```

Par la suite, nous supposerons que la deuxième option est choisie, si
bien que l'accès à chaque élément de la bibliothèque est dénoté par ``pg.``

Les concepts principaux sont :

*  des moteurs à initialiser : pygame lui-même, celui des polices de caractères
   (les « fontes »), etc. : ``pg.init()``, ``pg.font.init()``
   
*  un tampon d'écran, qui se comporte à la façon d'une grande matrice à
   deux dimensions, de pixels en mode RGBA (red, green, blue, alpha), c'est à
   dire rouge, vert, bleu, transparence. La taille de ce tampon correspond
   exactement à celle de la fenêtre dans laquelle le jeu se déroule.
   La commande ``screen = pg.display.set_mode((400,300))`` crée un tampon
   de 400 fois 300 pixels, et une fenêtre s'ouvre sur le bureau, avec
   cette même taille. La fenêtre ne contient que du noir, tant qu'on n'a
   pas recopié le tampon à l'écran, par exemple par la commande
   ``pg.display.update()``
   
*  des opérations de copie de matrices les unes dans les autres, correctement
   optimisées. Le type des matrices de pixels RGBA est ``pg.Surface`` ; la
   variable screen définie ci-dessus, le tampon d'écran, est de type 
   ``pg.Surface``. Le code suivant, 
   ``r = pg.image.load("renard.png"); screen.blit(r, (10, 20))`` permet de
   dessiner l'image d'un *renard* dans le tampon d'écran, aux coordonnées
   ``(x, y) == (10, 20))``.
   
*  une boucle de jeu, aussi appelée boucle principale. On la code souvent
   comme un boucle « infinie » commençant par ``while True:``. Dans cette
   boucle, on récupère tous les évènements issus du clavier, de la souris,
   ou d'ailleurs dans une liste fournie par l'appel de fonction
   ``pg.events.get()``, puis selon les évènements, et selon un ensemble de
   variables qui décrivent l'état du jeu, on fait évoluer ce qui est
   affiché dans la fenêtre et on déclenche des sons.
   
# Documentation de ``pygame`` #

Le site https://www.pygame.org/docs/ permet d'accéder à une bonne
documentation en ligne. L'en-tête de chaque page permet de naviguer
rapidement vers les concepts intéressants.

# Le programme ``mini-jeu-quattro.py`` #

Le programme ``mini-jeu-quattro.py`` ne permet pas de jouer vraiment, mais
c'est une base qui fournit un plateau de jeu quadrillé, une zone dénommée
« Tab » à droite du plateau, où sont représentées les seize pièces du jeu
en format miniature, avec leurs noms, et un ligne de code montre clairement
comment faire apparaître une pièce du jeu sur le plateau.

La boucle de jeu analyse les évènements, mais tout ce qu'elle fait, c'est
de stopper le « jeu » dès qu'on touche au clavier.

# Votre mission, si vous l'acceptez ... #

## Gérer le placement des pièces ##

* un clic gauche, dans le **Tab**, sélectionne une pièce
* un clic gauche, dans le **plateau**, pose la pièce sélectionnée

## Détecter une situation gagnante ##

Définir une fonction ``quarto()`` qui renvoie un booléen, ``False`` au
début du jeu, qui devient ``True`` dès qu'un alignement de pièces en ligne,
colonne ou diagonale, possède une caractéristique commune.

## Astuces... ##

### Choix de structures de données pour suivre les pièces du jeu ###

Il n'est pas facile d'exploiter les données affichées à l'écran pour
mémoriser le placement des pièces à un moment du jeu. C'est donc une bonne
idée de maintenir des structures de données appropriées :

*  pour le **Tab** : une liste des pièces déjà utilisées, qui ne sont donc
   plus disponibles
*  pour le **plateau** : un tableau (liste de listes) qui contient une
   représentation pertinente des pièces du jeu : rien, ou un quadruplet
   de propriétés binaires.
* quatre données binaires se représentent facilement comme un nombre compris
  entre zéro et 15 (sur 4 bits !). Python offre les opérateurs bit à bit :
  ``&`` qui est le ET, ``|`` qui est le OU.
  
On peut aussi essayer le type ``set`` de Python, qui peut être plus explicite.
Essayez les lignes de code suivantes :

```python
p1 = set(("grand", "bloc", "plein", "clair"))
p2 = set(("petit", "bloc", "creux", "clair"))
print(p1, p2, p1 & p2, p1 | p2)
```

### Choix de structures de données pour faciliter ``quarto()`` ###

De cette façon, si dans le tableau du plateau, on place des entiers
ou des ``set``s, le calcul avec ``&`` (le ET logique, qui revient à 
l'intersection  des ensembles) devrait permettre de coder la fonction
``quarto`` de façon efficace et élégante.
