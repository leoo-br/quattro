import  os, sys, pygame as pg
import time

"""
Voici un corrigé pour que la partie devienne jouable (un joueur, contre
personne).

Quelques décisions particulières ont été prises :

*  dès qu'on clique sur une pièce dans le Tab à droite, cette pièce est
   sélectionnée et on ne peut plus la « reposer » dans le Tab
*  quand une pièce a été sélectionnée, on clique sur le plateau de jeu
   pour l'y poser sur une place libre. La pose est définitive
*  c'est l'odinateur qui décide s'il s'est formé un « quarto » ; si c'est
   le cas, un segment est dessiné pour le mettre en évidence

*  le mécanisme de résolution du quarto est implémenté avec des ensembles
   (type set) plutôt qu'avec des entiers ; ça ne change pas le type d'opérateur
   & pour faire soit le ET bit à bit soit l'intersection ensembliste. La seule
   chose à laquelle on doit faire attention, c'est que si on travalle avec des
   ensembles, il faut faire attention à travailler sur une copie des cases du
   plateau de jeu.

© 2019 Georges Khaznadar <georgesk@debian.org>
Licence : Domaine Public, CC0
"""

### quelques constantes
MARGE=10                   # marge entre les pièces du jeu
PIECE=150                  # largeur d'une pièce du jeu
LARG=MARGE+4*(PIECE+MARGE) # largeur de la zone de jeu
TAB_DROIT=150              # largeur du "tab" à droite
MY_FONT = None             # fonte à initialiser au départ


def dessinePiece(screen, img, X, Y):
    """
    Sert à placer une pièce de Quattro en X, Y sur le plateau
    :param: screen : le tampon de l'écran
    :param: img: une pièce, donnée par son image (type pigame.Surface)
    :param: X: n° de colonne (débute à zéro)
    :param: Y: n° de ligne (débute à zéro)
    """
    screen.blit(img, (MARGE+X*(PIECE+MARGE), MARGE+Y*(PIECE+MARGE)))
    return
    
def miniature(screen, images, noms, n, textcolor="yellow"):
    """
    place une miniature dans le tab à droite
    pour l'objet de numéro n
    :param: screen: le tampon d'écran
    :param: images: une liste d'images(pg.Surface)
    :param: noms:  une liste de noms, dans le même ordre
    :param: n: numéro de la pièce, entre 0 et 15 
    :param: textcolor: la couleur pour le texte
    """
    y=MARGE+39*n
    mini=pg.transform.scale(images[n], (37,37))
    screen.blit(mini, (LARG+MARGE+2, y))
    mots=noms[n].split("-")
    label1=MY_FONT.render(" ".join(mots[:2]), 1, pg.Color(textcolor))
    label2=MY_FONT.render(" ".join(mots[2:]), 1, pg.Color(textcolor))
    screen.blit(label1, (LARG+MARGE+50, y))
    screen.blit(label2, (LARG+MARGE+50, y+16))
    return

