from poke_env.environment.move_category import MoveCategory

    # Calcola il danno di una mossa in base alle statistiche dell'attaccante e del difensore.
def calculateDamage(move, attaccante, difensore, pessimistic, myTurn):
    # Se la mossa è nulla o è una mossa di stato, non infligge danno
    if move is None:
        return 0
    if move.category == MoveCategory.STATUS:
        return 0

    # Inizializza il danno con la potenza base della mossa
    damage = move.base_power
    ratio = 1

    # Calcola il rapporto Attacco/Difesa in base alla categoria della mossa
    if move.category == MoveCategory.PHYSICAL:
        ratio = calculatePhysical(attaccante, difensore, myTurn)
    elif move.category == MoveCategory.SPECIAL:
        ratio = calculateSpecial(attaccante, difensore, myTurn)
    # Applica il rapporto Attacco/Difesa
    damage *= ratio

    # Calcola il moltiplicatore di livello
    levelMultiplier = ((2 * attaccante.level) / 5) + 2
    damage *= levelMultiplier
    # Completa il calcolo base del danno
    damage = (damage / 50) + 2

    # Se impostato su pessimistic, applica il moltiplicatore minimo (85%) del fattore casuale
    if pessimistic:
        damage *= 0.85

    # Applica il bonus STAB (Same Type Attack Bonus) se il tipo della mossa coincide con quello del Pokémon attaccante
    if move.type == attaccante.type_1 or move.type == attaccante.type_2:
        damage *= 1.5

    # Applica il moltiplicatore di tipo in base alle debolezze e resistenze del difensore
    typeMultiplier = difensore.damage_multiplier(move)
    damage *= typeMultiplier

    return damage

    # Calcola il rapporto tra Attacco e Difesa per le mosse fisiche.
def calculatePhysical(attaccante, difensore, myTurn):
    if myTurn:
        # Ottieni il valore dell'Attacco dell'attaccante
        attack = attaccante.stats["atk"]

        # Stima la Difesa dell'avversario considerando la base e un valore medio di EV/IV
        defense = 2 * difensore.base_stats["def"] + 36
        defense = ((defense * difensore.level) / 100) + 5
    else:
        # Se è il turno dell'avversario, prendi direttamente la statistica di Difesa
        defense = difensore.stats["def"]
        # Calcola l'Attacco dell'avversario basandoti sulla sua statistica base e un valore medio di EV/IV
        attack = 2 * attaccante.base_stats["atk"] + 36
        attack = ((attack * attaccante.level) / 100) + 5

    return attack / defense

#  Calcola il rapporto tra Attacco Speciale e Difesa Speciale per le mosse speciali.
def calculateSpecial(attaccante, difensore, myTurn):
    if myTurn:
        # Ottieni il valore dell'Attacco Speciale dell'attaccante
        spatk = attaccante.stats["spa"]

        # Stima la Difesa Speciale dell'avversario
        spdef = 2 * difensore.base_stats["spd"] + 36
        spdef = ((spdef * difensore.level) / 100) + 5
    else:
        # Se è il turno dell'avversario, prendi direttamente la statistica di Difesa Speciale
        spdef = difensore.stats["spd"]
        # Calcola l'Attacco Speciale dell'avversario basandoti sulla sua statistica base e un valore medio di EV/IV
        spatk = 2 * attaccante.base_stats["spa"] + 36
        spatk = ((spatk * attaccante.level) / 100) + 5

    return spatk / spdef

#calcolo degli Hp
def calculateTotalHP(pokemon): 
    HP = pokemon.base_stats["hp"] * 2
    # Add average EVs and IVs to stat
    HP = HP + 36
    HP = ((HP * pokemon.level) / 100)
    HP = HP + pokemon.level + 10
    return HP

 # Determina se l'avversario può superare in velocità il mio Pokémon.
def opponentOutspeed(my_pokemon, opponent_pokemon):
    my_speed = my_pokemon.speed if hasattr(my_pokemon, 'speed') and my_pokemon.speed is not None else 0
    opponent_speed = opponent_pokemon.speed if hasattr(opponent_pokemon, 'speed') and opponent_pokemon.speed is not None else 0
    
    return my_speed > opponent_speed

   #Calcola il moltiplicatore di danno in base alla tipologia dell'avversario.
def DefensiveTypeMultiplier(myPokemon, opponentPokemon):
    # Ottieni il primo tipo dell'avversario e calcola il moltiplicatore di danno
    first_type = opponentPokemon.type_1
    first_multiplier = myPokemon.damage_multiplier(first_type)

    # Controlla se l'avversario ha un secondo tipo
    second_type = opponentPokemon.type_2
    if second_type is None:
        return first_multiplier

    # Calcola il moltiplicatore di danno per il secondo tipo
    second_multiplier = myPokemon.damage_multiplier(second_type)

    # Restituisce il valore maggiore tra i due moltiplicatori
    return max(first_multiplier, second_multiplier)

def bestSuperEffectiveMove(attaccante, difensore):
    bestMultiplier = 1  # Di default, nessuna super efficacia

    for move in attaccante.moves.values():  # Controlla tutte le mosse disponibili
        if move.category == MoveCategory.STATUS:  # Ignora mosse di stato
            continue

        # Calcola il moltiplicatore di tipo (superefficacia)
        typeMultiplier = difensore.damage_multiplier(move)

        # Se questa mossa è migliore, aggiorniamo il bestMove
        if typeMultiplier > bestMultiplier:
            bestMultiplier = typeMultiplier

    return bestMultiplier
