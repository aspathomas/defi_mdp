import torch
import torch.nn as nn

characters = []
characters.append('€')
with open('occurrences.txt', 'r') as fichier:
    for ligne in fichier:
        characters.append(ligne[0])


nb_neuronne = 50
nb_neuronne_cacher = 100
emb = nn.Embedding(len(characters), nb_neuronne)
rnn = nn.RNN(nb_neuronne, nb_neuronne_cacher, batch_first=True)
linear = nn.Linear(nb_neuronne_cacher, len(characters))

model = torch.load('mdp.pth')
emb.load_state_dict(model['emb'])
rnn.load_state_dict(model['rnn'])
linear.load_state_dict(model['linear'])

nb_letter = 1000
generated_letters = []

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

# Save the generated letters to a file
with open('mdpTrouve.txt', 'w') as resultat:
    for caractere in generated_letters:
        if caractere == '€':
            resultat.write('\n')
        else:
            resultat.write(caractere)