# Classificatore bayesiano ingenuo di testi

Si tratta di un esempio ormai standard di analisi bayesiana di un corpus di testi, come per esempio descritta nel libro di Mitchell sul machine learning.

Il programma si aspetta in una cartella (che viene indicata nella variabile NOME_DIR, delle cartelle che corrispondono ciascuna a una classe di documenti e si aspetta in ciascuna cartella i documenti di quella classe.

Il programma analizza il corpus di documenti estraendo le parole e calcolando una misura classica basata sulla frequenza di apparizione delle parole in un singolo documento e nell'intero corpus per calcolare le probabilità che data una certa classe una parola compaia in qualche documento di quella classe.

A quel punto col teorema di Bayes si riesce a dare una predizione della classe dato un documento: l'ipotesi semplificativa che si usa nell'applicare il teorema di Bayes è che le parole in un documento compaiano in modo indipendente, il che è palesemente falso, ma semplifica il conto.

Per collaudare il programma ho usato il celebre corpus di 20.000 documenti 20_newsgroups che si trova per esempio sulla pagina web di Jason Rennie: http://qwone.com/~jason/20Newsgroups/

Il motore bayesiano e l'analizzatore lessicale sono condensati in una libreria nbayes.py che viene chiamata dal programma che ne fa il test sul corpus.

Enjoy,
P
