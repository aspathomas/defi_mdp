import torch
import torch.nn as nn

characters = []
characters.append('€')
with open('occurrences.txt', 'r') as fichier:
    for ligne in fichier:
        characters.append(ligne[0])

# Permet de récupérer qu'un nomber fixe de ligne
nbLine= 375852
nbSample = 100000
gap = int(nbLine/nbSample)
lineToTake = gap

motDePasse = ''
with open('Ashley-Madison.txt', 'r') as fichier:
    for count, ligne in enumerate(fichier):
        if count == lineToTake:
            ligne = ligne.rstrip('\n')
            motDePasse += ligne + '€'
            lineToTake += gap

print(motDePasse)
l = [characters.index(char) for char in motDePasse if char in characters]
print(characters)

t = torch.tensor(l)

emb = nn.Embedding(len(characters), 3)

out = emb(t)

rnn = nn.RNN(3, 10, batch_first=True)

out, h = rnn(out)

linear = nn.Linear(10, len(characters))

letter = linear(h.view(1, -1)) 

probabilities = nn.functional.softmax(letter, dim=1)

# Generate letters
with torch.no_grad():
    sampled_char_indices = torch.multinomial(probabilities, 1000000, replacement=True).squeeze()
    generated_letters = [characters[idx] for idx in sampled_char_indices]

with open('mdpTrouve.txt', 'w') as resultat:
    for caractere in generated_letters:
        if caractere == '€':
            resultat.write('\n')
        else:
            resultat.write(caractere)


        
