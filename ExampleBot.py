import sys
import asyncio
from poke_env import RandomPlayer

# Aggiungi la libreria 'poke_env' se non è nel path
sys.path.append("../src")  # Modifica questo percorso se necessario

# Crea i due agenti RandomPlayer senza configurazione di account (server locale)
random_player_1 = RandomPlayer()
random_player_2 = RandomPlayer()

# Funzione asincrona per iniziare la battaglia
async def start_battle():
    # Avvia la battaglia tra i due giocatori
    await random_player_1.battle_against(random_player_2, n_battles=1)

    # Stampa il risultato della battaglia
    print(f"Player {random_player_1.username} won {random_player_1.n_won_battles} out of {random_player_1.n_finished_battles} played")
    print(f"Player {random_player_2.username} won {random_player_2.n_won_battles} out of {random_player_2.n_finished_battles} played")

    # Stampa le battaglie per ogni giocatore
    for battle_tag, battle in random_player_1.battles.items():
        print(f"Battle: {battle_tag} | Won: {battle.won}")

    for battle_tag, battle in random_player_2.battles.items():
        print(f"Battle: {battle_tag} | Won: {battle.won}")

# Esegui la funzione asincrona
asyncio.run(start_battle())
