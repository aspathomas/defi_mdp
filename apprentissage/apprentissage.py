import torch
import torch.nn as nn
import torch.optim as optim

characters = []
characters.append('€')
with open('occurrences.txt', 'r') as fichier:
    for ligne in fichier:
        characters.append(ligne[0])

motDePasse = ''
with open('train.txt', 'r') as fichier:
    for count, ligne in enumerate(fichier):
        ligne = ligne.rstrip('\n')
        motDePasse += ligne + '€'

l = [characters.index(char) for char in motDePasse if char in characters]

nb_neuronne = 50
nb_neuronne_cacher = 100
nb_couche = 0

emb = nn.Embedding(len(characters), nb_neuronne)
rnn = nn.RNN(nb_neuronne, nb_neuronne_cacher, batch_first=True)
linear = nn.Linear(nb_neuronne_cacher, len(characters))

# ajoute des couches rnn
rnn_layers = nn.ModuleList([nn.RNN(nb_neuronne_cacher, nb_neuronne_cacher, batch_first=True) for _ in range(nb_couche)])

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(list(emb.parameters()) + list(rnn.parameters()) + list(linear.parameters()), lr=0.001)

num_epochs = 7

# Boucle d'entraînement
for epoch in range(num_epochs):
    print(f'Epoch {epoch + 1}/{num_epochs}')

    # Réinitialisation de l'état caché pour chaque époque
    h = torch.zeros(nb_couche + 1, 1, nb_neuronne_cacher)
    
    correct_predictions = 0
    total_predictions = 0
    # Itérer à travers vos données
    for i in range(len(l)-1):
        input_index = l[i]
        target_index = l[i+1]
        
        input_tensor = torch.tensor([input_index])
        target_tensor = torch.tensor([target_index])

        optimizer.zero_grad()

        out = emb(input_tensor)
        out, h = rnn(out)

        for rnn_layer in rnn_layers:
            out, h = rnn_layer(out)

        logits = linear(h.view(1, -1))

        loss = criterion(logits, target_tensor)

        loss.backward()
        optimizer.step()
        
        # Suivi des prédictions correctes
        _, predicted_indices = torch.max(logits, 1)
        correct_predictions += (predicted_indices == target_tensor).sum().item()
        total_predictions += target_tensor.size(0)

    # Calculer et imprimer le pourcentage de prédictions correctes
    accuracy_percentage = (correct_predictions / total_predictions) * 100
    print(f'Accuracy: {accuracy_percentage:.2f}%')



# Sauvegarder le modèle
torch.save({
    'emb': emb.state_dict(),
    'rnn': rnn.state_dict(),
    'linear': linear.state_dict(),
}, 'mdp.pth')   
