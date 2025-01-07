![alt text](logo.png)
# PokeBrain AI

## Cos'è Pokémon Showdown?

[Pokémon Showdown](https://pokemonshowdown.com/) è un simulatore di battaglie Pokémon basato sul browser, progettato per emulare i combattimenti competitivi tra allenatori di Pokémon. Creato da Zarel e mantenuto da una comunità di sviluppatori, Pokémon Showdown consente agli utenti di creare squadre personalizzate e sfidare avversari da tutto il mondo, simulando le regole e le meccaniche dei giochi ufficiali Pokémon.

### Caratteristiche principali

- **Simulazione fedele**: Pokémon Showdown riproduce fedelmente le regole e le meccaniche delle battaglie competitive Pokémon, incluse abilità, mosse, statistiche e status.
- **Battaglie online**: Puoi sfidare avversari casuali o amici in tempo reale.
- **Team Builder**: Un potente strumento che ti permette di costruire e personalizzare le tue squadre, scegliendo tra centinaia di Pokémon, mosse, strumenti e abilità.
- **Supporto per generazioni multiple**: È possibile giocare utilizzando le regole di diverse generazioni Pokémon, dalla prima alla più recente.

Pokémon Showdown è uno strumento essenziale per la comunità competitiva Pokémon. Offre un ambiente ideale per testare strategie, allenarsi per tornei ufficiali o semplicemente divertirsi con amici e altri appassionati.

### Risorse aggiuntive di Pokémon Showdown

- **Un sito web per combattere Pokémon**:  
  [http://pokemonshowdown.com/](http://pokemonshowdown.com/)
  
- **Una libreria JavaScript per simulare battaglie Pokémon e ottenere dati Pokédex**:  
  Consulta la documentazione in `sim/LEGGIMI.md`.

- **Strumenti da riga di comando per simulare battaglie Pokémon**:  
  Consulta il file `LINEACOMANDO.md` per maggiori dettagli.

- **API web per il sito web delle battaglie Pokémon**:  
  Consulta `WEB-API.md` nella directory `client-pokemon-showdown`.

- **Server di gioco per ospitare la tua community e modalità di gioco personalizzate**:  
  Consulta il file `server/LEGGIMI.md`.

Pokémon Showdown supporta lotte singole, doppie e triple, coprendo tutte le generazioni di giochi Pokémon, dalla prima alla nona.

### Collegamenti rapidi alla documentazione

- **`PROTOCOL.md`**: Come comunicano tra loro il client e il server.
- **`sim/SIM-PROTOCOL.md`**: La parte del protocollo relativa alle battaglie e ai messaggi di battaglia.
- **`CONTRIBUTING.md`**: Standard di codice utili per chi vuole contribuire al progetto.
- **`ARCHITECTURE.md`**: Una panoramica di alto livello sul funzionamento del codice.
- **FAQ sui bot**: Una FAQ compilata da Kaiepi sulla creazione di bot per Pokémon Showdown (chatbot e bot di battaglia).

---

## Poke-env

Poke-env è un'interfaccia Python progettata per creare agenti Pokémon da combattimento. Questa libreria offre un'interfaccia semplice per sviluppare bot basati su regole o su apprendimento rinforzato per competere in Pokémon Showdown.

Gli agenti sono istanze di classi Python che ereditano da `Player`. La documentazione, gli esempi dettagliati e il codice di partenza sono disponibili su [ReadTheDocs](https://poke-env.readthedocs.io/).

### Requisiti

- Python >= 3.9
- Un server Pokémon Showdown

### Installazione

```bash
pip install poke-env
## Configurazione del server locale
```

Puoi usare il server di Smogon per testare i tuoi agenti contro giocatori umani. Tuttavia, è fortemente consigliato configurare un server di sviluppo locale. Usa il flag `--no-security` per disattivare la maggior parte dei limiti di velocità e delle restrizioni.

### Istruzioni per configurare un server locale

```bash
git clone https://github.com/smogon/pokemon-showdown.git
cd pokemon-showdown
npm install
cp config/config-example.js config/config.js
node pokemon-showdown start --no-security
```
## Ringraziamenti

Un sentito ringraziamento a:  

- **[Smogon](https://github.com/smogon)** per il repository di Pokémon Showdown, uno strumento fondamentale per il nostro progetto.  
- **Haris Sahovic** per la libreria [poke-env](https://github.com/hsahovic/poke-env), che ci ha permesso di sviluppare agenti intelligenti per Pokémon Showdown in modo semplice ed efficace.  
