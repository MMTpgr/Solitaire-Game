
# Description generale:
# Ce programme implémente le jeu "addiction solitaire" et l'affiche dans une
# page HTML via un serveur web. Les cartes affichées et leur arrangement sont
# représentées par des entiers stockés dans une liste. Pour appliquer les
# règles du jeu, le programme modifie le code HTML de la page web ainsi que
# la liste de l'arrangement des cartes principalement. Les cartes qui peuvent
# etre deplacees ont un fond de couleur vert vif. Le joueur doit donc placer
# les cartes au bon endroit sous la contrainte de 3 brassages possibles. Si
# Aucun déplacement n'est possible, le joueur doit brasser les cartes. Le
# joueur perds si il ne peut plus brasser les cartes et qu'aucun déplacement
# n'est possible. Un message de victoire est affiché si le joueur a gagné.
# Cette fonction permet de créer une liste qui permet d'associer les
# indices des cartes au fichier svg correspondant.




# Cette fonction permet de créer une liste qui permet d'associer les
# indices des cartes au fichier svg correspondant.
def generation_liste_fichiers():
   liste_types = ["C.svg","D.svg","H.svg","S.svg"]
   liste_cartes = list(range(2,11)) + ["J","K","Q"]
   liste_fichiers = ["absent.svg"]*4
   for valeur in range(12):
     for type in range(4):
       liste_fichiers.append(str(liste_cartes[valeur])+liste_types[type])
   return liste_fichiers


# Procédure qui, à l'appel génère un message qui indique que le joueur a gagné
# la partie ou qu'il l'a perdue suivant la valeur mise en paramètre. Elle ne
# prend aucun argument et ne retourne rien mais remplace le texte affiché.

def etat_actuel_partie(issue_partie):
   #Code HTML actuel
   texte = racine.innerHTML
   if issue_partie == "victoire":
     message = '''<p style = 'position:relative;top:20px'>
     Vous avez réussi! Bravo!</p>'''
   elif issue_partie == "perdu":
     message = '''<p style = 'position:relative;top:20px'>Vous n'avez
     pas réussi à placer toutes les cartes... Essayez à nouveau!</p>'''
   else:
     # cas_obligation indiquera que la fonction etat_actuel_partie a été
     # appelée dans le cadre d'une obligation de brasser les cartes
     # (l'utilité sera expliquée plus loin dans le code).
     global cas_obligation
     cas_obligation = True
     texte = racine.innerHTML # Code HTML actuel de la page web
     message = '''<p style = 'position:relative;top:20px'>Vous devez
     <button style = 'border: 1px solid black' onclick=
     'afficher_cartes(generateur_liste(arrangement_cartes_actuel))'>
     Brasser les cartes </button> </p>'''

   # Récupération du code HTML qui affiche le bouton "Nouvelle partie"
   fin_du_texte = texte[texte.find('<br>'):]
   # Remplacement du message actuel du jeu par le nouveau message
   # indiquant au joueur l'état de la partie (victoire défaite ou
   # obligation de brasser les cartes)
   racine.innerHTML = texte[:texte.find('<p')] + message + fin_du_texte



# Cette fonction vérifie la ligne que l'utilisateur a choisi pour voir si
# cette dernière contient 12 valeurs croissantes de même couleur et type
# ainsi qu'une case vide a la fin de la ligne. Si cela est vrai, elle renvoie
# un booleen True, sinon un booleen False. La fonction prend un int ligne
# représentant la ligne qu'on veut verifier et une liste qui contient
# l'arrangement des cartes.
def verification_ligne(ligne,liste):
  # On vérifie que la ligne contient 12 valeurs de même couleur et type
  # dans l'ordre croissant.
  if liste[13*ligne] // 4 == 0:
        return False
  for indice in range(11):
       # Vérification que la valeur actuelle et la suivantes sont successives.
       if liste[(13*ligne)+indice+1] - liste[(13*ligne)+indice] != 4:
            return False
     # Vérification de la présence d'une case vide à la fin de la ligne.
  if liste[(13*(ligne+1))-1] // 4 !=0 :
        return False
  return True


