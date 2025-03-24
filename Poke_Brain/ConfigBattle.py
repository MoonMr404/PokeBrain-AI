import sys
from poke_env import RandomPlayer
from poke_env.environment.battle import Battle
from PokeMinimax import PokeMinimax

# Sovrascrivere il metodo choose_move per includere il print delle informazioni della squadra
class TeamManager:
    """
    Classe responsabile della configurazione e gestione della logica delle squadre.
    """
    def __init__(self):
        self.player_teams = {}  # Dizionario per le squadre dei giocatori

    def configure_player_team(self, player_id: str, battle: Battle):
        """
        Configura e salva la squadra di un giocatore specifico.
        """
        if player_id not in self.player_teams:
            all_pokemon_ready = all(len(pokemon.moves) == 4 for pokemon in battle.team.values())
            if all_pokemon_ready:
                self.player_teams[player_id] = list(battle.team.values())

    def get_opponent_team(self, opponent_id: str, battle: Battle):
        """
        Ritorna la squadra avversaria conoscendo l'ID avversario.
        """
        if opponent_id in self.player_teams:
            return self.player_teams[opponent_id]
        else:
            all_opponent_pokemon_known = all(len(pokemon.moves) > 0 for pokemon in battle.opponent_team.values())
            if all_opponent_pokemon_known:
                self.player_teams[opponent_id] = list(battle.opponent_team.values())
            return self.player_teams.get(opponent_id, [])

class MinimaxPlayer(RandomPlayer):
    def __init__(self, team_manager, player_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.team_manager = team_manager
        self.player_id = player_id
        self.opponent_id = None
        self.node_created = False
        self.pokeMcts = None

    async def choose_move(self, battle: Battle):
        # Configura la squadra del giocatore
        self.team_manager.configure_player_team(self.player_id, battle)

        # Configura la squadra avversaria
        if not self.opponent_id:
            self.opponent_id = "player_2" if self.player_id == "player_1" else "player_1"
        opponent_team = self.team_manager.get_opponent_team(self.opponent_id, battle)

        # Configura il nodo MCTS solo una volta 
        # PRIMO TURNO E' SEMPRE VUOTO
        if not opponent_team:
            print("Opponent team vuoto, ritorno mossa di default")
            return self.choose_default_move()

    # Configura il nodo MCTS solo una volta
        if not self.node_created:
            self.pokeMcts = PokeMinimax(battle, opponent_team)
            self.node_created = True

        if not self.pokeMcts:  # Aggiungi un controllo per il caso in cui poke_mcts è None
            print("Errore: pokeMcts non è inizializzato correttamente!")
            return self.choose_default_move()  # Fai una mossa di fallback

        mossaScelta = self.pokeMcts.scegliMossa(battle)

        # la mossa è inizializzata
        if mossaScelta:
            print(f"Mossa scelta: {mossaScelta.action}, valore nodo: {mossaScelta.valore}")
            return self.create_order(mossaScelta.action)
        else:
            #La mossa non è stata inizializzata
            print("MOSSA: NULL!!!!")
            return self.choose_default_move()

class CustomerRandomPlayer(RandomPlayer):
    def __init__(self, team_manager, player_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.team_manager = team_manager
        self.player_id = player_id
        self.opponent_id = None
        self.node_created = False

    async def choose_move(self, battle):
        self.team_manager.configure_player_team(self.player_id, battle)
        if not self.opponent_id:
            self.opponent_id = "player_2" if self.player_id == "player_1" else "player_1"
        opponent_team = self.team_manager.get_opponent_team(self.opponent_id, battle)

        # Configura il nodo MCTS solo una volta
        if not self.node_created and opponent_team:
            self._NodeConfiguration(battle, opponent_team)
        self.node_created = True

        return super().choose_move(battle)
    
    def _NodeConfiguration(self, battle: Battle, opponent_team):
        """
        Configura il nodo MCTS con il team avversario.
        """
        poke_mcts = PokeMinimax(battle, opponent_team)
        print(poke_mcts)
