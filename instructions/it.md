
# <Span style = "color: #ff0000;"> <strong> Istruzioni </span> </strong>

Quindi hai scritto un abilità e vuole tradurlo? Buon lavoro, consente di ottenere in poi.

# <Span style = "color: #0000FF;"> <strong> fasi operative rapidi </span> </strong>

** Per usare questa abilità **

1. Andare alle impostazioni di abilità

2. Inserire il nome della abilità che si desidera tradurre in ** ** skillTitle campo

3. Fare clic su Salva

Chiedi alice di "tradurre la mia abilità"

# <Span style = "color: #0000FF;"> <strong> Abilità Panoramica </span> </strong>

- modalità Pre-check
 
Questo verrà eseguito attraverso il processo di traduzione, senza in realtà l'invio di dati di traduzione a Google.
Si tratta di un dummy run che non modificare alcun file, ma dare un feedback statistica alla fine del processo.

Questa modalità utilizza il file di lingua l'abilità è stato scritto in (impostazioni impostato tramite ... >> abilità skillLanguage) per determinare le statistiche sul processo di traduzione
prima di inviare i dati a Google. In questo modo si può prendere una decisione informata se

1. ci sono errori nei file che si fermerà il processo di traduzione

2. I file sono entro i limiti di quota di Goggle o sopra suoi limiti e, pertanto, si innescheranno in guardie di sicurezza integrate

Una volta run e si vede nessun errore, disattivare questa modalità off per eseguire l'abilità in modalità Traduzione


## ** Quando eseguito in modalità di traduzione: **

L'abilità si tradurrà nella directory colloqui prima. Se le richieste di essere fatte a Google superano la quota lo farà
mettere in pausa il codice per 70 secondi (Pausa l'abilità non Alice) poi riprendere.

L'abilità verrà poi tradurre il file finestra di dialogo e fare la stessa quota guardie di sicurezza. (Nota: se il conteggio dei caratteri
per un caso sarà probabilmente superare i 1500 del codice farà una pausa per 1 ora)

Durante la traduzione di dialogo Template il codice estrae la: porzione => KeyValue} delle esternazioni
in modo che il keyValue non ottiene tradotto e fermare l'abilità di lavorare. E 'quindi mettere che il codice Backin
prima di scriverlo in un file.

Una volta tradotto sarà poi aggiungere tutte le 4 lingue per il file di installazione.

## ** ** skillPath campo (opzionale)

- Questo è utile di che si desidera tradurre i file di abilità che si trovano al di fuori della cartella competenze

  - ** IE: **
 
    - Se sei uno sviluppatore di abilità e hanno una copia master che si desidera tradurre, piuttosto che tradurre una competenza attiva
che possono avere su espressioni ecc in.

Digitare il percorso ** a ** l'abilità, ma ** non ** lo skillname. (Utilizzare il campo skillTitle per questo)

PER ESEMPIO:

- skillPath = / home / PI / DevelopmentSkills
- skillTitle = HomeAssistant
.

## ** ** SkillTitle campo (richiesto)

Questo campo denota l'abilità che si desidera tradurre

- Con questo campo di pieni e ** non ** il * * skillPath campo così poi le impostazioni predefinite percorso della cartella ProjectAlice / competenze
- Con questo campo e campo skillPath ** non ** compilato allora si avrà tradurre questa abilità di default ..
_
## ** ** translateOnlyThis

Per questo campo ...

- Empty = tradurrà tutti i file necessari (default)

- Inserire una delle seguenti operazioni per tradurre solo quella cartella (opzionale)
 - colloqui
 - dialogo
 - Istruzioni_______________________

Bugs #Known

Esecuzione l'abilità una volta dovrebbe funzionare come previsto, ma il tentativo di eseguire due volte senza riavviare Alice sarà
tradursi in una "lingua non valida" errore.

**Esempio**:

1. Eseguire la modalità di controllo preliminare e lasciare che l'abilità completarlo del compito
2. Vai a impostazioni e disattivare la modalità di controllo preliminare
3. Eseguire il processo di traduzione e Alice mostrerà nei log che il set di lingua nelle impostazioni
è "non valido" nonostante non sia cambiato.

Aggiustare:

1. Riavviare Alice ed eseguire di nuovo la modalità di traduzione

- Nota a margine:

 se vi capita di ottenere questo errore costantemente ..
 
 `` `Json.decoder.JSONDecodeError: Valore Aspetta: linea 1 colonna 1 (char 0)` ``
 
 Poi potenzialmente, Goggle ha appena bloccato il vostro IP dai file di traduzione e si dovrà attendere fino al prossimo mezzanotte ora del Pacifico per esso t per essere sbloccato

------------------

Google translate tende ad amare l'aggiunta di spazi in cui la spaziatura non era prima. Anche se questa abilità trys per la cattura
alcune di queste occasioni si possono trovare che quando si traduce le istruzioni cartella che se si dispone di tag nella Markdown
che potrebbe essere necessario prendere manualmente alcuni spazi bianchi per averlo visualizzare correttamente.

** Ciò che l'abilità non farà **

Attualmente l'abilità non tradurre i file di riduzione dei prezzi, come queste istruzioni. Questa è una caratteristica futuro da aggiungere

Godetevi traduzione