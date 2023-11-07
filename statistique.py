import csv
with open('Ashley-Madison.txt', 'r') as file:
    statistics = {}
    tot_line = 0
    for line in file:
        tot_line +=1
        num_chars = len(line.strip())
        if num_chars in statistics:
            statistics[num_chars] += 1
        else:
            statistics[num_chars] = 1

statistics = dict(sorted(statistics.items(), key=lambda item: item[0]))

with open('statistique.csv', 'w', newline='') as result_file:
    writer = csv.writer(result_file)
    writer.writerow(['Caractères', 'Nombre de mots'])  # Write header row

    for num_chars, count in statistics.items():
        writer.writerow([num_chars, count])

    writer.writerow(['', ''])
    writer.writerow(['Caractères', 'Pourcentage de mots'])
    for num_chars, count in statistics.items():
        writer.writerow([num_chars, (count/tot_line)])

