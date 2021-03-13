from nbayes import analizza_corpus, training, testing

NOME_VOC = "vocabolario.txt"
NOME_DIR = "20_newsgroups"

# Crea il vocabolario
vocabolario = {}
corpus = analizza_corpus(NOME_DIR, vocabolario)

print(f"Corpus con {len(corpus)} classi e {len(vocabolario)} parole")

# Salva il vocabolario
with open(NOME_VOC, "w") as file:
    for p in vocabolario:
        file.write(p + "\n")

n = int(input("Percentuale di documenti nel training set: "))
training_set = {}   # training_set[classe] = [documenti in quella classe]
prob_classi = {}    # {classe: P(classe) }
prob_parole = {}    # {parola,classe: P(parola|classe), ...}
print(f"\nTraining set: {n}%")
training(corpus, vocabolario, n, prob_classi, prob_parole, training_set)

print("\nFase di test: classifica i documenti che non sono nel training set.")
risultato = testing(corpus, vocabolario, n, prob_classi, prob_parole, training_set)

print(f"\nRisultato totale della classificazione: {risultato}% di risposte esatte")
input("Premere un tasto per terminare...")
