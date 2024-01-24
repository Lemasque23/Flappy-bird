#Flappy Bird Python
#par Elwan Chollet
print("by Elwan Chollet")
#--------------------
from casioplot import *
from random import randint
#--------------------
L_FENETRE = 384 #largeur de la zone graphique affichable
H_FENETRE = 192 #hauteur de la zone graphique affichable

#dimensions des caracteres des polices
LNUMH_POLICE = {"small":(8,10), "medium":(12,17), "large": (18,23)}
POLICE = "small"                      #taille de police (small, medium ou large)
H_POLICE = LNUMH_POLICE[POLICE][1]    #hauteur des caracteres de la police
LNUM_POLICE = LNUMH_POLICE[POLICE][0] #largeur des caracteres numeriques de la police
#-------------------
HMIN_TUYAU = 16            #hauteur minimale des tuyaux
H_SOL = H_POLICE + 4       #hauteur du sol
L_TUYAU = 32               #largeur des tuyaux
H_FOND = H_FENETRE - H_SOL #hauteur du fond
L_FBIRD = 17               #largeur de Flappy Bird
H_FBIRD = 12               #hauteur de Flappy Bird
D_FBIRD = 64               #position initiale de Flappy Bird
INTH_TUYAUX = 144          #espacement horizontal entre les posititions de deux tuyaux consecutifs
INTVMIN_TUYAUX = 64        #espacement vertical minimal entre les pays de tuyaux

#--------------------
def draw_prect(x, y, w, h, c):
  """
  dessine un rectangle plein
  de largeur w,hauteur h et couleur c
  avec le coin superieur gauche de coordonnees (x;y)
  """
  x2 = x + w
  for yp in range(y, y + h):
    for xp in range(x, x2):
      set_pixel(xp, yp, c)


#######################
COULEUR_BORD = (0,0,0)
COULEUR_FOND = (112,160,192)
COULEUR_SOL = (177,157,71)
COULEUR_TUYAU = (170,200,0)
PALETTE = (
  (0,0,0),
  (112,160,192),
  (201,192,193),
  (211,190, 37),
  (225,128, 21),
  (237, 80, 63),
  (235,252,220)
)
BIRD_IMG = (
  "      ######    ",
  "    ##...#__#   ",
  "   #..::#____#  ",
  " ####:::#___#_# ",
  "#....#::#___#_# ",
  "#.....#::#____# ",
  "#:...:#:::######",
  " #:::#:::#======",
  "  ###+++#=######",
  "  #++++++#=====#",
  "   ##+++++##### ",
  "     #####      "
)
# traduction des caracteres en couleurs
BIRD = [[PALETTE["# .:+=_".index(c)] for c in line] for line in BIRD_IMG]


def y_altitude(alt):
  """
  retourne la position verticale d'affichage
  d'un objet situe a l'altitude alt
  """
  return H_FOND - alt

def redraw_prect(x,y,l,h,cint,credraw):
  """
  rafraichit l'affichage d'un rectangle plein
  en redessinant uniquement ses extremites gauche et droite
  """
  x2=x+l
  for i in range(y, y + h):
    set_pixel(x, i, cint)
    set_pixel(x + 1, i, cint)
    set_pixel(x2, i, credraw)
    set_pixel(x2 + 1, i, credraw)

def draw_tuyaux(x, hinf, hsup):
  """
  affiche une paire de tuyaux
  de hinf de hauteur pour le tuyau inferieur
  de hsup de hauteur pour le tuyau superieur
  avec x comme limite gauche
  """
  yinf = y_altitude(hinf)
  draw_prect(x + 3, 0, L_TUYAU - 6, hsup - 12, COULEUR_TUYAU)
  draw_prect(x, hsup - 12, L_TUYAU, 12, COULEUR_TUYAU)
  draw_prect(x, yinf, L_TUYAU, 12, COULEUR_TUYAU)
  draw_prect(x + 3, yinf + 12, L_TUYAU - 6, hinf - 12, COULEUR_TUYAU)

