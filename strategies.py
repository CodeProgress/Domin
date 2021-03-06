##### 
#Strategies for AI players.
#Try working this into the player class
#ex:  player.strategy = function (default = None)
#then in game, call the function
#if strategy, return what strategy dictates, otherwise accept user input

import random

def buy_only_prov(numCoins):
    """strategy where player only buys provinces if numCoins >= 8
    otherwise, player buys the most valuable treasure card.
    returns the card to buy (as String) if numCoins > 0, else returns None
    """
    
    if numCoins >= 8:
        return "province"
    if numCoins >= 6:
        return "gold"
    if numCoins >= 3:
        return "silver"
    if numCoins >= 1:
        return "copper"
    return None

def buy_only_prov_no_copper(numCoins):
    """strategy where player only buys provinces if numCoins >= 8
    otherwise, player buys the most valuable treasure card.
    returns the card to buy (as String) if numCoins > 0, else returns None
    """
    
    if numCoins >= 8:
        return "province"
    if numCoins >= 6:
        return "gold"
    if numCoins >= 3:
        return "silver"
    return None

def buy_only_duchy(numCoins):
    """strategy where player only buys provinces if numCoins >= 8
    otherwise, player buys the most valuable treasure card.
    returns the card to buy (as String) if numCoins > 0, else returns None
    """
    
    if numCoins >= 6:
        return "gold"
    if numCoins == 5:
        return "duchy"
    if numCoins >= 3:
        return "silver"
    if numCoins >= 1:
        return "copper"
    return None

def buy_only_duchy_no_copper(numCoins):
    """strategy where player only buys provinces if numCoins >= 8
    otherwise, player buys the most valuable treasure card.
    returns the card to buy (as String) if numCoins > 0, else returns None
    """
    
    if numCoins >= 6:
        return "gold"
    if numCoins == 5:
        return "duchy"
    if numCoins >= 3:
        return "silver"
    return None

def buy_best_avail(numCoins):

    if numCoins >= 8:
        return "province"
    if numCoins >= 6:
        return "gold"
    if numCoins == 5:
        return "dutchy"
    if numCoins >= 3:
        return "silver"
    if numCoins == 2:
        return "estate"
    if numCoins == 1:
        return "copper"
    return None

def buy_best_avail_no_copper(numCoins):

    if numCoins >= 8:
        return "province"
    if numCoins >= 6:
        return "gold"
    if numCoins == 5:
        return "dutchy"
    if numCoins >= 3:
        return "silver"
    if numCoins == 2:
        return "estate"
    return None

def action_trivial(actions):
    """returns the action to play
    actions: list of action functions
    """
    pass
    
def rand_remaining_action_card(actions):
    """returns a random action card from the player's hand"""
    return random.choice(actions)
    
