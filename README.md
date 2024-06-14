# Snake AI
Made Snake game and trained computer to play it itself using g NeuroEvolution of Augmenting Topologies Genetic Algorithm

## How does it work
### Ai inputs
The ai gets 8 inputs from the game. The inputs are the distance from the snake to the 3 walls front left and right, the distance from head to snake body in three directions as well distance to the food in x and y.

### Ai Outputs
The inputs are then fed to the neural network. The output of the neural network is the direction (front,left,right) the snake should move in.The direction is chosen by taking the direction with the highest output value.

### Fitness function
The fitness function is the score of the snake. It is calculated using the following rules:

+1 if the snake gets closer to the food
-1 if the snake gets further from the food
+100 if the snake eats the food
-100 if the snake dies from starving
+0.1 for every frame the snake is alive
stop the game if the snake dies

### Training
The neural network is trained using the neat algorithm. The neat algorithm is a genetic algorithm that evolves the neural network to play the game. The neat algorithm is implemented in the neat-python library. The neat algorithm is explained in the [neat-python documentation](https://neat-python.readthedocs.io/en/latest/neat_overview.html).

### Visualization
The visualization of the neural network is done using graphviz (use the runcheck.py file to visualize checkpoints and winner). One can visualize all checkpoints and winners after training is done.

## Getting Started
### Installation
Clone the repo and the submodules

```
git clone --recurse-submodules https://github.com/om-khandwala/SnakeAI.git
```

Install the requirements

```
pip install -r requirements.txt
```

Train the game

```
python ai.py
```

### Usage
You can change settings in the ai.py file.

```
RUNS_PER_GAME=10
CORE_COUNT = multiprocessing.cpu_count()-4
GAME_SIZE=(200,200)
FOOD_TIMER=(max(GAME_SIZE[0],GAME_SIZE[1])//10) * 1.414
```

in the runcheck.py file.
```
CHECKPOINT_DIR = './checkpoint'
CONFIG = 'config'
GAME_SIZE=(200,200)
FOOD_TIMER=(max(GAME_SIZE[0],GAME_SIZE[1])//10) * 1.414
RUNWINNER=False
GUI=True
GRAPHS=False
SNAKE_SPEED=10
```