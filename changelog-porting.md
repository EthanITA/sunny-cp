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
I docstring li ho convertiti in `"""` invece di `'''` per consistenza