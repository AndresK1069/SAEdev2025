# Bzzz : règles du jeu

Paramètres entiers à définir :
NCASES = 15  
NFLEURS = 4  
NECTAR_INITIAL = 10  
MAX_NECTAR = 50  
TIME_OUT = 250  
COUT_PONTE = 5  
TIME_KO = 5  

## Résumé

Dans ce jeu, quatre joueurs s'affrontent en contrôlant des abeilles dont le but est de butiner des fleurs afin de ramener du nectar à la ruche. Malheureusement, quand les abeilles des deux joueurs se croisent il peut y avoir du grabuge, butiner c'est un métier dangereux. Les points de nectar déterminent la victoire, mais ce sont également eux qui permettent de pondre de nouvelles abeilles, et de se soigner. Il faudra donc opérer un équilibre entre accumuler du nectar pour s'approcher de la victoire et produire de nouvelles abeilles permettant la domination du terrain de jeu et donc, des fleurs et de leur précieux nectar.
À ces fins, les joueurs peuvent produire trois variétés d'abeilles différentes : les ouvrières, qui sont spécialisées dans le butinage des fleurs, les bourdons qui ne peuvent pas presque pas ramener de nectar mais sont sont des durs à cuire, et enfin les éclaireuses, qui permettent d'explorer et de prendre l'adversaire de vitesse... À vos ailes, que le meilleur bzzz !

## Détail des règles

### Le plateau de jeu

Le jeu se déroule sur une grille de NCASES fois NCASES cases numérotées à partir de 0. Dans les quatre coins se trouvent les ruches. Sur le plateau de jeu se trouvent des fleurs, sur des positions déterminées aléatoirement en début de partie, mais réparties de manière symétrique pour que chaque joueur ait affaire à la même disposition de son point de vue. Les joueurs ont visibilité et information complète sur :

- les informations de leurs ruches, leurs abeilles
- les positions des fleurs
- les positions de toutes les abeilles ennemies, leur état, le joueur qui les contrôle, leur variété (ouvrière, bourdon, éclaireuse)
Ce qui est caché :
- le nectar contenu sur les fleurs, dans le stock des autres joueurs, sur les abeilles des autres joueurs

Le fait que la carte soit symétrique donne de l'information car les fleurs situés en (x,y), en (NCASES-1-x,y), en (x, NCASES-1-y)  et en (NCASES-1-x,NCASES-1-y) ont initialement la même quantité de nectar.

### Le nectar

Les points de nectar peuvent se trouver en plusieurs endroits :

- sur une fleur, attendant d'être butinés
- sur les abeilles, en transport
- et dans une ruche, c'est le stock personnel de chaque joueur.

### Les abeilles

Chaque abeille est déterminée par les éléments suivants :

- sa variété : ouvrière, bourdon  ou éclaireuse , qui détermine ses caractéristiques :
  - possibilités de mouvement
  - force
  - quantité de nectar maximum

- la quantité de points de nectar qu'elle transporte sur elle, inférieure au maximum autorisé
- sa position, c'est-à-dire la case du plateau sur laquelle elle se trouve
- son état, qui peut être OK ou KO

Les abeilles sont bloquantes pour le déplacements, il ne peut y en avoir qu'une au maximum par case.

### Les fleurs

Les fleurs sont disposées sur une case et ne sont pas mobiles. Elles ne sont pas bloquantes pour les déplacements. Chaque fleur contient une certaine quantité de points de nectar, tirée aléatoirement au début du jeu. Le nectar ne se reforme pas et une fois récolté, il n'y en a plus. La quantité de nectar restant est une information cachée : le joueur saura qu'il n'y en a plus quand une abeille butine et que son total de nectar n'augmente pas.
La quantité initiale de nectar d'une fleur est comprise entre 1 et MAX_NECTAR.
Le nombre de fleurs pour un côté d'un joueur est défini par NFLEURS. Le nombre total de fleurs sur le plateau est donc NFLEURS*4.

### début du jeu

Le jeu commence avec aucune abeille en jeu et chaque joueur possede NECTAR_INITIAL points de nectars en stock.

### fin du jeu

Le jeu se termine quand une des conditions suivantes est remplie :

- il n'y a pas plus aucun point de nectar disponible dans les fleurs et sur les abeilles
- un joueur possède dans sa ruche plus de la moitié des points de nectar disponibles au départ (victoire blitzkrieg)
- le nombre de tours dépasse TIME_OUT
Les points de victoire récoltés dans la ruche (donc pas ceux sur les abeilles) font alors office de points de victoire pour déterminer le vainqueur.

### Les tours de jeu

Le jeu se déroule en alternant un tour pour chaque joueur. Chaque tour est effectué en 4 phases :

1) Ponte : chaque ruche peut produire une abeille, qui apparaît sur la case ruche, pour une quantité de nectar à payer, prise dans le stock.
2) Mouvement : chaque abeille peut bouger
3) Butinage
4) Escarmouches

Chaque abeille ne peut butiner que pendant le tour de son joueur, mais par contre chaque abeille peut participer à une escarmouche pendant le tour de chaque joueur !

### Ponte

