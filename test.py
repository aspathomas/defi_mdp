# Read the content of both files
with open('mdpTrouve.txt', 'r', encoding='utf-8') as file1:
    content1 = file1.read().lower().split()
    
# Display total words in file1
total_words_file1 = len(content1)
print(f"Total de mots de passe : {total_words_file1}\n")

with open('Ashley-Madison.txt', 'r', encoding='utf-8') as file2:
    content2 = file2.read().lower().split()

# Find common words
common_words = set(content1) & set(content2)
num_common_words = len(common_words)

print(f"\nNombre de mots communs: {num_common_words}\n")
print("Mots communs:", ', '.join(common_words))