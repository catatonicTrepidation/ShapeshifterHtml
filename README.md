# ShapeshifterHtml
Using A* to solve Neopet's Shapeshifter Game.

The goal is to use all the rotation pieces to make the entire board the goal picture.

Still looking for better heuristics, and optimizing speed. (It gets pretty slow when the board is large enough)

<img src="https://i.imgur.com/uqD0tvT.png" height="50%" width="50%">

Example of the hardest level:
https://www.youtube.com/watch?v=M0fklfvPfAQ

Playing it yourself:
http://www.neopets.com/games/game.phtml?game_id=151

You can use my account:

username: shapeshiftersolver

password: algorithm123

## How to Use

### Command Line
Open Terminal, or whatever you have python on and run `python shapeshifter.py` or `python3 shapeshifter.py` or whatever floats your boat

### Using your own levels
While collecting html puzzles, it occurred to me that the puzzle actually dynamically changes. To replace the puzzle, just inspect the element and select 'edit as html', and save the contents as `something.html`

Example: 

<img src="https://i.imgur.com/hLT7Mgf.png" height="50%" width="50%">


Inside shapeshifter.py, you just change the html file listed in

```gamemap, pieces, cycle, goalpiece = shapeshifter_html.get_shapeshifter_config('htmllevels/level4.html')```

## Understanding the code

### HTML Parser
We are fetching the board through html parsing, and saving it to a txt file via `shapeshifter_html.py`

### Search Heuristics

We are using Berkeley AI's skeleton (CS188) for A* search in `search.py` and their Counter for the dictionary in `util.py`.

We originally received the skeleton code from Georgia Tech's CS3600 class and implemented it ourselves. 

For all our heuristics we tested it on the "hard coded" level in `search.py`

#### Heuristic 1: Blind equidistance from goal state

```
return sum(sum([bool(y != problem.goal_rank) for y in x]) for x in gamemap)
```

Nodes Expanded on Test Case: 47859

#### Heuristic 2: Blind equidistance distance from goal state if there are enough pieces remaining to rotate four corners, otherwise weighted sum of distances from goal state

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
