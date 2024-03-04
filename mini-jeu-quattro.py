import  os, sys, pygame as pg

"""
Courte démonstration dessinant un plateau de jeu de QUATTRO sans
aucune interaction avec l'utilisateur, hormis la scrutation
d'évènements pour fermer la fenêtre.

On sort de cette démonstration en appyant sur n'importe quelle touche
du clavier, ou encore en cliquant sur la « croix » de fermeture de la
fenêtre.

© 2019 Georges Khaznadar <georgesk@debian.org>
Licence : Domaine Public, CC0
"""

### quelques constantes
MARGE=10                   # marge entre les pièces du jeu
PIECE=150                  # largeur d'une pièce du jeu
LARG=MARGE+4*(PIECE+MARGE) # largeur de la zone de jeu
TAB_DROIT=150              # largeur du "tab" à droite


def placePiece(screen, img, X, Y):
    """
    Sert à placer une pièce de Quattro en X, Y sur le plateau
    :param: screen : le tampon de l'écran
    :param: img: une pièce, donnée par son image (type pigame.Surface)
    :param: X: n° de colonne (débute à zéro)
    :param: Y: n° de ligne (débute à zéro)
    """
    screen.blit(img, (MARGE+X*(PIECE+MARGE), MARGE+Y*(PIECE+MARGE)))
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
    myfont = pg.font.SysFont("Times New Roman", 12)
    y=MARGE
    for img, nom in zip(images, noms):
        miniature=pg.transform.scale(img, (37,37))
        screen.blit(miniature, (LARG+MARGE+2, y))
        mots=nom.split("-")
        label1=myfont.render(" ".join(mots[:2]), 1, pg.Color("yellow"))
        label2=myfont.render(" ".join(mots[2:]), 1, pg.Color("yellow"))
        screen.blit(label1, (LARG+MARGE+50, y))
        screen.blit(label2, (LARG+MARGE+50, y+16))
        y+=39
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

def mainLoop():
    """
    boucle principale de l'ineraction
    """
    while True:
       for event in pg.event.get():
            if event.type in (pg.QUIT, pg.KEYDOWN):
                return
       pg.display.update()

if __name__=="__main__":
    pg.init()
    pg.font.init()

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

    afficheTab(screen, images, noms)
    tracePlateau(screen)

    placePiece(screen, images[4], 1 ,0) 

    mainLoop()
