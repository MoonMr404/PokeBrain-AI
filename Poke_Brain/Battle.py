import asyncio
from ConfigBattle import TeamManager, MinimaxPlayer, CustomerRandomPlayer

# Inizializza il gestore delle squadre
team_manager = TeamManager()

# Inizializza i giocatori con il gestore delle squadre
random_player_1 = MinimaxPlayer(team_manager, "player_1", battle_format="gen4randombattle")
random_player_2 = MinimaxPlayer(team_manager, "player_2", battle_format="gen4randombattle")

# Funzione asincrona per iniziare la battaglia
async def start_battle():
    # Avvia la battaglia tra i due giocatori
    await random_player_1.battle_against(random_player_2, n_battles=10)

    # Stampa il risultato della battaglia
    print(f"\nPlayer {random_player_1.username} won {random_player_1.n_won_battles} out of {random_player_1.n_finished_battles} played")
    print(f"Player {random_player_2.username} won {random_player_2.n_won_battles} out of {random_player_2.n_finished_battles} played")

    # Stampa le battaglie per ogni giocatore
    for battle_tag, battle in random_player_1.battles.items():
        print(f"Battle: {battle_tag} | Won: {battle.won}")

    for battle_tag, battle in random_player_2.battles.items():
        print(f"Battle: {battle_tag} | Won: {battle.won}")

# Esegui la funzione asincrona
asyncio.run(start_battle())
