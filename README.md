# ShapeshifterHtml
Attempt to create a good search algorithm to solve Neopet's Shapeshifter Game.

The goal is to use all the rotation pieces to make the entire board the goal picture.

![shapeshifterscreenshot](https://i.imgur.com/uqD0tvT.png)

Example of the hardest level:
https://www.youtube.com/watch?v=M0fklfvPfAQ

Playing it yourself:
http://www.neopets.com/games/game.phtml?game_id=151

You can use my account:

username: shapeshiftersolver

password: algorithm123

## How to Use

## HTML Parser
We are fetching the board through html parsing, and saving it to a txt file

## Search Heuristics
### Heuristic 1: Blind equidistance from goal state

```
return sum(sum([bool(y != problem.goal_rank) for y in x]) for x in gamemap)
```

Nodes Expanded on Test Case: 47859

### Heuristic 2: Blind equidistance distance from goal state if there are enough pieces remaining to rotate four corners, otherwise weighted sum of distances from goal state

```
    if (len(piecesleft) > 7):
        for x in gamemap:
            for y in x:
                htotal = (htotal + y) #the more rotations the further away
    else:
        for x in gamemap:
            for y in x:
                htotal = htotal + bool(y != problem.goal_rank) #the more rotations, the less of a difference
```

Nodes Expanded on Test Case: 13691

## Built With
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) - HTML Parser for Python

## Authors

* **Andrew Young** - [Github](https://github.com/catatonicTrepidation/)
* **Brian Cai** - [Github](https://github.com/brian-cai)
