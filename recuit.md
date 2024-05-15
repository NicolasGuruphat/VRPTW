# Avant propos

Les données qui ont servi l'analyse du recuit simulé ont été récoltées sur des ordinateurs différents, les temps d'exécution récoltés ne partagent donc pas tous le même référentiel matériel.  
L'ensemble des simulations a été faite à partir du produit cartésien de ces différents ensembles de valeurs pour les différents hyper-paramètres :  
- $\mu : \{0.5,0.6,0.7,0.75,0.8,0.85,0.9,0.91,0.92,0.93,0.94,0.95,0.96,0.97,0.98\}$
- opérateurs de voisinage utilisés : {Relocate, Relocate + Exchange, Relocate + Cross-Exchange, Relocate + Exchange + Cross-Exchange, Relocate + Reverse, Relocate + Exchange + Cross-Exchange + Reverse}
- $$n_2 : \begin{cases} 10000,& si \space \mu \in \{0.5,0.6,0.7,0.75,0.8,0.85,0.9,0.91,0.92,0.93\} \\ 1000,& si \space \mu \in \{0.94,0.95,0.96,0.97,0.98\} \end{cases}$$
- $t_0 : \{3,4,5,6,7,8,9,10,15,20,25,30,40,50,60,70,80,90,100,150,200,300,400,500,1000\}$  

Pour des raisons logistiques (principalement de temps), seul une itération a été effectuée pour chaque combinaison d'hyper-paramètres, hormi pour $\mu = 0.5$ mais cela sera ignoré. $n_2$ a également été réduit pour des valeurs de $\mu$ élevées car le temps d'exécution devenait trop important ($n_1 = 149$ pour $\mu = 0.98$)  
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

$ \begin{pmatrix}
1.00 & 0.00 & -0.00 & 0.00 & -0.02 & -0.25 & -0.03 & 0.01 & 0.10 \\
0.00 & 1.00 & 0.00 & 1.00 & -0.00 & 0.35 & 0.32 & 0.12 & -0.04 \\
-0.00 & 0.00 & 1.00 & 0.00 & 0.01 & -0.12 & 0.08 & -0.38 & -0.31 \\
0.00 & 1.00 & 0.00 & 1.00 & -0.00 & 0.35 & 0.32 & 0.12 & -0.04 \\
-0.02 & -0.00 & 0.01 & -0.00 & 1.00 & -0.02 & 0.01 & 0.00 & -0.03 \\
-0.25 & 0.35 & -0.12 & 0.35 & -0.02 & 1.00 & -0.19 & 0.37 & 0.12 \\
-0.03 & 0.32 & 0.08 & 0.32 & 0.01 & -0.19 & 1.00 & -0.17 & 0.05 \\
0.01 & 0.12 & -0.38 & 0.12 & 0.00 & 0.37 & -0.17 & 1.00 & -0.03 \\
0.10 & -0.04 & -0.31 & -0.04 & -0.03 & 0.12 & 0.05 & -0.03 & 1.00 
\end{pmatrix}  $

avec, dans l'ordre : $mu$, la température finale, les opérateurs utilisés, la température initiale, la fitness initiale, la fitness finale, le nombre d'itérations avant d'atteindre le meilleur minimum calculé, le nombre de camions en sortie, le temps d'exécution.

On peut en extraire quelques valeurs :
- 0.35 : la corrélation entre la température finale et la fitness finale
- 0.32 : la température finale et le nombre d'itérations avant le meilleur minimum
- -0.38 : les opérateurs utilisés et le nombre de camions
- -0.31 : les opérateurs utilisés et le temps d'exécution
- 0.35 : la température intiale et la fitness finale
- 0.32 : la température initiale et le nombre d'itérations avant le meilleur minimum
- 0.37 : la fitness finale et le nombre de camions

Certains critères ne sont pas à leur avantage à cause de la façon dont les données ont été générées. Par exemple la température initiale qui est aléatoire ne peut pas être correctement corrélée à un autre critère avec des hyper-paramètres changeant à chaque itération.  
Le plus intéressant est d'observer que la température finale (et intiale car $t_{n1} = \mu^{n_1}\times t_0$), on en déduit donc qu'en déterminant la plage de températures finales qui donnent une solution optimale, on peut déterminer le $\mu$ adéquat.  
La corrélation entre les opérateurs utilisés et le nombre de camions a un sens puisque la capacité à vider une route dépend des opérateurs et influe sur le nombre de camions.  
Les opérateurs utilisés et le temps d'exécution est aussi logique car certains opérateurs sont plus gourmands en nombre de temps processeur (cross-exchange par exemple). L'objectif seront donc de trouver le groupe d'opérateurs demandant le moins de temps mais permettant de réduire le nombre de camions.  
Nous avons également expliqué que la fitness était intrinsèquement reliée aux nombres de camions, il est donc logique de voir ces derniers corrélés.  
Toutes les corrélations abordées ci-dessus étaient cohérentes et/ou attendues. Cependant, le fait que la température finale/initiale soit corrélée au nombre d'itérations avant le meilleur minimum, et cela avec le même signe (positif) que la température et la fitness, est très intéressant car on peut donc espérer avoir une bonne solution avec un nombre d'itérations limitées !

