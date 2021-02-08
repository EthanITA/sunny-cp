# ./src/parsing.py 
## modifiche
- tolto gli `eval()` con `eval_extractor()`, che fa essenzialmente un switch-case e prende la classe corrispondente
- aggiunto fz. `exit_error(status, *reasons)` in modo tale da evitare i copia-incolla di `"For help use --help"` e i `file=sys.stderr`. Di conseguenza sostituito tutte le parti di codice di questa forma:
    ```
    print("Error! ...", file=..) 
    print("For help..." file=..) 
    sys.exit(2)
    ```
### parse_arguments()
- semplificato inizializzazione di `solver_options`
- rimosse varie conversioni inutili da iteratori a liste 
- varie conversione da concatenazione a f-string
### get_solve()
- varie conversione da concatenazione a f-string

# ./src/sunny_server.py
## modifiche
### do_GET()
- self.wfile.write() parametro attuale convertito in bytes()
    
    https://stackoverflow.com/questions/7646657/writing-response-body-with-basehttprequesthandler
### do_POST()
- varie stringhe convertite in bytes per operazioni di scrittura in binario
- `process` viene inizializzata nel blocco `try`, potrebbe non essere inizializzata
# ./src/solver.py
## modifiche
### RunningSolver
- non è possibile avere piu costruttori in una classe in python
- concatenazione in f-string
- in `inject_bound()`, inutile conversione di `string()` a `list()` usando metodo `split()`
# ./src/scheduling.py
## modifiche
### get_neighbours(): 
- `feat_vectors` e `sorted_dist` variabili mai utilizzate
- espressione per generare il dizionario di ritorno semplificato (nel `return`)
### euclidean_distance():
- resa l'espressione per calcolare la distanza più "matematica" 
### sunny_csp():
- il for per inizializzare `solved` e `times` si può farlo inline
- conversione in `list()` inutile di `neighbours.items()` nel statement del for
- convertitio `eval()` in `ast.literal_eval()`
- `old_pfolio = best_pfolio` e `if old_pfolio == best_pfolio` ora viene usato un semplice booleano per il controllo
- conversione inutile da `[]` a `set()`
- `backup in list(schedule.keys())` fa operazioni ridondanti, basta `backup in schedule` per vedere se `backup` è una chiave di `schedule`
### sunny_cop()
- for di inizializzazione inline
- conversione inutile
- `old_pfolio = best_pfolio` e `if old_pfolio == best_pfolio` ora viene usato un semplice booleano per il controllo
- rimosso definizioni inutili di `time` e `area`
- `port_scores` semplificato
- operazione ridondante (riga 160)
### parallelize()
- conversione inutile
- convertito `/` in `//` perchè è un'operazione fra interi

## possibile problemi
### get_neighbours(): 
    round() built-in function
    ---
    PYTHON3: rounding is done toward the even choice (so, for example, both round(0.5) and round(-0.5) are 0, and round(1.5) is 2)
    ---
    PYTHON2: rounding is done away from 0 (so, for example, round(0.5) is 1.0 and round(-0.5) is -1.0).

# ./src/problem.py
## modifiche
### __ init __()
- convertito in operatore ternario per l'assegnamento `self.best_bound`
### bound_worse_than() e bound_better_than():
- rimossi `\` nelle condizioni all'interno delle parentesi
# ./src/features.py
## modifiche
### extract()
- concatenazione string in f-string
- inlining e semplificazione list comprehension `[float(f) for f in features]`

# ./src/defaults.py
## modifiche
- concatenazione string in f-string
- utilizzo di `with` per aprire file
- semplificazione per generare `DEF_PFOLIO`


# ./src/combinations.py
## modifiche 
### binom():
- unito condizioni `n == k` e `k == 0`
- `/` non torna più interi, rimpiazzato con `//`

# ./kb/util/csv2kb.py
## modifiche
- aggiunto `import sys`
- `kb_path` concatenazione string in f-string

