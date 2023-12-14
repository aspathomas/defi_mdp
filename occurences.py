
with open('Ashley-Madison.txt', 'r') as fichier:
    occurrences = {}
    for ligne in fichier:
        for caractere in ligne:
            if caractere != '\n':
                occurrences[caractere] = occurrences.get(caractere, 0) + 1

# Trier les caractères par nombre d'occurrences (du plus fréquent au moins fréquent)
occurrences = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)

# Écrire les occurrences dans un nouveau fichier
with open('occurrences.txt', 'w') as resultat:
    for caractere, occurrence in occurrences:
        resultat.write(f"{caractere}: {occurrence}\n")