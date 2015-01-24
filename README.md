ProjetX
=======
Map testées : (AmbianceTeam VS VieuxSac)
 2, 3, 4, 5, 6, 7, 8

Sur la map 1, la vieille IA gagne
Sur la 7, la vieille gagne à peu près 1 fois sur 2



Pour lancer un match entre l'IA actuelle et la vieille IA :

./poooserver.py -s 2 -r 2 -P 9876

./pooobot.py -s localhost:9876 -b AmbianceTeam Destructor     (IA actuelle)
./pooobot.py -s localhost:9876 -b VieuxSac Vieux                (vieille IA)