Chaque joueur peut créer, pour COUT_PONTE unités de nectar de son stock, une abeille du type de son choix qui apparait sur sa ruche. La case de la ruche doit être vide d'abeilles pour que ce soit possible. L'abeille est tout de suite opérationnelle ce tour.

### Mouvement

Chaque abeille peut se déplacer, à chaque tour, d'une case. Le joueur choisit dans quel ordre les abeilles bougent. Les ouvrières et bourdons ne peuvent se déplacer que dans les 4 directions de base, alors que les éclaireuses peuvent également se déplacer en diagonale. La condition pour qu'un déplacement soit possible est que la case de destination soit valide (dans la grille), ne soit pas dans la zone de 4*4 cases contenant une ruche adverse dans son coin (zone d'exclusion) et ne contienne aucune abeille au moment du déplacement. Les fleurs n'empechent pas le déplacement.

### Butinage

Si une abeille ne bouge pas pendant un tour et qu'elle est sur une case fleur ou adjacente dans une des huit directions à cette case, elle butine : on transfère des points de nectar de la fleur dans la réserve personnelle de l'abeille, selon la règle suivante :

- Si la fleur contient au moins 2/3 de MAX_NECTAR, elle donne 3 points de nectar par butinage
- Si la fleur contient plus de 1/3 de MAX_NECTAR mais moins que 2/3, elle donne 2 points de nectar par butinage
- Si la fleur contient moins de 1/3 de MAX_NECTAR, elle donne 1 points de nectar par butinage.

Ces informations permettent au joueur de savoir à quel point une fleur contient encore du nectar ou non.

Chaque abeille a une réserve maximale qu'elle ne peut pas dépasser :
1 pour les bourdons
3 pour les éclaireuses
12 pour les ouvrières
Une abeille transportant déjà son maximum de nectar sur elle peut quand même butiner s'il reste du nectar sur la fleur, mais ce nectar sera perdu. Ce serait donc un acte de pur vandalisme, mais la guerre des abeilles est ce qu'elle est.
A la fin de cette phase, une abeille dans la zone de sa ruche (zone 4*4 contenant la ruche dans le coin) dépose automatiquement le nectar : tout son nectar est transféré de l'abeille vers le stock récolté du joueur.

### Escarmouches

Les points de force des abeilles sont :

éclaireuse 1
ouvrière 1
bourdon 5

Il y a exactement une escarmouche par abeille qui est en contact (les diagonales comptent) avec au moins une autre abeille ennemie. Cette escarmouche simule l'abeille qui se défend face au attaquantes. On va déterminer pour chaque abeille en escarmouche la probabilité qu'elle esquive ces attaques.

a) On détermine la force effective de chaque abeille par la formule
FE = F / K
où F est la force de l'abeille et K est le nombre d'abeilles ennemies qui sont en contact avec elle.

b) Pour chaque abeille, on détermine si elle parvient à esquiver l'attaque des adversaires adjacents. Pour cela, on compare la Force de l'abeille (F et pas FE) à la somme des FE des abeilles ennemies en contact (les attaquantes). La probabilité d'esquive de l'abeille est égale à :
F / (F +somme des FE ennemies). On détermine ensuite par un tirage aléatoire si l'abeille parvient à esquiver.

exemple deux abeilles A1 et A2 sont opposées à 3 abeilles adverses B1 B2 B3 selon le schéma suivant.
Entre parenthèses on écrit la force de l'abeille (A2 et B2 bourdons, les autres ouvrières)

A1(1) B1(1)  
A2(5) B2(1)  
      B3(5)  

les forces effectives sont  
1/2    1/2  
5/3    1/2  
       5/2  

la probabilité d'esquive de A1 est de  1 / (1 + 1/2 + 1/2) = 1/2
la probabilité d'esquive de A2 est de  5 / (5 + 1/2 + 1/2 + 5/2) = 10/17
la probabilité d'esquive de B1 est de  1 / (1 + 1/2 + 5/3) = 6/19
la probabilité d'esquive de B2 est de  1 / (1 + 1/2 + 5/3) = 6/19
la probabilité d'esquive de B3 est de  5 / (5 + 5/3) = 3/4

Note : il serait préférable de faire des calculs exacts.

Une fois la probabilité d'esquive déterminée, on tire pour chaque abeille un nombre réel au hasard dans l'intervalle [0,1]. Si ce nombre est inférieur à la valeur de probabilité calculée, l'esquive est réussie, et sinon elle est ratée et l'abeille doit subir les conséquences.

Exemple : une abeille a une probabilité d'esquive de 3/4 = 0,75. On tire un nombre réel au hasard : si on tire 0.22874, l'esquive est réussie, et si on tire 0.943421, l'esquive est ratée.

c) Les conséquences des attaques sont traitées simultanément une fois toutes les esquives du tour tentées : toutes les abeilles ayant raté leurs esquives subissent les conséquences à cet instant.

### conséquences de l'escarmouche

Une abeille qui a raté son esquive :

- perd son nectar transporté
- devient KO pour les prochains TIME_KO tours de jeu de son propriétaire.

Une abeille KO occupe toujours sa case et la bloque donc, mais elle est totalement inactive : elle ne peut ni bouger ni butiner ni participer aux escarmouches.
