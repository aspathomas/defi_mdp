# Read the content of both files
with open('mdpTrouve.txt', 'r', encoding='utf-8') as file1:
    content1 = file1.read().lower().split()

with open('Ashley-Madison.txt', 'r', encoding='utf-8') as file2:
    content2 = file2.read().lower().split()

# Find common words
common_words = set(content1) & set(content2)
num_common_words = len(common_words)

print(f"\nNumber of common words: {num_common_words}\n")
print("Common words:", ', '.join(common_words))