Nous allons donc nous intéressé à quelques unes de ces corrélations.

## Température finale et fitness finale

À partir des données récoltées, en récupérant toutes les températures finales qui ont donné une solution optimale pour le jeu de données d'entrée. On en déduit qu'en moyenne $t_{n1} = 0.8624991157717019$ donne de bons résultats. Il est intéressant de noter que la température finale maximale donnant une solution optimale croît avec $\mu$, par exemple, elle est de :

| $\mu$ | $max(t_{n1})$ tel que $x$ est une solution optimale avec $x$ résultat du recuit simulé |
|---|---|
| 0.5 | 0.14536501951208458 |
| 0.6 | 0.1938200260161128 |
| 0.7 | 4.845500650402822 |
| 0.75 | 14.536501951208459 |
| 0.8 | 48.45500650402821 |
| 0.85 | 48.4550065040282 |
| 0.9 | 48.455006504028226 |
| 0.91 | 48.45500650402821 |
| 0.92 | 48.45500650402819 |
| 0.93 | 48.455006504028205 |
| 0.94 | 24.22750325201411 |
| 0.95 | 14.536501951208459 |
| 0.96 | 7.268250975604232 |
| 0.97 | 24.227503252014102 |
| 0.98 | 2.9073003902416916 |

Il subsiste tout de même un biais qui est la qualité de la solution aléatoire qui peut influer sur la qualité de la solution en sortie, de ce fait, le tableau ci-dessus n'est qu'une possibilité et l'aléatoire du recuit simulé (choix du voisin) combiné à la qualité aléatoire de la solution initiale aurait très bien pu produire $t_{n1} = 100$ pour $\mu = 0.9$ par exemple.

Nous noterons également que la corrélation entre la température finale et la fitness finale est très importante pour les $\mu$ petits jusqu'au passage de 0.75 à 0.85 où la corrélation passe de 0.63 à 0.15. La corrélation pour $\mu = 0.5$  et $\mu = 0.6$ sont respectivement de 0.86 et 0.88, élément important car si l'objectif est d'arriver à une température finale inférieure à 1 avec une température intiale calculée, plus le jeu de données en entrée sera grand, plus la température intiale risque d'être élevée et donc plus $\mu$ devra s'éloigner de 1 ($t_{n1}=\mu^{n1}\times t_0$). En combinant ces deux aspects, on peut aisément supposer que travailler avec des $\mu$ petits présentent un intérêt.

Nous allons donc chercher à calculer $\mu$ en fonction de $t_{n1}$ et $t_0$ :
$$
t_{n1} = \mu^{n1} \times t_0
\newline \Leftrightarrow

t_{n1} = \mu^{\frac{\ln(\frac{\ln(0.8)}{\ln(0.01)})}{\ln(\mu)}} \times t_0
\newline \Leftrightarrow

\ln(t_{n1}) = \ln(\mu^{\frac{\ln(\frac{\ln(0.8)}{\ln(0.01)})}{\ln(\mu)}} \times t_0)
\newline \Leftrightarrow

\ln(t_{n1}) = \ln(\mu^{\frac{\ln(\frac{\ln(0.8)}{\ln(0.01)})}{\ln(\mu)}}) + \ln(t_0)
\newline \Leftrightarrow

\ln(t_{n1}) = \frac{\ln(\frac{\ln(0.8)}{\ln(0.01)})}{\ln(\mu)} \times \ln(\mu) + \ln(t_0)
\newline \Leftrightarrow

\ln(t_{n1}) = \ln(\frac{\ln(0.8)}{\ln(0.01)}) + \ln(t_0)
$$
Nous arrivons donc à une impasse dans ce cas, cela est logique car il existe une infinité de solutions pour $t_{n1} = \mu^{\frac{\ln(\frac{\ln(0.8)}{\ln(0.01)})}{\ln(\mu)}} \times t_0$  
Nous allons donc fixer calculer $\mu$ à partir de $t_{n1}$, $t_0$ et $n_1$ :

$$
t_{n_1} = \mu^{n_1} \times t_0
\newline \Leftrightarrow

\ln(t_{n_1}) = \ln(\mu^{n_1} \times t_0)
\newline \Leftrightarrow