# Procedure qui prend deux numéros de cartes et qui permute leur placement
# et actualise l'affichage.
def changer_place(numero_carte_1,numero_carte_2):
   global arrangement_cartes_actuel
   global signal
   # Permutation des cartes
   carte_1 = arrangement_cartes_actuel.index(numero_carte_1)
   carte_2 = arrangement_cartes_actuel.index(numero_carte_2)
   arrangement_cartes_actuel[carte_1] = numero_carte_2
   arrangement_cartes_actuel[carte_2] = numero_carte_1
   # Variable qui indique que la fonction changer_place a été appelée
   # (le contexte sera explicité plus loin dans le code).
   signal = True
   # Actualisation de l'affichage
   afficher_cartes(arrangement_cartes_actuel)
   # Vérification de nouvelles cartes à jouer.
   verifier(arrangement_cartes_actuel)


# Procédure qui vérifie les cartes dont le numéro est 2 en fonction des cases
# vides dans la premiere colone. Elle parcours les premières cases de chaque
# ligne et vérifie si la case est vide, si c'est le cas, elle active la
# possibilié de cliquer sur un 2 puis vérifier si on peut déplacer d'autres
# cartes.
def deplacer_2():
   global arrangement_cartes_actuel
   # Parcours des 1ères cases de chaque ligne
   for colonne in range(0,52,13):
     # Si la case est vide.
     if arrangement_cartes_actuel[colonne] // 4 == 0:
       # Activation de tout les 2
       for valeur in range(4):
         id_case ="#case" + str(4+valeur)
         case = document.querySelector(id_case)
         carte_1 = str(arrangement_cartes_actuel[colonne])
         carte_2 = str(4+valeur)
         chaine = "changer_place("+carte_1+","+carte_2+")"
         case.setAttribute("onclick",chaine)
   # Vérification de nouvelles cartes à jouer.
   verifier(arrangement_cartes_actuel)

# Procédure qui permet d'activer le changement de position entre deux cartes
# lorsque l'utilisateur clique dessus. Elle prend deux valeurs deux cartes
# et permet de deplacer la carte valeur_2 à coté de valeur_1 lorsqu'elle est
# cliquée.
def changement_case(valeur_1,valeur_2):
   global arrangement_cartes_actuel
   str_val_2 = str(valeur_2)
   str_val_1 = str(valeur_1)
   id_case ="#case" + str_val_2
   case = document.querySelector(id_case)
   chaine = "changer_place("+str_val_1+","+str_val_2+")"
   # Activation du changement lorsque l'utilisateur clique dessus.
   case.setAttribute("onclick",chaine)



# Cette procédure vérifie lorsqu'il est possible de déplacer une carte dans la
# liste lorsqu'une carte possède une case vide à sa droite, elle permet de
# deplacer la carte suivante à cette case
def verifier(liste):
   global cartes_a_deplacer
   # Réinitialisation de la variable indiquant le nombre de cartes à déplacer
   cartes_a_deplacer = 0
   # Parcours de la liste pour vérifier si une carte peut être déplacée
   for indice in range(len(liste)-1):
     # Si la case actuelle n'est pas vide et que la suivante l'est
     if liste[indice+1]//4 == 0 and liste[indice]//4 !=0:
       # Si la carte suivante existe (Cas où on a un Q)
       if liste[indice]+4<52:
         case_choisie(liste[indice]+4)
         cartes_a_deplacer +=1
         changement_case(liste[indice+1],liste[indice]+4)


# Procédure qui appelle les deux procédures
# qui vérifient si des cartes peuvent être déplacées.
# Elle vérifie si on peut deplacer des cartes de 2,
# en suite si on peut déplacer les autres cartes.
def cartes_a_changer(liste):
 couleurs_2()
 verifier(liste)


# Procédure qui prend en paramètre l'identifiant de carte et la colorie en
# vert. Elle ne prend aucun argument et ne retourne rien mais modifie
# l'affichage de la carte en question
def case_choisie(identifiant):
 identifiant_case ="#case" + str(identifiant)
 case = document.querySelector(identifiant_case)
 case.setAttribute("style", "background-color: lime")


