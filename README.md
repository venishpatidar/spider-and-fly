# Spider and Fly
This program aims to compare the performance of the Multiagent Rollout algorithm against the Ordinary Rollout algorithm and the Base Policy in the context of the Spiders and Flies problem. 

The Spiders and Flies problem from Bertsekas, D. P. 2024. A Course in Reinforcement Learning. Athena Scientific p103-105 involves a scenario with multiple spiders and stationary flies on a 2- dimensional grid. The spiders aim to catch all flies as quickly as possible. The control space is structured to have separate controls for each spider (Ex: Consider 2 spiders then the control space will consist list of two separate controls for each spider say [‘west’, ‘north’]). In this implementation, we implemented three different strategies that an agent will use: Base Policy, Ordinary Rollout, and Multiagent Rollout and aims to compare the perfomance of these methods.

## Base policy
![Base Policy](./outputs/base_policy.gif?raw=true "Base Policy") <br>
Utilized Manhattan distance to the nearest fly as the base policy

## Oridnary Rollout acting on Base Policy
![Ordinary Rollout](./outputs/base_policy.gif?raw=true "Ordinary Rollout")<br>
Computed and compared Q-factors for each possible move of each spider.


## Multi Agent Rollout acting on Base Policy
![Multi Agent Rollout](./outputs/base_policy.gif?raw=true "Multi Agent Rollout")<br>
For each spider, we compute and compare (taking into consideration all the
controls of the current spider) the Q-factor for the current spider and assume the future spiders will act according to base policy, and the previous spider has already chosen their control.


## Program Structure
`Graphics.py` <br>
Contains code for rendering spiders and flies and handling graphic elements of the game.

`Spider.py`
<ul>
    <li>Contains the code for returning the control set based on a given state and Contains core logic for all three algorithms.</li>
    <li>Base Policy class: Implements the Manhattan distance-based base policy. o Ordinary Rollout class: Implements the standard rollout strategy.</li>
    <li>Multiagent Rollout class: Implements the multiagent rollout strategy.</li>
</ul>

`Fly.py`<br>
Contains code for simulating the random movement of flies (currently unused as flies are
stationary).

`Game.py`
The core of the program includes rules of the game, sets up the environment, and metadata,keeps track of the game state, and grid, and places spiders and flies