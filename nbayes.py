from stopwords import STOPWORDS
import os
import re

PATHSEP = os.path.sep

def analizza_testo(testo):
    """Tokenizza il testo dato e torna una lista che contiene i token estratti
        nell'ordine con cui si presentano."""
    parole = []
    for parola in re.findall(r"[a-zA-Z]+", testo):
        if parola not in STOPWORDS:
            parole.append(parola)
    return parole

def analizza_corpus(NOME_DIR, vocabolario):
    """Data una cartella NOME_DIR si aspetta che contenga solo cartelle,
        ciascuna delle quali rappresenta una classe e in ciascuna delle quali ci
        siano soltanto file che contengono testi che sono elementi di quella
        classe. Scandisce tutti questi elementi e mette le parole nel dizionario
        vocabolario. Torna il corpus contenuto nella directory, cioè un
        dizionario le cui chiavi sono le sottocartelle (le classi) e i cui valori
        sono dizionari le cui chiavi sono i nomi dei file contenuti nelle
        sottocartelle e le liste di parole che sono state scandite da essi."""
    print("\nCarica nel vocabolario tutte le parole di tutti i documenti")
    corpus = {}
    for root, dirs, files in os.walk(NOME_DIR):
        for d in dirs:
            corpus[d] = {}
            # Ora apre tutti i file nella classe
            print(d)
            for sroot, sdirs, sfiles in os.walk(NOME_DIR + PATHSEP + d):
                for f in sfiles:
                    with open(NOME_DIR + PATHSEP + d + PATHSEP + f, "r", encoding="latin-1") as file:
                        parole = analizza_testo(file.read().lower())
                        corpus[d][f] = parole
                        for t in parole:
                            if t in vocabolario:
                                vocabolario[t] += 1
                            else:
                                vocabolario[t] = 1
    # Elimina le parole che compaiono meno di 3 volte in tutto il vocabolario
    da_eliminare = []
    for p in vocabolario:
        if vocabolario[p] <= 3:
            da_eliminare.append(p)
    for p in da_eliminare:
        del vocabolario[p]
    return corpus

def training(corpus, vocabolario, n_training, prob_classi, prob_parole, training_set):
    """Costruisce le matrici con le probabilita' a priori P(c) e a posteriori
        P(p|c) di ciascuna classe c del corpus dato e di ciascuna parola nella
        lista delle classi e nel vocabolario dati. Usa i primi n_training file
        nel dizionario corpus[c] dove c e' il nome di una classe. Pone i
        risultati nei dizionari prob_classi e prob_parole, mentre in training_set
        pone per ciascuna chiave (classe) la lista dei documenti che ha usato per
        addestrare il classificatore."""
    len_voc = len(vocabolario)
    n_classi = len(corpus)
    n_doc = n_classi * n_training   # numero di doc di training set totali
    for c in corpus:
        print("Classe", c, end=" ")
        # produce la lista di tutte le parole (con ripetizione) di tutti i
        # documenti della classe c: la ottiene concatenando le parole di tutti
        # questi documenti
        parole = []
        training_set[c] = []
        for testo in corpus[c]:
            training_set[c].append(testo)
            parole.extend(corpus[c][testo])
            # Training set = primi n_training documenti.
            if len(training_set[c]) >= n_training:
                break
        # Ora calcola le P(p|c) per ogni parola p nel vocabolario
        print("contiene", len(parole), "parole totali (anche ripetute)")
        denominatore = len(parole) + len_voc
        for p in vocabolario:
            # Moltiplichiamo per len_voc in modo da non ottenere valori troppo
            # bassi: ha senso in quanto prob_parole[p,c] andrebbe diviso per
            # P(p), che non è 1/len_voc ma in quell'ordine di grandezza.
            # Ai fini di prendere argmax il fattore moltiplicativo indipendente
            # da c non incide.
            prob_parole[p,c] = ((parole.count(p) + 1) / denominatore) * len_voc
        # Ora calcola la P(c)
        prob_classi[c] = len(training_set[c]) / n_doc

def testing(corpus, vocabolario, n_training, prob_classi, prob_parole, training_set):
    """Considera i file corpus[c] per ciascuna classe c nel corpus dato e prova
        a classificarli sulla base delle probabilita' fornite. Il dizionario
        training_set contiene come chiavi le classi e come valori le liste di
        file che NON vanno utilizzati per il test. Torna come valore
        la percentuale di risposte esatte."""
    risposte_esatte = 0
    risposte_sbagliate = 0
    for c in corpus:
        print("Classe", c, end=" ")
        e = risposte_esatte
        s = risposte_sbagliate
        for testo in corpus[c]:
            if testo in training_set[c]:
                continue
            # Ora prova a classificare il documento
            #print("Documento", nome, end="")
            parole = corpus[c][testo]
            # Cerca la classe che massimizza P(classe)P(token|classe)
            p_max = -1
            class_max = ""
            for cc in prob_classi:
                p = prob_classi[cc]
                for t in parole:
                    if t in vocabolario:
                        p *= prob_parole[t,cc]
                if p > p_max:
                    p_max = p
                    class_max = cc
            # La classe scelta è class_max
            #print(class_max, "[", p_max*100, "%]?", c)
            if class_max == c:
                risposte_esatte += 1
            else:
                risposte_sbagliate += 1
        print(str(100*(risposte_esatte - e)/(risposte_esatte - e + risposte_sbagliate - s)) + "% di risposte esatte")
    return risposte_esatte / (risposte_esatte + risposte_sbagliate) * 100
