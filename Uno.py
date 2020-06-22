#Version 0.8 - Fix Wildcard Logic, and make +2/+4 cards
import random
import time
print("[]* = Skip, []% = Reverse, []+ = Draw 2, WC = Wildcard, WD = Wildcard (Draw 4)")
deck = [
"A1","A2","A3","A4","A5","A6","A7","A8","A9","A*","A%","A+",
"A1","A2","A3","A4","A5","A6","A7","A8","A9","A*","A%","A+",
"B1","B2","B3","B4","B5","B6","B7","B8","B9","B*","B%","B+",
"B1","B2","B3","B4","B5","B6","B7","B8","B9","B*","B%","B+",
"C1","C2","C3","C4","C5","C6","C7","C8","C9","C*","C%","C+",
"C1","C2","C3","C4","C5","C6","C7","C8","C9","C*","C%","C+",
"D1","D2","D3","D4","D5","D6","D7","D8","D9","D*","D%","D+",
"D1","D2","D3","D4","D5","D6","D7","D8","D9","D*","D%","D+",
"A0","B0","C0","D0","WC","WC","WC","WC","W#","W#","W#","W#"]
random.shuffle(deck)
hand = []
discard = []
current = []
while True:
  if deck[0][0] == "W" or deck[0][1] == "*" or deck[0][1] == "%" or deck[0][1] == "+":
    random.shuffle(deck)
  else:
    break
current = deck[0]
deck.remove(current)

def drawCard(hand, count):
  for i in range(0, count):
    if len(deck) == 0:
      for i in range(0, len(discard)):
        deck.append(discard[0])
      random.shuffle(deck)
      discard.clear()
      print("Reshuffled the deck!")
    hand.append(deck[0])
    deck.remove(deck[0])

players = int(input("Number of players 2-8 (one will be you): "))
if 1 < players < 9:
  for i in range(0, players):
    hand.append([])
order = []
for i in range(0, players):
  order.append(i)

for i in range(0, players):
  for ii in range(0, 7):
    hand[i].append(deck[0])
    deck.remove(deck[0])

win = 0
while win == 0:
  time.sleep(0.3)
  c = ""
  if order[0] == 0: #Player's Turn
    while True:
      print()
      hand[0].sort()
      print("Current: " + current)
      print(len(hand[0]), hand[0])
      play = input("Type card to play or \"draw\": ").upper()
      if play == "DRAW": #Draw card
        print("Drew " + deck[0] + "!")
        drawCard(hand[0], 1)
        if hand[0][-1][0] == current[0] or hand[0][-1][0] == "W" or hand[0][-1][1] == current[1]:
          play = hand[0][-1]
        else:
          break
      if play in hand[0] and play[0] == "W":
        while True:
          c = play[1]
          color = input("Type new letter to change to: ").upper()
          if 64 < ord(color) < 69:
            print("Played " + play + " and changed the letter to " + color + "!")
            break
          else:
            print("Illegal play!")
        discard.append(play)
        current = color + " "
        hand[0].remove(play)
        break
      elif play in hand[0] and play[0] == current[0] or play in hand[0] and play[1] == current[1]:
        if current[1] != " ": 
          discard.append(current)
        print("Played " + play + "!")
        current = play
        hand[0].remove(current)
        c = current[1]
        break
      else:
        print("Illegal play!")
    print()
  else: #AI's Turn
    card = ""
    x = 0
    for i in range(0, len(hand[order[0]])):
      if hand[order[0]][i][0] == current[0] and hand[order[0]][i][0] != "W": 
        card = hand[order[0]][i]
        x = 1
        break
      elif hand[order[0]][i][1] == current[1]:
        card = hand[order[0]][i]
        x = 1
        break
      elif hand[order[0]][i][0] == "W":
        card = hand[order[0]][i]
        c = hand[order[0]][i][1]
        x = 2
        break
    if x == 0:
      drawCard(hand[order[0]], 1)
      print("Player " + str(order[0]) + " drew a card! (" + str(len(hand[order[0]])) + " cards left)")
      if hand[order[0]][-1][0] == current[0] or hand[order[0]][-1][1] == current[1]:
        x = 1
        card = hand[order[0]][-1]
      elif hand[order[0]][-1][0] == "W":
        x = 2
        card = hand[order[0]][-1]
    if x == 1:
      if current[1] != " ":
        discard.append(current)
      current = card
      hand[order[0]].remove(current)
      print("Player " + str(order[0]) + " played " + current + "! (" + str(len(hand[order[0]])) + " cards left)")
      c = current[1]
    elif x == 2:
      r = ["A", "B", "C", "D"]
      random.shuffle(r)
      high = 0
      highcolor = ""
      for i in range(0, 4):
        check = 0
        for ii in range(0, len(hand[order[0]])):
          if hand[order[0]][ii][0] == r[i]:
            check = check + 1
        if check > high:
          high = check
          highcolor = r[i]
      discard.append(card)
      current = highcolor + " "
      hand[order[0]].remove(card)
      print("Player " + str(order[0]) + " played " + card + " and changed the color to " + highcolor + "! (" + str(len(hand[order[0]])) + " cards left)")
  if len(hand[order[0]]) == 0:
    print("Player " + str(order[0]) + " wins.")
    break
  if c == "%":
    if len(order) == 2:
      print("Player " + str(order[1]) + "'s turn was skipped! (" + str(len(hand[order[1]])) + " cards left)")
      for i in range(0, 2):
        order.append(order[0])
        order.remove(order[0])
    else:
      order.reverse()
      print("Turn order reversed!")
  elif c == "*":
    print("Player " + str(order[1]) + "'s turn was skipped! (" + str(len(hand[order[1]])) + " cards left)")
    for i in range(0, 2):
      order.append(order[0])
      order.remove(order[0])
  elif c == "+":
    drawCard(hand[order[1]], 2)
    print("Player " + str(order[1]) + " drew 2 cards and was skipped! (" + str(len(hand[order[1]])) + " cards left)")
    for i in range(0, 2):
      order.append(order[0])
      order.remove(order[0])
  elif c == "#":
    drawCard(hand[order[1]], 4)
    print("Player " + str(order[1]) + " drew 4 cards and was skipped! (" + str(len(hand[order[1]])) + " cards left)")
    for i in range(0, 2):
      order.append(order[0])
      order.remove(order[0])
  else:
    order.append(order[0])
    order.remove(order[0])