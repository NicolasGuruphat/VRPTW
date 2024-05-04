# Avant propos

Les données qui ont servi l'analyse du recuit simulé ont été récoltées sur des ordinateurs différents, les temps d'exécution récoltés ne partagent donc pas tous le même référentiel matériel.  
L'ensemble des simulations a été faite à partir du produit cartésien de ces différents ensembles de valeurs pour les différents hyper-paramètres :  
- $\mu : \{0.5,0.6,0.7,0.75,0.8,0.85,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99\}$
- opérateurs de voisinage utilisés : {Relocate, Relocate + Exchange, Relocate + Cross-Exchange, Relocate + Exchange + Cross-Exchange, Relocate + Reverse, Relocate + Exchange + Cross-Exchange + Reverse}
- $$n_2 : \begin{cases} 10000,& si \space \mu \in \{0.5,0.6,0.7,0.75,0.8,0.85,0.9,0.91,0.92,0.93\} \\ 1000,& si \space \mu \in \{0.94,0.95,0.96,0.97,0.98,0.99\} \end{cases}$$
- $t_0 : \{3,4,5,6,7,8,9,10,15,20,25,30,40,50,60,70,80,90,100,150,200,300,400,500,1000\}$  

Pour des raisons logistiques (principalement de temps), seul une itération a été effectuée pour chaque combinaison d'hyper-paramètres, hormi pour $\mu = 0.5$ mais cela sera ignoré. $n_2$ a également été réduit pour des valeurs de $\mu$ élevées car le temps d'exécution devenait trop important ($n_1 = 301$ pour $\mu = 0.99$)  
Les simulations ont été effectuées à partir d'une solution aléatoire non-optimisée. La solution aléatoire donne la priorité aux clients qui attendent d'être livrés et ne se rend chez un client qui n'est pas encore prêt pour attendre uniquement s'il n'y a plus de clients en attente.

# Mise en place

Dans un premier temps le recuit simulé a été appliqué aux trente premiers clients du fichier `data_101.vrp` sans tenir compte des fenêtres de temps. La fonction de fitness a été choisie comme la somme des distances parcourues par les camions. Dans une perspective de valoriser un plus faible nombre de camion, une fonction de fitness integrant une pénalité pour chaque camion et une pénalité pour les camions avec trop de paquets restant a été expérimenter sans que cela n'apporte de bénéfice aux résultats car la distance à elle-seule pénalise les camions superflus à travers l'allé retour à l'entrepot qui en découle.  
Parmis les opérateurs de voisinage implémentables, seuls Relocate (inter et intra), Exchange (inter et intra), Cross-Exchange (intra) et Reverse (inter) ont été choisis. Parmis ces derniers l'usage d'un opérateur permettant de vider une route est important car la solution aléatoire initiale peut comporter des véhicules dispensables qui devront être supprimés pour se rapprocher d'une solution la plus optimale possible.  

# Influence et synergie des hyper-paramètres

L'objectif ultime serait de trouver une combinaison d'hyper-paramètres qui donne une bonne solution (de préférence une optimale) dans un temps le plus court possible. Pour cela, il serait intéressant de chercher combien de tours de recuit sont nécessaires pour atteindre notre objectif et surtout, comment déterminer cette valeur en fonction de la taille du jeu de données. Nous nous intéresserons donc à deux axes :
- Un $\mu$ grand (proche de 1) avec un $n_2$ petit
- Un $\mu$ petit (proche de 0.5 car 0 est trop faible) avec un $n_2$ grand

La principale différence entre ces deux cas et qu'avec un $\mu$ grand, les $n_1$ itérations auront des températures similaires d'un tour à l'autre alors que pour un $\mu$ faible, la température va drastiquement changée mais sur un moins grand nombre d'itérations (car $n_1$ sera plus petit car dépendant de $\mu$).  

Nous avons donc cherché quels hyper-paramètres influaient le plus sur la qualité de la solution. Nous avons pour cela utilisé une matrice de corrélation (cours d'Analyse des Données Multidimensionnelles qui nous est dispensé durant le S8). Cela nous a permis d'obtenir ceci :

MATRICE
-

EXPLICATIONS
-


À partir des données récoltées, en récupérant toutes les températures finales qui ont donné une solution optimale pour le jeu de données d'entrée. On en déduit qu'en moyenne $t_{n1} = !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!$ donne de bons résultats. Il est intéressant de noter que la température finale maximale donnant une solution optimale croît avec $\mu$, par exemple, elle est de :

| $\mu$ | $max(t_{n1})$ tel que $x$ est une solution optimale avec $x$ résultat du recuit simulé |
|---|---|
| 0.5 | 0.14536501951208458 |
| 0.6 | 0.1938200260161128 |
| 0.7 | 4.845500650402822 |
| 0.75 |  |
| 0.8 |  |
| 0.85 |  |
| 0.9 | 48.455006504028226 |
| 0.91 | 48.45500650402821 |
| 0.92 |  |
| 0.93 |  |
| 0.94 |  |
| 0.95 |  |
| 0.96 |  |
| 0.97 |  |
| 0.98 |  |
| 0.99 |  |

Il subsiste tout de même un biais qui est la qualité de la solution aléatoire qui peut influer sur la qualité de la solution en sortie, de ce fait, le tableau ci-dessus n'est qu'une possibilité et l'aléatoire du recuit simulé (choix du voisin) combiné à la qualité aléatoire de la solution initiale aurait très bien pu produire $t_{n1} = 100$ pour $\mu = 0.9$ par exemple.

TESTS SUR LE MU CALCULÉ
-

TESTS SUR GROS ECHANTILLONS
-

TESTS AVEC TW
-

# Difficultés et axes d'amélioration

Le plus gros frein durant nos expérimentations et notre analyse fut le temps d'exécution et donc le langage utilisé, même si ce choix était déjà controversé avant même le développement, nous avons quand même décidé de conserver le langage Python pour être certain de mener à bien le développement même si cela impactait négativement le temps nécessaire pour la génération de données.
Ce manque de temps qui en a résulté a donné lieu a un second obstacle, la quantité de données générées n'étaient pas assez importante pour pouvoir correctement illustrer des hypothèses ou interpréter les résultats avec le bon recul (par exemple une exécution pour un groupe d'hyper-paramètres n'est pas assez).