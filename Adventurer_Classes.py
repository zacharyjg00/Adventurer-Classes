import mysql.connector

mydb = mysql.connector.connect(host = "localhost", user = "root", passwd = "root", port = 3306, database = "adventurer_matches")
mycursor = mydb.cursor()

#==========================================
# Purpose: This method takes in the results of a duel and stores them into a SQL database table named match_scores
# Input Parameter(s): player1 - The string name of the first adventurer
#                     player2 - The string name of the second adventurer
#                     player1_hp - The int of the first adventurer's final hp from the duel
#                     player2_hp - The int of the second adventurer's final hp from the duel
#                     victor - A string that says the victors name and that they won
# Return Value(s): Nothing is returned from this method
#==========================================
def db_insert(player1, player2, player1_hp, player2_hp, hp_difference, victor):
    sql = "insert into match_scores (first_name, second_name, final_hp_p1, final_hp_p2, hp_difference, result) VALUES (%s, %s, %s, %s, %s, %s)"
    val = (player1, player2, player1_hp, player2_hp, hp_difference, victor)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted")


# Problem A

class Adventurer:
#==========================================
# Purpose: This method initializes all of the instance variables for an instance of the Adventurer.
# Input Parameter(s): name - the string name of the adventurer instance
#                     level - the level of the adventurer instance
#                     strength - the strength of the adventurer instance
#                     speed - the speed of the adventurer instance
#                     power - the power of the adventurer instance
# Return Value(s): Nothing is returned from the constructor
#==========================================
    def __init__(self, name, level, strength, speed, power):
        self.name = str(name)
        self.level = int(level)
        self.strength = int(strength)
        self.speed = int(speed)
        self.power = int(power)
        self.HP = int(self.level * 6)
        self.hidden = False
    def __repr__(self):
        return str(self.name) + ' - HP: ' + str(self.HP)
    def __lt__(self, other):
        return self.HP < other.HP

#==========================================
# Purpose: This method simulates one adventurer attacking another adventurer. If the target adventurer is hidden, then no attack is performed. Otherwise, the damage is calculated and subtracted from the target's HP
# Input Parameter(s): target - the target adventurer object which will be dealt damage
# Return Value(s): Nothing is returned from this method
#==========================================
    def attack(self, target):
        if target.hidden == True:
            print(str(self.name) + ' can\'t see ' + str(target.name))
        else:
            damage = self.strength + 4
            target.HP -= int(damage)
            print(str(self.name) + ' attacks ' + str(target.name) + ' for ' + str(damage) + ' damage')

class Fighter(Adventurer):
    def __init__(self, name, level, strength, speed, power):
        Adventurer.__init__(self, name, level, strength, speed, power)
        self.HP = int(self.level * 12)

#==========================================
# Purpose: This method overwrites the attack method from the Adventurer class to simulate the attack from a Fighter. The method is exactly the same except for how damage is calculated. Damage is now strength multiplied by 2 and then 6 is added after the fact.
# Input Parameter(s): target - the target adventurer object which will be dealt damage
# Return Value(s): Nothing is returned from this method
#==========================================
    def attack(self, target):
        if target.hidden == True:
            print(str(self.name) + ' can\'t see ' + str(target.name))
        else:
            damage = (2 * self.strength) + 6
            target.HP -= int(damage)
            print(str(self.name) + ' attacks ' + str(target.name) + ' for ' + str(damage) + ' damage')

class Thief(Adventurer):
    def __init__(self, name, level, strength, speed, power):
        Adventurer.__init__(self, name, level, strength, speed, power)
        self.HP = int(self.level * 8)
        self.hidden = True

#==========================================
# Purpose: This method overwrites the attack method from the Adventurer class to simulate the attack from a Thief. If the Thief is hidden, then a sneak attack is performed so long as the target is either not hidden, or is hidden and slower than the attacker. A sneak attack is speed plus level
#          multiplied by 5. After a sneak attack is performed, both the attacker and target are no longer hidden and attacks go back to normal.
# Input Parameter(s): target - the target adventurer object which will be dealt damage
# Return Value(s): Nothing is returned from this method
#==========================================
    def attack(self, target):
        if self.hidden == False:
            Adventurer.attack(self, target)
        elif (target.hidden == True) and (self.speed < target.speed):
            print(str(self.name) + ' can\'t see ' + str(target.name))
        else:
            damage = (self.speed + self.level) * 5
            target.HP -= int(damage)
            self.hidden = False
            target.hidden = False
            print(str(self.name) + ' sneak attacks ' + str(target.name) + ' for ' + str(damage) + ' damage')

class Wizard(Adventurer):
    def __init__(self, name, level, strength, speed, power):
        Adventurer.__init__(self, name, level, strength, speed, power)
        self.fireballs_left = self.power

