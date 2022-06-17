import math


allcards = ["1", "2", "3", "4", "5", "5", "7", "7", "9", "11", "11", "13", "14", "15", "17", "h1",
            "h1", "h2", "h2", "h2", "h3", "h3", "h3", "h4", "h4", "h4", "h5", "h5", "h5", "a", "a", "a", "a", "a"]
onboard = []
bannedcards = []

# ask the user for the number of players
players = int(input("How many players? "))
totalplayers = players
pointstoearn = 0

# a function that safely parses as int cardsleft and sums all values


def sumcardsleft():
    sum = 0
    for i in cardsleft:
        # if i starts with a, it is worth 5 points if more than 2 are left, otherwise it is worth 10 points
        if i[0] == "a":
            # if there are more than 2 instances of "a" in cardsleft, it is worth 5 points
            if cardsleft.count("a") + onboard.count("a") > 2:
                sum += 5
            # otherwise it is worth 10 points
            else:
                sum += 10
        # if i starts with h, it is worth 0 points
        elif i[0] == "h":
            sum += 0
        # else it is worth the value of i
        else:
            sum += int(i)
    return sum

# a function that returns the expected artifact value if leaving


def expectedartifactvalue():
    sum = 0
    for i in onboard:
        # if i starts with a, it is worth 5 points if more than 2 are left, otherwise it is worth 10 points
        if i[0] == "a":
            # if there are more than 2 instances of "a" in cardsleft, it is worth 5 points
            if cardsleft.count("a") + onboard.count("a") > 2:
                sum += 5
            # otherwise it is worth 10 points
            else:
                sum += 10
        # if i starts with h, it is worth 0 points
        elif i[0] == "h":
            sum += 0

    return sum

# a function that returns the chance of losing the game


def chanceoflosing():
    sum = 0
    for i in cardsleft:
        # if i starts with an h and there is already a matching entry in onboard, we lose
        if i[0] == "h" and onboard.count(i) > 0:
            sum += 1
    return sum / len(cardsleft)


# do five times
for i in range(5):
    players = totalplayers
    gemsleft = 0
    pointstoearn = 0
    onboard = []
    lost = False
    cardsleft = allcards.copy()
    # remove banned cards from cardsleft
    for i in bannedcards:
        cardsleft.remove(i)

    # print new game
    print("New game")

    # while there are players left
    while players > 0 and len(cardsleft) > 0:
        # ask player how many people left, then decrement players by that amount
        peoplewholeft = int(input("How many people have left? "))
        players -= peoplewholeft
        # if there are no players left, break out of the loop
        if players <= 0:
            break
        # if people have left, gemsleft is the remainder of gemsleft divided by how many people left
        if peoplewholeft > 0:
            gemsleft += gemsleft % peoplewholeft
            # remove all instances of "a" in hazards if one person left
            if peoplewholeft == 1:
                # ban all recovered artifacts
                for i in range(onboard.count("a")):
                    bannedcards.append("a")
                # remove all instances of "a" in onboard
                onboard = [i for i in onboard if i != "a"]

        userinput = "x"
        # if the input is not in cardsleft, ask again
        while userinput not in cardsleft:
            userinput = input("Enter the card: ")

        cardsleft.remove(userinput)
        # get card value as int if inpput does not begin with h or with an a
        if userinput[0] != "h" and userinput[0] != "a":
            value = int(userinput)
            # points to earn is incremented by the euclidian division of the card value by the number of players, and gemsleft is the remainder
            pointstoearn += math.floor(value / players)
            gemsleft = value % players
        # else add it to onboard
        else:
            onboard.append(userinput)
            hazards = ["h1", "h2", "h3", "h4", "h5"]
            for h in hazards:
                # if h is in onboard twice, end the game
                if onboard.count(h) == 2:
                    print("You have two " + h + " on board. You lose.")
                    # ban unrecovered artifacts
                    for i in range(onboard.count("a")):
                        bannedcards.append("a")
                    # ban killing hazard
                    bannedcards.append(userinput)
                    # set lost flag
                    lost = True
                    break
            # if we lost, break out of the loop
            if lost:
                break

        # if there are no cards left, break out of the loop
        if len(cardsleft) == 0:
            break

        # the expected value of leaving is the currents points to earn + the gems left on the board
        leaving = pointstoearn + gemsleft + expectedartifactvalue()
        # the expected value of staying is the current points to earn plus the average value of pulling a card
        staying = pointstoearn + ((sumcardsleft() / len(cardsleft))/players)

        losing = chanceoflosing()
        notlosing = 1 - losing

        # print the expected value of leaving, the expected value of staying, and the chance of losing
        print("Expected value of leaving now: " + str(leaving))
        print("Expected value of staying 1 round, without leftover gems and artifacts: " + str(staying))
        print("Expected value of staying 1 round, with all leftover gems and artifacts: " +
              str(staying + gemsleft + expectedartifactvalue()))

        # print chance of losing in percent
        print("Chance of losing: " + str(losing * 100) + "%")
        # print chance of not losing in percent
        print("Chance of not losing: " + str(notlosing * 100) + "%")
        print("")
