import Utils
from poke_env.environment.pokemon import Pokemon
from poke_env.environment.move import Move
from poke_env.environment.battle import Battle

class NodoMinimax:
    
    def __init__(self, battle=None, action=None, previousAction=None, OpponentTeam=None, OpponentActive=None, OpponentHp=None,
                 MyActive=None, MyActiveHp=None, padre=None, valore=None):
        self.battle = battle
        self.padre = padre
        self.OpponentTeam = OpponentTeam if OpponentTeam else []
        self.OpponentActive = OpponentActive
        self.OpponentHp = OpponentHp if OpponentHp else {}  # Conserva HP dell'avversario con oggetti Pokémon come chiave
        self.MyActive = MyActive
        self.MyActiveHp = MyActiveHp if MyActiveHp else {}  # HP del Pokémon attivo
        self.action = action
        self.previousAction = previousAction
        self.figli = []  # Lista per i figli del nodo
        self.valore = valore if valore else 0  # Valore del nodo 

    def la_foglia(self):
        # Controlla se il nodo è una foglia.
        return len(self.figli) == 0
    
    # Genera tutte le mosse che PokeMcts può generare
    def generateChilde(self):
        self.addChildeMove()
        if not self.battle.trapped and (not isinstance(self.previousAction, Pokemon) or self.battle.active_pokemon.current_hp <= 0):
            self.addChildeSwitch()
        return self.figli
    
    # Genera tutte le mosse che l'avversario può generare
    def generateOppChilde(self):
        self.addOppChildeMove()
        self.addOppChildeSwitch()
        return self.figli

    def addChildeMove(self):
        if self.battle.active_pokemon is self.MyActive: 
            # Crea un nodo per ogni mossa disponibile
            for move in self.battle.available_moves:
                if move.current_pp > 0:
                    self.figli.append(NodoMinimax(self.battle, move, self.previousAction, OpponentTeam=self.OpponentTeam, 
                                                OpponentActive=self.OpponentActive, OpponentHp=self.OpponentHp, 
                                                MyActive=self.MyActive, MyActiveHp=self.MyActiveHp, padre=self, valore=self.valore))
        else:
            # Se non è il Pokémon attivo, aggiungi i figli per tutte le mosse del Pokémon
            for move in self.MyActive.moves.values():
                if move.current_pp > 0:
                    self.figli.append(NodoMinimax(self.battle, move, self.previousAction, OpponentTeam=self.OpponentTeam, 
                                                OpponentActive=self.OpponentActive, OpponentHp=self.OpponentHp, 
                                                MyActive=self.MyActive, MyActiveHp=self.MyActiveHp, padre=self, valore=self.valore))

    def addChildeSwitch(self):
        # Gestisce gli switch, aggiungendo un nodo per ogni Pokémon disponibile da sostituire
        for switch in self.battle.team.values():
            if switch.current_hp > 0 and switch is not self.MyActive:
                self.figli.append(NodoMinimax(self.battle, switch, self.previousAction, OpponentTeam=self.OpponentTeam, 
                                            OpponentActive=self.OpponentActive, OpponentHp=self.OpponentHp, 
                                            MyActive=self.MyActive, MyActiveHp=self.MyActiveHp, padre=self, valore=self.valore))
        return self.figli

    def addOppChildeMove(self):
        # Genera nodi per ogni possibile mossa dell'avversario.
        for move in self.OpponentActive.moves.values():
            currentHp = self.MyActiveHp.copy()
            opponentHp = self.OpponentHp.copy()

            if self.OpponentActive not in self.OpponentHp:
                self.OpponentHp[self.OpponentActive] = self.OpponentActive.current_hp

            if Utils.opponentOutspeed(self.MyActive, self.OpponentActive) or isinstance(self.action, Pokemon):
                self.opponentFirst(move, currentHp, opponentHp)
            else:
                self.playerAttack(opponentHp)
                self.opponentSurviveAttack(currentHp)

            self.figli.append(NodoMinimax(self.battle, move, self.previousAction, self.OpponentTeam, self.OpponentActive, 
                                        opponentHp, self.MyActive, currentHp, self, self.valore))
    
    def opponentFirst(self, move, currentHp, opponentHp):
        # Gestisce il caso in cui l'avversario attacca per primo.
        damage = Utils.calculateDamage(move, self.OpponentActive, self.MyActive, False, False)
        currentHp[self.MyActive] = self.MyActiveHp[self.MyActive] - damage
        if isinstance(self.action, Move) and currentHp[self.MyActive] > 0:
            self.playerAttack(opponentHp)
    
    def playerAttack(self, opponentHp):
        # Gestisce l'attacco del giocatore.
        damage = Utils.calculateDamage(self.action, self.MyActive, self.OpponentActive, True, True)
        damagePercentage = (damage / Utils.calculateTotalHP(self.OpponentActive)) * 100
        opponentHp[self.OpponentActive] = self.OpponentHp[self.OpponentActive] - damagePercentage
    
    def opponentSurviveAttack(self, currentHp):
        # Gestisce il caso in cui l'avversario sopravvive e contrattacca.
        damage = Utils.calculateDamage(self.action, self.MyActive, self.OpponentActive, True, True)
        damagePercentage = (damage / Utils.calculateTotalHP(self.MyActive)) * 100
        currentHp[self.MyActive] = self.MyActiveHp[self.MyActive] - damagePercentage

    def addOppChildeSwitch(self):
        # Gestisce gli switch per l'avversario
        for switch in self.OpponentTeam:
            if switch is not None and switch is not self.OpponentActive and switch.current_hp > 0:
                if isinstance(self.action, Move):
                    damage = Utils.calculateDamage(self.action, self.MyActive, switch, True, True)
                    damagePercentage = (damage / Utils.calculateTotalHP(self.OpponentActive)) * 100
                    opponentHp = switch.current_hp - damagePercentage
                self.figli.append(NodoMinimax(self.battle, switch, self.previousAction, self.OpponentTeam, self.OpponentActive, 
                                           self.OpponentHp.copy(), self.MyActive, self.MyActiveHp.copy(), self, self.valore))

    # Stampa le squadre Pokémon
    def __str__(self):
        team_info = "\nTeam:"
        for pokemon in self.battle.team.values():
            moves = [f"{move.id}: {move.current_pp}" for move in pokemon.moves.values()]
            team_info += f"\n - {pokemon.species} (Lvl {pokemon.level}), HP: {pokemon.current_hp}, Moves: {moves}"

        opponent_info = "\nOpponent Team:"
        for opp in self.OpponentTeam:
            moves = [f"{move.id}: {move.current_pp}" for move in opp.moves.values()]
            opponent_info += f"\n - {opp.species} (Lvl {opp.level}), HP: {opp.current_hp}, Moves: {moves}"

        return (f"{team_info}\n\n"
                f"{opponent_info}\n\n"
                f"Valore: {self.valore}\n"
                f"Pokemon attivo: {self.MyActive.species if self.MyActive else 'Nessuno'}\n"
                f"Pokemon avversario attivo: {self.OpponentActive.species if self.OpponentActive else 'Nessuno'}")