# Procédure qui prend l'identifiant d'une carte et retourne son expression
# HTML pour pouvoir l'afficher sur la page web.
def carte(id_carte):
   global liste # la liste des noms des cartes (sous la forme XX.svg)

   valeur_carte = liste[id_carte]
   # valeur HTML pour afficher la carte
   carte= '<td id="case'+str(id_carte)+'"><img src="cards/'+str(valeur_carte)
   carte+= '"></td>\n'
   return carte


# Fonction qui prend en paramètre une liste (la liste qui représente une des
# lignes de l'arrangement des cartes actuel). La fonction vérifie si il existe
# une suite de cartes consécutives et de même couleur (commençant par une
# carte de valeur2) et retourne l'indice (dit de référence) ou cette série
# se termine.
def determination_indice(liste):
   indice_de_reference = 0
   # Si la première carte de la ligne est un 2, indice_de_reference commence
   # a 1 pour bien inclure tous les éléments de la liste faisant partie de
   # la suite.
   if liste[0] == 4 or liste[0] == 5 or liste[0] == 6 or liste[0] == 7:
      indice_de_reference = 1
   # Les cartes consécutives (à partir de 2) et de même couleur sont separe
   # par 4 dans la liste des cartes originale
   for indice in range(len(liste)-1):
       if liste[indice] == liste[indice+1]-4:
          indice_de_reference +=1
       else:
          break
   return indice_de_reference

# Fonction qui prend en paramètres une liste (la liste qui représente
# l'arrangement des cartes actuel), une liste de cartes qui devra être
# insérée dans une sous liste de la liste originale (une des ligne du tableau),
# et rangée, un entier qui représente dans quelle ligne devra se situer la
# liste à insérer. Elle insère les éléments de liste à insérer au début de la
# liste originale et retourne cette dernière.
def reinsertion(liste_originale,liste_a_inserer,rangee):
   indice = 0
   # Insertion des éléments de la liste à insérer dans la liste originale
   for element in liste_a_inserer:
     liste_originale.insert(indice + rangee*13,element)
     indice+=1
   return liste_originale


# Procédure sans argument qui, a l'appel, décompose la liste de l'arrangement
# des cartes actuelle en 4 sous liste, vérifie si il existe des suites de
# cartes consécutives (à partir de 2) et de même couleur au début de chaque
# sous liste (fonction determination_indice), les suppriment de la liste de
# l'arrangement puis modifie cette liste, et réinsérer les listes supprimées
# dans la liste originale(fonction reinsertion). Le but plus tard sera de
# pouvoir brasser les cartes sans toucher aux cartes bien placées.
def generateur_liste(arrangement_cartes):
     liste_sous_listes = [] # Liste des quatres sous listes de l'arrangement
     liste_indices = [] # Liste des indice où une suite se termine
     suites =[] # Liste des cartes appartenant a une suite
     for indice in range(4):
         # Séparation de la liste de l'arrangement des cartes actuel en 4 sous
         # listes de longueur 13
         liste_sous_listes.append(arrangement_cartes[indice*13:(indice+1)*13])
         # Déterminer l'indice pour lequel la suite se termine pour chaque sous
         # liste
         liste_indices.append(determination_indice(liste_sous_listes[indice]))
         # Déterminer les cartes faisant partie de la suite et les regrouper
         # dans l'ordre dans une liste
         suites.append(liste_sous_listes[indice][:liste_indices[indice]])

     # Réunion de toutes les souslistes de cartes consecutives dans une seule
     # Liste et upression des cartes de cette liste de la liste de
     # L'arrangement actuel
     for liste in suites:
        for element in liste:
            arrangement_cartes.remove(element)


     # Brassage de la liste de l'arrangement actuel (sans les cartes faisant
     # partie d'une suite commancant par 2)
     taille_liste = len(arrangement_cartes)
     for indice in range(taille_liste) :
         indice_aleatoire = math.floor(random()*(taille_liste-1))
         actuel = arrangement_cartes[indice]
         arrangement_cartes[indice] = arrangement_cartes[indice_aleatoire]
         arrangement_cartes[indice_aleatoire] = actuel

     # Réinsertion des valeurs faisant partie d'une suite au début de chaque
     # ligne (sous liste) de manière respective
     for indice in range(4):
        reinsertion(arrangement_cartes,suites[indice],indice)
     return arrangement_cartes