def redraw_tuyaux(x, hinf, hsup):
  """
  efface l'affichage precedent puis dessine une paire de tuyaux
  de hinf de hauteur pour le tuyau inferieur
  de hsup de hauteur pour le tuyau superieur
  avec x comme limite gauche
  apres effacement de l'affichage precedent
  """
  yinf = y_altitude(hinf)
  redraw_prect(x + 3, 0, L_TUYAU - 6, hsup - 12, COULEUR_TUYAU, COULEUR_FOND)
  redraw_prect(x, hsup - 12, L_TUYAU, 12, COULEUR_TUYAU, COULEUR_FOND)
  redraw_prect(x, yinf, L_TUYAU, 12, COULEUR_TUYAU, COULEUR_FOND)
  redraw_prect(x + 3, yinf + 12, L_TUYAU - 6, hinf - 12, COULEUR_TUYAU, COULEUR_FOND)

def redraw_fbird(x, y, x_ancien, y_ancien):
  """
  dessine Flappy Bird
  dans un rectangle de L_FBIRD*H_FBIRD pixels
  de coin superieur gauche (x;y)
  apres effacement de l'ancien affichage a (x_ancien;y_ancien)
  """
  draw_prect(x_ancien + 1, round(y_ancien), L_FBIRD, H_FBIRD, COULEUR_FOND)
  y = round(y)
  for ligne in range(H_FBIRD):
    for col in range(L_FBIRD-1):
      set_pixel(x + col, y + ligne, BIRD[ligne][col])

def draw_sol():
  """
  affiche le sol et
  dedans les informations
  """
  draw_prect(0, H_FOND, L_FENETRE, H_SOL, COULEUR_SOL)
  if vx_fenetre == 0:
    info="[AC]: Demarrer"
  elif vx_fbird != 0:
    info="[AC]: Battre des ailes"
  else:
    info="[AC]: Quitter"
  draw_string(1, H_FENETRE - H_POLICE - 2, info, COULEUR_BORD, POLICE)

def draw_jeu():
  """
  initialise l'affichage en dessinant
  l'ensemble des elements graphiques
  """
  draw_prect(0, 0, L_FENETRE, H_FOND, COULEUR_FOND)
  for k in range(score - 1, len(d_tuyaux)):
    d_tuyau = d_tuyaux[k]
    if d_tuyau+L_TUYAU >= d_fenetre and d_tuyau < d_fenetre+L_FENETRE:
      draw_tuyaux(d_tuyau - d_fenetre, hinf_tuyaux[k], hsup_tuyaux[k])
  draw_sol()

def redraw_score():
  """
  affiche le score
  apres effacement de l'ancien affichage
  """
  ch_score = str(score)
  l_score = LNUM_POLICE * len(ch_score)
  x_score = L_FENETRE - l_score
  y_score = H_FENETRE - H_POLICE-2
  draw_prect(x_score, y_score, l_score, H_POLICE, COULEUR_SOL)
  draw_string(x_score, y_score, ch_score, COULEUR_BORD, POLICE)

def redraw_jeu():
  """
  rafraichit l'affichage en redessinant
  les seuls elements graphiques modifies
  """
  redraw_fbird(d_fbird - d_fenetre, y_altitude(alt_fbird), d_fbird_ancien - d_fenetre, y_altitude(alt_fbird_ancien))
  for k in range(score - 1, len(d_tuyaux)):
    d_tuyau = d_tuyaux[k]
    if d_tuyau+L_TUYAU >= d_fenetre and d_tuyau < d_fenetre+L_FENETRE:
      redraw_tuyaux(d_tuyau - d_fenetre, hinf_tuyaux[k], hsup_tuyaux[k])
  redraw_score()