\ln(t_{n_1}) = \ln(\mu^{n_1}) + \ln(t_0)
\newline \Leftrightarrow

\ln(t_{n_1}) = n_1 \times \ln(\mu) + \ln(t_0)
\newline \Leftrightarrow

\ln(t_{n_1}) - \ln(t_0) = n_1 \times \ln(\mu) 
\newline \Leftrightarrow

\frac{\ln(t_{n_1}) - \ln(t_0)}{n_1} = \ln(\mu) 
\newline \Leftrightarrow

e^{\frac{\ln(t_{n_1}) - \ln(t_0)}{n_1}} = e^{\ln(\mu)} 
\newline \Leftrightarrow

\mu = e^{\frac{\ln(t_{n_1}) - \ln(t_0)}{n_1}}
$$

Nous avons $t_0 = \frac{-\Delta f}{\ln(0.8)}$ et $t_{n_1} = 0.86$. Reste à déterminer $t_{n_1}$.  
Pour cela, il faudrait trouver une valeur qui dépende de la taille de l'entrée. Plus la taille de l'entrée est grande, plus l'écart entre la fitness de la meilleure solution et celle de la pire est grand ou au moins constant (Raisonnement par l'absurde, si la différence entre la fitness de la meilleure solution et celle de la pire diminuait quand la taille de l'entrée augmente, alors la pire solution serait égale/semblable à la meilleure pour une taille d'entrée $x_{k}$ avec $k \longrightarrow \infty$ **et donc aussi pour $x_{k+1}$ !** Hors cela est vraie pour un et deux clients mais par pour trois alors c'est absurde). $\Delta f$ calculé à partir de solutions aléatoires pourrait donc être une bonne piste, il est, cependant, trop élevé pour être utilisé tel quel. Il existe plusieurs fonctions permettant de réduire celle valeur pour éviter un trop grand nombres d'itérations tout en évitant de trop rapidement converger vers l'infini : racine carrée et logarithme néperien. Nous continuerons donc avec $n_1 = \sqrt{|\Delta f|}$ ou $n_1 = \ln{|\Delta f|}$

Si on implémente cela, dans le cas des trente premiers clients du fichier 101, on constate facilement que $n_1$ est très voire trop petit si calculé avec $ln$ (environ 3-4) et la solution finale peine à avoir une fitness en dessous de 400 alors que l'optimale est d'environ 358 contrairement à $\sqrt{}$, pour laquelle les valeurs de $n_1$ sont plus correctes (6-8) et où l'optimale est parfois atteint (environ une fois sur dix dans le cas présent). On remarque que c'est discutablement efficace pour un petit jeu de données.  
Si on reprend les cent clients du fichier data101, $\Delta f$ est bien évidemment plus élevé et donc $n_1$ aussi. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

TESTS SUR LE MU CALCULÉ
-

## Température finale et nombre d'itérations avant le meilleur minimum

## Le choix des opérateurs

TESTS SUR GROS ECHANTILLONS
-

TESTS AVEC TW
-
La sélection aléatoire d'un voisin implique que l'on doit chercher un voisin valide (qui respecte les contraites temporelles, de capacité). Ces voisins sont moins nombreux avec les fenêtres de temps et donc la recherche dure plus longtemps. Cela a donc un impacte important que n'a pas un Tabu qui cherche tous les voisins.

# Difficultés et axes d'amélioration

Le plus gros frein durant nos expérimentations et notre analyse fut le temps d'exécution et donc le langage utilisé, même si ce choix était déjà controversé avant même le développement, nous avons quand même décidé de conserver le langage Python pour être certain de mener à bien le développement même si cela impactait négativement le temps nécessaire pour la génération de données.  
Ce manque de temps qui en a résulté a donné lieu a un second obstacle, la quantité de données générées n'étaient pas assez importante pour pouvoir correctement illustrer des hypothèses ou interpréter les résultats avec le bon recul (par exemple une exécution pour un groupe d'hyper-paramètres n'est pas assez).  
Nous avons également rencontré un problème avec $\mu = 0.99$ qui créait parfois une erreur (qui n'était pas forcément la même à chaque fois) lors de l'exécution du recuit, le problème racine n'étant pas flagrant, nous n'avons pas prioriser ce fait et avons préféré privilégier la suite de l'analyse.  
Une optimisation/amélioration du code serait également pertinente pour éviter les nombreux cas où le recuit fonctionnait sur un temps anormal (plus d'un quart d'heure pour la sélection d'un voison), pour régler cela, nous avons mis en place une durée maximale (trois minutes) pour la sélection du voisin aléatoire et du tour de boucle $n_1$ (donc les $n_2$ itérations).