# Procédure qui change la couleurs des cartes 2 lorsqu'il est possible
# de les déplacer. Elle vérifie si tout les cartes de valeurs 2 ne sont
# pas dans la première colonne, si c'est le cas, elle permet de deplacer
# tout les 2 quand le joueur clique dessus.
def couleurs_2():
   global arrangement_cartes_actuel
   cases = []
   # Valeurs de la première carte des 4 lignes.
   for position in range(0,52,13):
      cases.append(arrangement_cartes_actuel[position])

   # Si la valeur de toutes les premières cartes dans les lignes
   # sont toutes égales à 2, on ignore.
   if cases[0]//4==1 and cases[1]//4==1 and cases[2]//4==1 and cases[3]//4==1:
      pass
   # Cas où une case de la première colonne est vide.
   elif cases[0]//4==0 or cases[1]//4==0 or cases[2]//4==0 or cases[3]//4==0:
       # Possibilité de déplacer tout les 2
       for indice in range(4):  
         case_choisie(4+indice)
         # Appel de la procédure pour déplacer les 2 quand cliqués
         deplacer_2()

# Procédure qui prend en paramètre une liste qui représente l'arrangement des
# cartes actuel et génère le code HTML qui représente sur une page web
# l'arrangement des cartes et les cartes en elles-mêmes.
def assembler_cartes(liste):
   # Initialisation de la table des cartes à l'aide des balises HTML
   table = '<div id="jeu">\n<table>\n'

   # parcours des quatres tranches (de 13) de la liste des positions
   for rangee in range(4):
     table += '<tr>\n' # Début d'une ligne de tableau
     for colonne in liste[rangee*13:(rangee+1)*13]:
         table += carte(colonne)
     table += '</tr>\n' # Fin de la ligne de tableau
   return table
# Procédure qui prend en paramètre une liste de l'arrangement des cartes
# actuel et la représente sur le site web en modifiant directement le code
# HTML illustrant l'arrangement sauvegardé précédemment.
# La procédure ne retourne rien.
def afficher_cartes(arrangement):
    global racine
    global cartes_a_deplacer
    global nombre_brassage_restant
    global signal
    global cas_obligation
     # Si signal est True, la fonction afficher_cartes a été appelée dans le
     # cadre d'un changement de l'emplacement d'une carte, donc on ne soustrait
     # pas 1 du nombre de brassage restant.
    if not signal :
        nombre_brassage_restant -=1
    signal = False

    nouvel_assemblage = assembler_cartes(arrangement)
    texte_HTML = racine.innerHTML
     # Récupération de la partie du code HTML qui vient avant la définition du
    # tableau de cartes et ajout du nouveau tableau à la valeur HTML de la
    # racine.
    racine.innerHTML = texte_HTML[:texte_HTML.find('<div id="jeu">')]
    racine.innerHTML += nouvel_assemblage
    # Récupération du code HTML qui affiche le bouton "Nouvelle partie"
    # sur la page web
    fin_du_texte = texte_HTML[texte_HTML.find('<br>'):]
    # Le cas où un brassage standard est appelé
    if nombre_brassage_restant>0 and not cas_obligation:
         # Complétion du code HTML de la racine (pour afficher les deux boutons)
         racine.innerHTML+= texte_HTML[texte_HTML.find('<p '):]
         # Remplacement du nombre de brassage restant par le nouveau dans
         # l'affichage web.
         nbr_actuel = str(nombre_brassage_restant+1)
         racine.innerHTML=racine.innerHTML.replace(nbr_actuel + ' fois',
         str(nombre_brassage_restant) + ' fois')
         # Vérification de cartes à changer dans la liste
         cartes_a_changer(arrangement)

     # Le cas où un brassage est appelé quand l'utilisateur est obligé de
     # brasser les cartes
    elif nombre_brassage_restant>0 and cas_obligation:
         message = '''<p style = "position:relative;top:20px"> Vous pouvez
         encore <button style = "border: 1px solid black" onclick=
         "afficher_cartes(generateur_liste(arrangement_cartes_actuel))"> Brasser
         les cartes </button> '''
         message += str(nombre_brassage_restant)+' fois </p>'
         # Récupération de tout le code HTML qui vient avant le message qui
         # indique le nombre de brassage restant
         racine.innerHTML = racine.innerHTML[:racine.innerHTML.find('<p')] + '>'
         racine.innerHTML += message + fin_du_texte
         # Vérification de cartes à changer dans la liste
         verifier(arrangement)
         # Réinitialisation de la valeur de cas_obligation a False
         cas_obligation = False

     # Le cas où plus aucun brassage n'est possible.
    elif nombre_brassage_restant == 0:
       message = '''<p style = 'position:relative;top:20px'>Vous ne pouvez
       plus brasser les cartes</p>'''
       # Remplacement du message actuel du jeu par le nouveau message
       # (indiquant que le joueur ne peut plus brasser les cartes)
       racine.innerHTML+= message + fin_du_texte

   # Vérification de cartes à changer dans la liste
    cartes_a_changer(arrangement)
   # Si aucun déplacer n'est possible mais qu'il reste des brassages
   # disponibles, appel de la fonction obligation_brasser_les_cartes
    if cartes_a_deplacer == 0 and nombre_brassage_restant >0:
      etat_actuel_partie("obligation_brasser_les_cartes")
   # Si aucun déplacement n'est possible, et qu'il ne reste aucun brassage,
   # appel de la fonction partie_perdue
    elif cartes_a_deplacer == 0 and nombre_brassage_restant == 0:
      etat_actuel_partie("perdu")
   # Vérification d'une potentielle victoire.
    victoire = True
    for ligne in range(4):
       if verification_ligne(ligne,arrangement) == False:
          victoire = False
   # Cas où les 4 lignes sont toutes dans l'ordre correct
    if victoire :
      etat_actuel_partie("victoire")



