import json
import random as r
import math as m
#from typing import Type

class Creature:

    def __init__(self, jsonPath : str):

        with open(jsonPath) as creature_json:
            self.__creatureData = json.load(creature_json)
        
        self.attributes = self.__creatureData['attributes']

        self.abilityScores = self.attributes['baseAbilities']
        self.abilityMods = {}
        
        for eachAbility in self.abilityScores:

            self.abilityMods[eachAbility] = m.floor((self.abilityScores[eachAbility] - 10) / 2)

        self.status = self.__creatureData['status']
        self.proficiencies = self.__creatureData['proficiencies']
        self.features = self.__creatureData['features']
        self.__actions = self.__creatureData['actions']

        self.actions = {}

        for eachAction in self.__actions['actions']:

            self.actions[eachAction] = Action(self.__actions['actions'][eachAction], self)

        self.bonusActions = {}

        for eachAction in self.__actions['bonusActions']:

            self.bonusActions[eachAction] = Action(self.__actions['bonusActions'][eachAction], self)

        self.reactions = {}

        for eachAction in self.__actions['reactions']:

            self.reactions[eachAction] = Action(self.__actions['reactions'][eachAction], self)

        self.legendaryActions = {}

        for eachAction in self.__actions['legendary']:

            self.legendaryActions[eachAction] = Action(self.__actions['legendary'][eachAction], self)

        self.otherActions = self.__actions['other']

        for eachAction in self.__actions['other']:

            self.otherActions[eachAction] = Action(self.__actions['other'][eachAction], self)
        
    def savingThrow(self, save : str, DC : int):

        natRoll = r.randint(1,20)

        if natRoll == 1:

            print("CRITICAL FAILURE")

            saved = False
            return saved
        
        if natRoll == 20:

            print("CRITICAL SUCCESS")

            saved = True
            return saved

        roll = natRoll + self.abilityMods[save]

        if save in self.proficiencies['saves']:

            roll += self.attributes['proficiencyBonus']
        
        if roll < DC:

            print(self.attributes['name'], "failed their", save, "save")
            saved = False
        
        else: 
            
            print(self.attributes['name'], "passed their", save, "save")
            saved = True

        return saved


class Action:

    def __init__(self, actionDict : dict, parent : Creature):

        self.description = actionDict['description']
        self.type = actionDict['type']
        self.form = actionDict['form']
        self.range = actionDict['range']
        self.damageDice = actionDict['damageDice']
        self.damageBonus = actionDict['damageBonus']
        self.damageType = actionDict['damageType']
        self.hitBonus = actionDict['hitBonus']
        self.saveAbility = actionDict['saveAbility']
        self.saveDC = actionDict['saveDC']
        self.saveFail = actionDict['saveFail']
        self.saveSuccess = actionDict['saveSuccess']
        self.charges = actionDict['charges']
        self.chargeReset = actionDict['chargeReset']
        self.parent = parent

        if (not (self.hitBonus is int)) and (self.hitBonus != None):

            self.hitBonus = self.parent.abilityMods[self.hitBonus]

            if self.type in self.parent.proficiencies['weapons']:

                self.hitBonus += self.parent.attributes['proficiencyBonus']
    
    def perform(self, target : Creature):

        print(self.parent.attributes['name'], "performs the following action")
        print(self.description)

        if self.hitBonus != None:

            toHit = r.randint(1,20) + self.hitBonus

            if toHit < target.attributes['AC']:

                print(self.parent.attributes['name'], "misses", target.attributes['name'])
        
        if self.saveAbility != None:

            if target.savingThrow(self.saveAbility, self.saveDC):

                print(self.saveFail['description'])
            
            elif self.saveSuccess != None:

                print(self.saveSuccess['description'])



class Spell:

    def __init__(self, jsonPath : str):

        with open(jsonPath) as spell_json:
            self.__spellData = json.load(spell_json)

        self.attributes = self.__spellData['attributes']
        self.components = self.__spellData['components']
        self.utility = self.__spellData['utility']
        self.source = self.__spellData['source']
        
        #print(self.__spellData)

    def cast(self, hitBonus : int = 0, damageBonus : int = 0, dc : int = None, adv_dis = None, casterName : str = "You", target : Creature = None, level : int = None):

        if level == None:

            level == self.attributes['level']

        elif level < self.attributes['level']:

            level = self.attributes['level']

        if self.utility['upcastable']:

            print(self.attributes['name'], "is cast by", casterName, "at level", level)

        else:

            print(self.attributes['name'], "is cast by", casterName)

        print(self.attributes['description'])

        if self.utility['damage']:

            if adv_dis != None:

                hitRoll1 = r.randint(1,20)
                hitRoll2 = r.randint(1,20)

                print(casterName, "rolled a", hitRoll1, "and a", hitRoll2)
                
                if ((hitRoll1 > hitRoll2) and adv_dis) or ((hitRoll1 < hitRoll2) and not adv_dis):

                    hitRoll = hitRoll1
                
                else:

                    hitRoll = hitRoll2
            
            else:

                hitRoll = r.randint(1,20)

                print(casterName, "rolled a", hitRoll)

            if hitRoll == 20:

                print("CRITICAL SUCCESS")

                crit = True

            elif hitRoll == 1:

                print("CRITICAL FAILURE")

            else:

                crit = False
            
            if dc != None and hitRoll + hitBonus < dc:

                print(casterName, "misses!")

                return 0, None
            
            else:

                if dc != None:

                    print(casterName, "hits!")

                damage = []

                for eachDie in range(int(self.utility['damageDice'].split('d')[0])):

                    damage.append(r.randint(1,int(self.utility['damageDice'].split('d')[1])))

                if crit:

                    damageTotal = sum(damage) * 2 + damageBonus
                
                else: 

                    damageTotal = sum(damage) + damageBonus
                
                print(casterName, "rolled", damage, "for", damageTotal, "total", self.utility['damageType'], "damage!")

                return damageTotal, self.utility['damageType']
            
                    

def roll(dice : str = "1d20", adv_dis = None):

    rolling = dice.split("d")

    if dice == "1d20":

        if adv_dis == None:

            natRoll = r.randint(1,20)

            print("rolled a natural", natRoll)

            if natRoll == 20:

                print("CRITICAL SUCCESS")

                crit = True

            elif natRoll == 1:

                print("CRITICAL FAILURE")

                crit = False

            else:

                crit = None
        
        elif adv_dis == False:

            natRoll1 = r.randint(1,20)



eldritchBlast = Spell(r"Spell\Eldritch_Blast.json")
eldritchBlast.cast(
    hitBonus=5,
    damageBonus=3,
    dc=14,
    casterName="Teefs"
)

direWolf = Creature(r"Creature\NonPlayer\Dire_Wolf.json")
direWolf.act(direWolf.actions['Bite'])