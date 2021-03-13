from nbayes import analizza_corpus, training, testing

NOME_VOC = "vocabolario.txt"
#NOME_DIR = "20_newsgroups"
NOME_DIR = "20_newsgroups_debug"

# Crea il vocabolario
vocabolario = {}
classi = []
analizza_corpus(NOME_DIR, vocabolario, classi)

# Salva il vocabolario
with open(NOME_VOC, "w") as file:
    for p in vocabolario:
        file.write(p + "\n")

risultati = []
for n in range(1, 101,10):
    training_set = {}   # training_set[classe] = [documenti in quella classe]
    prob_classi = {}    # {classe: P(classe) }
    prob_parole = {}    # {parola,classe: P(parola|classe), ...}
    print("\nTraining set:", n, "%")
    training(vocabolario, classi, n, NOME_DIR, prob_classi, prob_parole, training_set)
    print("\nFase di test: classifica i documenti che non sono nel training set.")
    risultati.append(testing(vocabolario, classi, n, NOME_DIR, prob_classi, prob_parole, training_set))

# Salva il risultato su un csv
with open("risultati20000.csv", "w") as f:
    for x in risultati:
        f.write(str(x) + "\n")