#==========================================
# Purpose: This method overwrites the attack method from the Adventurer class to simulate the attack from a Wizard. The Wizard uses a fireball attack until they are out of fireballs. The number of fireballs are equal to the power of the Wizard.
#          The damage of a fireball causes the target to no longer be hidden and deals the attackers level multiplied by 3. Once out of fireballs, the Wizard attacks normally.
# Input Parameter(s): target - the target adventurer object which will be dealt damage
# Return Value(s): Nothing is returned from this method
#==========================================
    def attack(self, target):
        if self.fireballs_left == 0:
            Adventurer.attack(self, target)
        else:
            target.hidden = False
            damage = self.level * 3
            target.HP -= int(damage)
            self.fireballs_left -= 1
            print(str(self.name) + ' casts fireball on ' + str(target.name) + ' for ' + str(damage) + ' damage')

#==========================================
# Purpose: This function simulates a fight between two Adventurers. Both adventurers attack each other until one of them dies (HP goes to or below 0). If the first adventurer (adv1) wins, then True is returned. If the second adventurer (adv2) wins, then False is returned.
#          If both adventurers adv1's and adv2's HP falls below or equal to 0, then everybody loses and False is returned
# Input Parameter(s): adv1 - adventurer object 1
#                     adv2 - adventurer object 2
# Return Value(s): True is returned if adv1 wins. False is returned if adv2 wins or nobody wins
#==========================================
def duel(adv1, adv2):
    while adv1.HP >= 0 and adv2.HP >= 0:
        print(adv1)
        print(adv2)
        adv1.attack(adv2)
        if adv2.HP <= 0 and adv1.HP > 0:
            print(adv1)
            print(adv2)
            print(str(adv1.name) + ' wins!')
            db_insert(adv1.name, adv2.name, adv1.HP, adv2.HP, adv1.HP - adv2.HP, (str(adv1.name) + ' wins!'))
            return True
        adv2.attack(adv1)
        if adv1.HP <= 0 and adv2.HP > 0:
            print(adv1)
            print(adv2)
            print(str(adv2.name) + ' wins!')
            db_insert(adv1.name, adv2.name, adv1.HP, adv2.HP, adv2.HP - adv1.HP, (str(adv2.name) + ' wins!'))
            return False
        elif adv1.HP <= 0 and adv2.HP <= 0:
            print(adv1)
            print(adv2)
            print('Everyone loses!')
            db_insert(adv1.name, adv2.name, adv1.HP, adv2.HP, "Not applicable. Everyone lost", "Everyone loses!")
            return False
    if adv2.HP <= 0 and adv1.HP > 0:
            print(adv1)
            print(adv2)
            print(str(adv1.name) + ' wins!')
            db_insert(adv1.name, adv2.name, adv1.HP, adv2.HP, adv1.HP - adv2.HP, (str(adv1.name) + ' wins!'))
            return True
    elif adv1.HP <= 0 and adv2.HP > 0:
            print(adv1)
            print(adv2)
            print(str(adv2.name) + ' wins!')
            db_insert(adv1.name, adv2.name, adv1.HP, adv2.HP, adv2.HP - adv1.HP, (str(adv2.name) + ' wins!'))
            return False
    elif adv1.HP <=0 and adv2.HP <= 0:
            print(adv1)
            print(adv2)
            print('Everyone loses!')
            db_insert(adv1.name, adv2.name, adv1.HP, adv2.HP, "Not applicable. Everyone lost", "Everyone loses!")
            return False



# Problem B
#==========================================
# Purpose: This function takes in a list of adventurer objects and pits them all against each other. The list is first sorted by the HP of the adventurers and the two adventurers with the most HP are then pitted against each other with the adventurer with second most HP going first.
#          Whichever adventurer loses is removed from the list and the list is resorted with updated HP's from the previous duel. The entire process is repeated until one adventurer remains.
# Input Parameter(s): adv_list - a list of adventurer objects
# Return Value(s): The function returns None if an empty listis given as the starting list. Otherwise, the winner of the tournament is returned at the end.
#==========================================
def tournament(adv_list):
    if len(adv_list) == 0:
        return None
    if len(adv_list) == 1:
        return adv_list[0]
    else:
        new_ls = sorted(adv_list)
        result = duel(new_ls[-2], new_ls[-1])
        if result:
            new_ls = new_ls[:-1]
            return tournament(new_ls)
        else:
            new_ls.remove(new_ls[-2])
            return tournament(new_ls)

adv12 = Adventurer("real_adv1", 5, 5, 5, 5)
adv22 = Adventurer("real_adv2", 1, 1, 1, 1)
Thor = Fighter("Thor", 6, 5, 2, 3)
Wizard_Cloud = Wizard("Wizard Cloud", 4, 4, 1, 10)
duel(adv12, adv22)
duel(Thor, Wizard_Cloud)
tournament([Thor, adv12, adv22, Wizard_Cloud])