# Fonction qui s'active quand la page HTML se charge complètement, elle
# contient le code HTML de la racine (la div #cb-body) elle fournit un premier
# assemblage des cartes une première fois, se charge de l'afficher sur la
# page web et ajoute au code HTML les deux boutons "afficher_cartes" et
# "nouvelle partie"
def init():
     global signal
     signal = False
     global cas_obligation
     cas_obligation = False
     global nombre_brassage_restant
     nombre_brassage_restant = 3
     global arrangement_cartes_actuel
     arrangement_cartes_actuel = list(range(52))
     global racine
     # La variable racine contiendra le code HTML de la div d'id "cb-body"
     racine = document.querySelector("#cb-body")
     # Initialisation du code HTML de la racine en spécifiant son style
     racine.innerHTML = """
     <style>
     #jeu table { float:none; }
     #jeu table td { border:0; padding:1px 2px; height:auto; width:auto; }
     #jeu table td img { height:130px; }
     </style>
     """
     # Ajout du premier assemblage de cartes du jeu au code HTML de la racine
     racine.innerHTML += assembler_cartes(generateur_liste(
     arrangement_cartes_actuel))
     # Ajout du bouton "afficher_cartes" ainsi que l'affichage du nombre de
     # Brassage restant restant au code HTML de la racine
     racine.innerHTML += '''<p style = "position:relative;top:20px"> Vous
     pouvez encore <button style = "border: 1px solid black"
     onclick="afficher_cartes(generateur_liste(arrangement_cartes_actuel))">
     Brasser les cartes </button> 3 fois </p>'''
     # Ajout du bouton "Nouvelle partie" au code HTML de la racine
     racine.innerHTML += '''<br><br><button style = "border: 1px solid black;
     position:relative;bottom:10px" id ="Nv_partie" onclick="init()">
     Nouvelle partie </button>
     '''
     # Ajout de quelques éléments de style pour embellir l'affichage web
     racine.setAttribute("style", '''margin-left:10px;font-size:14px;
     font-family:Arial''')
     # Vérification de potentielles cartes à changer dans la liste
     cartes_a_changer(arrangement_cartes_actuel)


# Création de la liste qui associe les cartes à leur fichiers.
liste = generation_liste_fichiers()
# Création de la variables pour savoir le nombre de cartes jouables
cartes_a_deplacer = 0



