def afficheTab(screen, images, noms):
    """
    affiche le tab à droite
    :param: screen: le tampon d'écran
    :param: images: une liste d'images(pg.Surface)
    : param: noms:  une liste de noms, dans le même ordre
    """
    pg.draw.line(
        screen, pg.Color("white"),
        (LARG+MARGE//2, MARGE//2), (LARG+MARGE//2, LARG-MARGE//2),
        2
    )
    y=MARGE
    for n, (img, nom) in enumerate(zip(images, noms)):
        miniature(screen, images, noms, n)
    return

def tracePlateau(screen):
    """
    Trace quelques lignes pour le plateau de jeu
    :param: screen: le tampon d'écran
    """
    for i in range(4+1):
        x=MARGE//2+i*(PIECE+MARGE)
        y=x
        pg.draw.line(
            screen, pg.Color("cyan"),
            (x, MARGE//2), (x, LARG-MARGE//2),
            1
        )        
        pg.draw.line(
            screen, pg.Color("cyan"),
            (MARGE//2,y), (LARG-MARGE//2,y),
            1
        )        
    return
    
def encadre(val, min, max):
    """
    Écrête la variation de val
    @return val si min <= val <= max, sinon min ou max
    """
    if min <= val <= max: return val
    elif val < min: return min
    else: return max
    
def proprietes_communes(cases):
    """
    trouve l'ensemble des propriétés communes à une série de cases
    chaque case est un ensemble de propriétés
    @param cases une liste d'ensembles de propriétés
    @return l'intersection des ensembles de cases
    """
    proprietes=set(cases[0]) # provoque une copie !
    for c in cases[1:]:
        proprietes &= c      # la copie est nécessaire ici !
    return proprietes
    
    
def quarto(plateau):
    """
    Décide si un quarto (ou plusieurs sont détectés)
    @return une liste, vide si aucun quarto n'est trouvé, sinon
    avec des données permettant de contruire des lignes de
    quarto
    """
    result=[]
    # examen des lignes
    for Y in range(4):
        if proprietes_communes([plateau[X][Y] for X in range(4)]):
            # une propriété est commune à la ligne Y
            y=MARGE+Y*(PIECE+MARGE)+PIECE//2
            result.append(((0, y), (LARG, y)))
    # examen des colonnes
    for X in range(4):
        if proprietes_communes([plateau[X][Y] for Y in range(4)]):
            # une propriété est commune à la colonne X
            x=MARGE+X*(PIECE+MARGE)+PIECE//2
            result.append(((x, 0), (x, LARG)))
    # examen d'une diagonale
    if proprietes_communes([plateau[X][X] for X in range(4)]):
        result.append(((0, 0), (LARG, LARG)))
    # examen de l'autre diagonale
    if proprietes_communes([plateau[X][3-X] for X in range(4)]):
        result.append(((0, LARG), (LARG, 0)))
    return result
    
def feedback_piece(screen, images, noms, n):
    """
    Floute une pièce dans le Tab
    :param: screen: le tampon d'écran
    :param: images: une liste d'images(pg.Surface)
    :param: noms:  une liste de noms, dans le même ordre
    :param: n: numéro de la pièce, entre 0 et 15 
    """
    couleur=(255,255,255,128) # blanc demi-transparent
    rect=((LARG+MARGE,MARGE+39*n),(TAB_DROIT,38))
    screen.fill(
        couleur,
        rect=rect
    )
    miniature(screen, images, noms, n, "blue")
    return
    
    

def mainLoop():
    """
    boucle principale de l'ineraction
    """
    index_piece=None            # l'index de la pièce choisie
    pieces_utilisees=16*[False] # au début, aucune pièce utilisée
    plateau=[                   # et le plateau est vide de propriétés
        [ set(), set(), set(), set()],
        [ set(), set(), set(), set()],
        [ set(), set(), set(), set()],
        [ set(), set(), set(), set()],
    ]
    while True:
        for event in pg.event.get():
            if event.type in (pg.QUIT, pg.KEYDOWN):
                return
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                ## c'est un clic gauche
                mousex, mousey = pg.mouse.get_pos()
                if mousex < LARG:
                    ## c'est sur le plateau de jeu
                    X = encadre((mousex - MARGE)//(PIECE+MARGE), 0, 15)
                    Y = encadre((mousey - MARGE)//(PIECE+MARGE), 0, 15)
                    if index_piece!=None and plateau[X][Y]==set():
                        # une pièce est choisie, et la case du plateau est libre
                        dessinePiece(screen, images[index_piece], X, Y)
                        pieces_utilisees[index_piece]=True
                        proprietes=set(noms[index_piece].split("-"))
                        plateau[X][Y]=proprietes
                        index_piece=None
                        ### on examine si un quarto s'est formé
                        segments=quarto(plateau)
                        if segments:
                            for s in segments:
                                # s a une struture du genre ((gauche, haut), (droite, bas))
                                pg.draw.line(screen, pg.Color("magenta"), *s, 3)
                                pg.display.update()
                                time.sleep(3)
                                pg.quit()

                else:
                    ## c'est à droite du plateau de jeu
                    ## on choisit une pièce entre 0 et 15
                    if index_piece == None:
                        # seulement si une pièce n'est pas encore choisie
                        index_piece = encadre((mousey-MARGE)//39, 0, 15)
                        if pieces_utilisees[index_piece] == True:
                            # si la pièce est déjà utilisée, on oublie !
                            index_piece=None
                        else:
                            # la pièce est bonne à prendre, il faut un feedback
                            feedback_piece(screen, images, noms, index_piece)
                        
        pg.display.update()

if __name__=="__main__":
    pg.init()
    pg.font.init()
    MY_FONT=pg.font.SysFont("Times New Roman", 12)

    root, dirs, files = next(os.walk("pieces"))
    # chargement des images sous forme d'une liste
    images=[
        pg.image.load(os.path.join("pieces",f)) \
        for f in sorted(files) if f.endswith(".png")
    ]

    # récupération de la liste des noms, dans le même ordre
    noms = [
        f.replace("image-","").replace(".png","") \
        for f in sorted(files) if f.endswith(".png")
    ]

    screen = pg.display.set_mode((LARG+TAB_DROIT, LARG))
    screen.convert_alpha() # ajoute la gestion de transparence

    afficheTab(screen, images, noms)
    tracePlateau(screen)

    mainLoop()
