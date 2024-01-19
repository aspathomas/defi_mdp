import sys
# Lire le contenu des deux fichiers
with open(sys.argv[1] + '.txt', 'r', encoding='utf-8') as file1:
    content1 = file1.read().lower().split()
    
# Afficher le nombre total de mots dans le fichier 1
total_words_file1 = len(content1)
print(f"Total de mots de passe : {total_words_file1}\n")

with open('eval.txt', 'r', encoding='utf-8') as file2:
    content2 = file2.read().lower().split()

# Trouver des mots communs
common_words = set(content1) & set(content2)
num_common_words = len(common_words)

print(f"\nNombre de mots de passe trouvé: {num_common_words}\n")
print(f"\nPourcentage: {num_common_words/total_words_file1*100:.2f}%\n")
print("Mots de passe:", ', '.join(common_words))