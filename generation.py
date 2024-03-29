import torch
import torch.nn as nn
import sys

# récupérer les caractères
characters = []
characters.append('€')
with open('apprentissage/occurrences.txt', 'r') as fichier:
    for ligne in fichier:
        characters.append(ligne[0])

nb_neuronne = 50
nb_neuronne_cacher = 100
emb = nn.Embedding(len(characters), nb_neuronne)
rnn = nn.RNN(nb_neuronne, nb_neuronne_cacher, batch_first=True)
linear = nn.Linear(nb_neuronne_cacher, len(characters))

# Chargement du modèle
model = torch.load('mdp.pth')
emb.load_state_dict(model['emb'])
rnn.load_state_dict(model['rnn'])
linear.load_state_dict(model['linear'])

nb_letter = int(sys.argv[1])
generated_letters = []

# générer 30 chaines de caractère avec nb_letter
for current_index in range(30):
    with torch.no_grad():
        sampled_char_indices = torch.zeros(nb_letter, dtype=torch.long)

        for i in range(nb_letter):
            input_tensor = torch.tensor([current_index])
            out = emb(input_tensor)
            out, h = rnn(out)
            logits = linear(h.view(1, -1))
            probabilities = nn.functional.softmax(logits, dim=1)
            current_index = torch.multinomial(probabilities, 1).item()
            sampled_char_indices[i] = current_index

        generated_letters += [characters[idx] for idx in sampled_char_indices]

# Ecrire les résultats dans un fichier
with open(sys.argv[2] + '.txt', 'w') as resultat:
    for caractere in generated_letters:
        if caractere == '€':
            resultat.write('\n')
        else:
            resultat.write(caractere)