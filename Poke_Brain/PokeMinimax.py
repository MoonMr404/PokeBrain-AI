import sys
import asyncio
from poke_env.environment.pokemon import Pokemon
from poke_env import RandomPlayer
from poke_env.player.player import Player
from poke_env.environment.battle import Battle
from poke_env import RandomPlayer
from poke_env.environment.move import Move
from poke_env.player.battle_order import BattleOrder
from NodoMinimax import NodoMinimax

import numpy as np
import pandas as pd
import Utils

class PokeMinimax:

    previousAction = None
    maxDepth = 2

    def __init__(self, battle: Battle, OpponentTeam: list):
        if not isinstance(battle, Battle):
            raise ValueError("Il parametro 'battle' deve essere un oggetto di tipo Battle.")
        self.battle = battle
        self.opponentTeam = OpponentTeam
        self.startNode = None

    def scegliMossa(self, battle: Battle):
        currentHp = {}
        for pokemon in battle.team.values():
            currentHp.update({pokemon: pokemon.current_hp})

        opponentHp = {}
        for pokemon in self.opponentTeam:
            opponentHp.update({pokemon: pokemon.current_hp})

        startNode = NodoMinimax(self.battle, None, self.previousAction, self.opponentTeam, battle.opponent_active_pokemon,
                             opponentHp, battle.active_pokemon, currentHp, None, float('-inf'))

        if battle.active_pokemon.current_hp <= 0:
            self.bestSwitch(startNode, 0)
        else:
            self.minimax(startNode, 0, True)

        nodiFiglio = startNode.figli
        bestValore = float('-inf')
        bestNodo = None
        for figlio in nodiFiglio:
            if figlio.valore >= bestValore:
                bestValore = figlio.valore
                bestNodo = figlio
        
        if bestNodo is None:
            self.previousAction = None
            return None
        
        self.previousAction = bestNodo.action
        return bestNodo

    def minimax(self, nodo: NodoMinimax, depth, myTurn):
        if depth == self.maxDepth or self.isTerminal(nodo):
            self.calcoloValore(nodo)
            return nodo.valore

        if myTurn:
            value = float('-inf')
            myMoves = nodo.generateChilde()
            for move in myMoves:
                figlioValore = self.minimax(move, depth, False)
                value = max(value, figlioValore)
                nodo.valore = value
            return value
        else:
            value = float('inf')
            opponentMoves = nodo.generateOppChilde()
            for move in opponentMoves:
                figlioValore = self.minimax(move, depth + 1, True)
                value = min(value, figlioValore)
            nodo.valore = value
            return value

    def bestSwitch(self, nodo: NodoMinimax, depth):
        switches = nodo.addChildeSwitch()
        value = float('-inf')
        for switch in switches:
            figlioValore = self.minimax(switch, depth, False)
            value = max(value, figlioValore)
            nodo.valore = value
        return value

    def isTerminal(self, nodo: NodoMinimax):
        allFainted = True
        for pokemon in nodo.MyActiveHp.keys():
            if nodo.MyActiveHp[pokemon] > 0:
                allFainted = False
        if allFainted:
            return True

        allFainted = True
        for pokemon in nodo.OpponentHp.keys():
            if nodo.OpponentHp[pokemon] > 0:
                allFainted = False
        if allFainted:
            return True

        return False

    def calcoloValore(self, nodo: NodoMinimax):
        value = 0

        # Valutazione del danno inflitto all'avversario
        for pokemon in nodo.OpponentHp.keys():
            if pokemon.current_hp is not None:
                if nodo.OpponentHp[pokemon] <= 0 and pokemon.current_hp > 0:
                    value += 300  # Premio per aver sconfitto un Pokémon
                else:
                    damage = pokemon.current_hp - nodo.OpponentHp[pokemon]
                    value += 3 * damage  # La formula di valore è stata modificata

            # Aggiungere la valutazione della migliore superefficacia
            bestMultiplier = Utils.bestSuperEffectiveMove(nodo.MyActive, pokemon)
            if bestMultiplier > 1:
                value += 50 * bestMultiplier  # Incremento proporzionale alla superefficacia

        # Valutazione del danno subito dal proprio Pokémon
        for pokemon in nodo.MyActiveHp.keys():
            if nodo.MyActiveHp[pokemon] <= 0 and pokemon.current_hp > 0:
                value -= 350  # Penalizzazione per il Pokémon che è stato sconfitto
            else:
                damage = (pokemon.current_hp / pokemon.max_hp) - (nodo.MyActiveHp[pokemon] / pokemon.max_hp)
                value -= damage  # Diminuzione del valore in base ai danni subiti

        nodo.valore = value
        return value

    def __str__(self):
        return str(self.startNode)