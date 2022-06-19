# Project Title

## Table of Contents

- [About](#about)
- [Demo](#demo)
- [Prerequisites](#prerequisites)
- [Installing](#installing)
- [Usage](#usage)

## About <a name = "about"></a>

Neat AI trying to learn how to play a small racing game<br/>

NeuroEvolution of Augmenting Topologies is a genetic algorithm<br/>
for the generation of evolving artificial neural networks developed by Ken Stanley in 2002.<br/>

I started with a population of 25 cars, fitness for each individual is equal to distance reached.
Fitness threshold is equal to 25 so whenever an individual reaches score 25, the simulation runs up
to the point where all cars are extinguished and doesn't repeat itself. After that, a winner.pkl file
is created with the champion genome.


## Demo <a name = "demo"></a>

![alt text](https://github.com/caiovini/Neat-racing/blob/main/Demo.gif)

### Prerequisites <a name = "prerequisites"></a>

Minimum "python 3.8"<br/>

Installation package "pip 22.0.4"

### Installing <a name = "installing"></a>

Install all dependencies:
```
pip3 install -r requirements.txt
```
## Usage <a name = "usage"></a>

Running the application:

```
python3 src/game.py
```