# ./kb/util/helper_kb.py
## Modifiche
### compute_infos():
- `\` per andare a capo non serve all'interno delle parentesi
- semplificato l'espressione per ottenere `values`
- `last_val = [v for (t, v) in values.items() if t == max(values.keys())]` fa un ciclo inutile, perchè può essere vuota o con un elemento:
    - vuota, se `values` vuota
    - l'unico elemento appartente è ottenibile accedendo in `values` con chiave `max(values)`
- Come conseguenza del punto precedente è stato semplificato la condizione nel parametro attuale di `check_invariant()`
- `if inst not in list(kb_cop.keys()):` è uguale a `if inst not in kb_cop`
- `list(values.values())` non serve conversione, le funzioni `min()` e `max()` accettano il tipo `dict_values()` (riga 75)
- `if inst not in list(kb_csp.keys()):` uguale a `if inst not in kb_csp`
- conversioni inutili (riga 87-88)
### check_invariant(): 
- `a <=/=> b` è uguale a dire `a != b`
### get_area():
- non serve conversione `list(values.items())` in `scaled_vals`
- rimosso commento che non serve
- assegnamento `t` if-else convertito in operatore ternario
### make_kb():
- concatenazione string in f-string (riga 183-186)
- `insts_csp = list(kb_csp.keys())` non serve conversione perchè nelle righe  successive vengono usate solamente keyword `in` riferito ad essa
- `feat_vector = eval(row[1])` sostituibile con `ast.literal_eval()` 
- `kb_row.append()` semplificabile
- `lims[i] = [feat_vector[i], feat_vector[i]]` semplificabile con `enumerate()
- tolto conversione in `list()` nel for (riga 221)
- concatenazione string in f-string (riga 257)
- `json.dump(eval('lims_' + i), outfile)` riscritto il for in modo più comprensibile togliendo anche `eval()`
# ./solvers/make_pfolio
## Modifiche
- `open(pfolio_path, 'w')` non viene chiuso
- gli `Iterator` non hanno più metodi `next()` 
- concatenazione di `str()` tradotti in `f-string` per leggibilità e performance
- `out` in byte convertito in `str()` 
- inline variabile (riga 57)
- `open("../opts", 'r')` non viene chiuso
## Possibili problemi
- `pfolio_solvers.py` generato da `make_pfolio.py`, importa `solver` che è anche una libreria (installabile) di Python
---
# ./job_dispatcher/job_dispatcher.py
## Modifiche
### get_hash_id():
- `h.update()` ora serve un byte-object like, invece di str
- `id` oscura funzione built-in

### create_request_list():
- `unicode()` è stato rimpiazzato da `str()` le operazioni di `line.replace()` devono usare stringhe e non più byte

### parse_solver_output():
- in docstring, la fz. restituisce un `dict()`
- `time` oscura modulo built_in

### worker():
- `id` oscura fz built-in
- `requests.exceptions.RequestException` è superclasse di `requests.exceptions.ConnectionError`, quindi errori di tipo `ConnectionError` non verrebbero catturati
- `json_result = parse_solver_output()`, la fz torna un `dict()`

### generate_kb_files():
- `Erronous` typo (riga 519)
- `f.write()` non accetta stringhe perchè è stato usato `open(.., "wb")`
### check_anomalies():
- `possible_erroneous_solvers = set([])`, `set()` torna direttamente un insieme vuoto, non serve convertirlo da `[]`


## Potenziali problemi (da vedere meglio)
### def worker():
- vengono fatte richieste post mandando file di tipo `<open file '...', mode 'rb' at 0x...>`, suppongo che il codice che va a toccarci sia in `sunny_server.py` nella fz. `do_POST()`

---

# Altro
- `eval()` sostituito con `ast.literal_eval()` per casi in cui serve una conversione da stringa a un tipo di Python
---
    >>> help(ast.literal_eval)
    Help on function literal_eval in module ast:

    literal_eval(node_or_string)
        Safely evaluate an expression node or a string containing a Python
        expression.  The string or node provided may only consist of the following
        Python literal structures: strings, numbers, tuples, lists, dicts, booleans,
        and None.
---

- I docstring li ho convertiti in `"""` invece di `'''` per consistenza