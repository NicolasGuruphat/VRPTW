# Avant propos

Les données qui ont servi l'analyse du recuit simulé ont été récoltées sur des ordinateurs différents, les temps d'exécution récoltés ne partagent donc pas tous le même référentiel matériel.  
L'ensemble des simulations a été faite à partir du produit cartésien de ces différents ensembles de valeurs pour les différents hyper-paramètres :  
- $\mu : \{0.5,0.6,0.7,0.75,0.8,0.85,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98,0.99\}$
- opérateurs de voisinage utilisés : {Relocate, Relocate + Exchange, Relocate + Cross-Exchange, Relocate + Exchange + Cross-Exchange, Relocate + Reverse, Relocate + Exchange + Cross-Exchange + Reverse}
- $n_2 : \{10000\}$
- $t_0 : \{3,4,5,6,7,8,9,10,15,20,25,30,40,50,60,70,80,90,100,150,200,300,400,500,1000\}$  

Pour des raisons logistiques (principalement de temps), seul une itération a été effectuée pour chaque combinaison d'hyper-paramètres, hormi pour $\mu = 0.5$ mais cela sera ignoré.  
Les simulations ont été effectuées à partir d'une solution aléatoire non-optimisée.

SAUF # 0.95 0.97 0.99 0.94 0.96 0.98
-

# Mise en place

Dans un premier temps le recuit simulé a été appliqué aux trente premiers clients du fichier `data_101.vrp` sans tenir compte des fenêtres de temps. La fonction de fitness a été choisie comme la somme des distances parcourues par les camions. Dans une perspective de valoriser un plus faible nombre de camion, une fonction de fitness integrant une pénalité pour chaque camion et une pénalité pour les camions avec trop de paquets restant a été expérimenter sans que cela n'apporte de bénéfice aux résultats car la distance à elle-seule pénalise les camions superflus à travers l'allé retour à l'entrepot qui en découle.  
Parmis les opérateurs de voisinage implémentables, seuls Relocate (inter et intra), Exchange (inter et intra), Cross-Exchange (intra) et Reverse (inter) ont été choisis. Parmis ces derniers l'usage d'un opérateur permettant de vider une route est important car la solution aléatoire initiale peut comporter des véhicules dispensables qui devront être supprimés pour se rapprocher d'une solution la plus optimale possible.  

# Influence et synergie des hyper-paramètres

L'objectif ultime serait de trouver une combinaison d'hyper-paramètres qui donne une bonne solution (de préférence l'optimale) dans un temps le plus court possible. Pour cela, il serait intéressant de chercher combien de tours de recuit sont nécessaires pour atteindre notre objectif et surtout, comment déterminer cette valeur en fonction de la taille du jeu de données. Nous nous intéresserons donc à deux axes :
- Un $\mu$ grand (proche de 1) avec un $n_2$ petit
- Un $\mu$ petit (proche de 0.5 car 0 est trop faible) avec un $n_2$ grand

La principale différence entre ces deux cas et qu'avec un $\mu$ grand, les $n_1$ itérations auront des températures similaires d'un tour à l'autre alors que pour un $\mu$ faible, la température va drastiquement changée mais sur un moins grand nombre d'itérations (car $n_1$ sera plus petit car dépendant de $\mu$).

# Difficultés et axes d'amélioration