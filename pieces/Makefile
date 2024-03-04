# création de jetons pour quattro

TAILLE = 150 # carrés de 150 x 150 pixels

all:
	blender --background --python pions-quattro.py
	for img in image-*.png; do \
	  python3 zoom_crop_image.py $${img} $(TAILLE); \
	done

clean:
	rm -f *.png *~