#--------------------
def ajoute_tuyau():
  """
  ajoute une paire de tuyaux
  """
  global d_tuyaux, hinf_tuyaux, hsup_tuyaux
  d_tuyaux.append(d_tuyaux[-1] + INTH_TUYAUX)
  hinf_tuyau = randint(HMIN_TUYAU, H_FOND - INTVMIN_TUYAUX - HMIN_TUYAU)
  hsup_tuyau = randint(HMIN_TUYAU, H_FOND - hinf_tuyau - INTVMIN_TUYAUX)
  hinf_tuyaux.append(hinf_tuyau)
  hsup_tuyaux.append(hsup_tuyau)

def simulation():
  """
  met a jour l'etat du jeu
  """
  global d_fenetre, d_fbird, d_fbird_ancien, alt_fbird, alt_fbird_ancien, vx_fbird, vy_fbird, score
  if d_fenetre+L_FENETRE >= d_tuyaux[-1]+INTH_TUYAUX:
    ajoute_tuyau()
  # le score correspond a l'index du tuyau a tester
  if d_tuyaux[score]+L_TUYAU<d_fbird:
    score+=1
  if vx_fbird>0 and collision_fbird():
    vx_fbird=0
    if vy_fbird>0:
      vy_fbird=0
    draw_sol()
  if vx_fenetre != 0 and vx_fbird != 0:
    d_fenetre -= vx_fenetre
    d_fbird_ancien,alt_fbird_ancien=d_fbird,alt_fbird
    d_fbird += vx_fbird
    alt_fbird = max(H_FBIRD,alt_fbird+vy_fbird)
    vy_fbird += dy_gravite

def isect_rect(x1,y1,w1,h1,x2,y2,w2,h2):
  """
  teste si il y a une intersection entre les
  rectangle de largeur w1 hauteur h1 et coin superieur gauche (x1,y1)
  rectangle de largeur w2 hauteur h2 et coin superieur gauche (x2,y2)
  """
  max_gauche = max(x1,x2)
  min_droit = min(x1+w1,x2+w2)
  max_haut = max(y1,y2)
  min_bas = min(y1+h1,y2+h2)
  return max_gauche <= min_droit and max_haut <= min_bas

def collision_fbird():
  """
  teste si il y a collision
  entre Flappy Bird et les
  actuels tuyaux inferieur ou superieur
  """
  d_tuyau = d_tuyaux[score]
  hinf_tuyau = hinf_tuyaux[score]
  hsup_tuyau = hsup_tuyaux[score]
  #test intersection tuyau inferieur
  y_fbird = y_altitude(alt_fbird)
  isect_inf = isect_rect(d_tuyau, y_altitude(hinf_tuyau), L_TUYAU, hinf_tuyau, d_fbird, y_fbird, L_FBIRD, H_FBIRD)
  #test intersection tuyau superieur
  isect_sup=isect_rect(d_tuyau, y_fbird, L_TUYAU, hsup_tuyau - y_fbird, d_fbird, y_fbird, L_FBIRD, H_FBIRD)
  return isect_inf or isect_sup

def action():
  """
  effectue l'action correspondant a la touche pressee
  """
  try:
    global vx_fenetre, vy_fbird
    if vx_fenetre == 0:
      vx_fenetre = -2
      draw_sol()
    elif vx_fbird != 0:
      vy_fbird = 4
    else:
      print("score:")
      print(score)
      print("LOOSER")
      raise SystemExit
  except KeyboardInterrupt:
    action()

#-----------------
d_tuyaux = [L_FENETRE // 2]     #emplacements horizontaux des tuyaux
hinf_tuyaux = [HMIN_TUYAU + 20] #hauteurs des tuyaux inferieurs
hsup_tuyaux = [HMIN_TUYAU + 20] #hauteurs des tuyaux superieurs
score = 0                       # nombre de tuyaux franchis
d_fbird, alt_fbird = D_FBIRD, H_FOND
d_fbird_ancien, alt_fbird_ancien = d_fbird, alt_fbird
vx_fbird, vy_fbird = 2, 0
dy_gravite = -0.18
d_fenetre = 0
vx_fenetre = 0

#--------------
ajoute_tuyau()
draw_jeu()

while True:
 try:
   redraw_jeu()
   show_screen()
   simulation()
 except KeyboardInterrupt:
   action()
