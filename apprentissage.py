import torch
import torch.nn as nn
import torch.optim as optim

characters = []
characters.append('€')
with open('occurrences.txt', 'r') as fichier:
    for ligne in fichier:
        characters.append(ligne[0])

# Permet de récupérer qu'un nomber fixe de ligne
nbLine= 375852
nbSample = 10000
gap = int(nbLine/nbSample)
lineToTake = gap

motDePasse = ''
with open('Ashley-Madison.txt', 'r') as fichier:
    for count, ligne in enumerate(fichier):
        if count == lineToTake:
            ligne = ligne.rstrip('\n')
            motDePasse += ligne + '€'
            lineToTake += gap

l = [characters.index(char) for char in motDePasse if char in characters]

emb = nn.Embedding(len(characters), 3)
rnn = nn.RNN(3, 10, batch_first=True)
linear = nn.Linear(10, len(characters))

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(list(emb.parameters()) + list(rnn.parameters()) + list(linear.parameters()), lr=0.001)

num_epochs = 5

# Boucle d'entraînement
for epoch in range(num_epochs):
    print(f'Epoch {epoch + 1}/{num_epochs}')

    # Réinitialisation de l'état caché pour chaque époque
    h = torch.zeros(1, 1, 10)

    # Itérer à travers vos données
    for i in range(len(l)-1):
        input_index = l[i]
        target_index = l[i+1]
        
        input_tensor = torch.tensor([input_index])
        target_tensor = torch.tensor([target_index])

        optimizer.zero_grad()

        out = emb(input_tensor)
        out, h = rnn(out)
        logits = linear(h.view(1, -1))

        loss = criterion(logits, target_tensor)

        loss.backward()
        optimizer.step()


# Sauvegarder le modèle
torch.save({
    'embedding_state_dict': emb.state_dict(),
    'rnn_state_dict': rnn.state_dict(),
    'linear_state_dict': linear.state_dict(),
}, 'mdp.pth')

# Générer des lettres
nb_letter = 100000
with torch.no_grad():
    sampled_char_indices = torch.zeros(nb_letter, dtype=torch.long)
    current_index = l[0]

    for i in range(nb_letter):
        input_tensor = torch.tensor([current_index])
        out = emb(input_tensor)
        out, h = rnn(out, h)
        logits = linear(h.view(1, -1))
        probabilities = nn.functional.softmax(logits, dim=1)
        current_index = torch.multinomial(probabilities, 1).item()
        sampled_char_indices[i] = current_index

    generated_letters = [characters[idx] for idx in sampled_char_indices]

with open('mdpTrouve.txt', 'w') as resultat:
    for caractere in generated_letters:
        if caractere == '€':
            resultat.write('\n')
        else:
            resultat.write(caractere)


        
