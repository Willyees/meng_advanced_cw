coursework advanced_software_development 2019/2020

# Aim
Build a working software applied to the previous chosen coursework research

# Research
Implementation of blockchain architecture, especially in financial systems. Researched different types of proof of work usable

# Implementation
The project has been implemented as a web application using Python and Flask framework. 
Simple blockchain implementation utilising proof of work consensus.

The node architecture follows the below figure

![node_architecture](https://github.com/Willyees/meng_advanced_cw/blob/assets/assets/block_arch.png)

The chain is secured and hardly modifiable by linking to the parent block using their hash. It has been used a simplified version of the below proposed architecture without implementing the Merkel Trees.

![block_architecture](https://github.com/Willyees/meng_advanced_cw/blob/assets/assets/block_components.png)

# Features
Multiple nodes can be started locally at different ports. Nodes can be made peers by letting other nodes to learn their node addresses. This is easily done by using the tool POSTMAN and creating a POST request to /register-with
![postman_register-with](https://github.com/Willyees/meng_advanced_cw/blob/assets/assets/register_with.png)

Once they are added, the address /peers can be used to check which peers have been connected
![peers](https://github.com/Willyees/meng_advanced_cw/blob/assets/assets/peers.png)


A central node at port :5000 can be used to governate the creation of new transactions that will be put into new blocks.
![central_node](https://github.com/Willyees/meng_advanced_cw/blob/assets/assets/gui.png)

Additionally it can be used to start the mining process in the other peer nodes that have been linked together.


Proof of work used as consensus mechanism. Once the block has been mined is propagated to the whole network and the chain can be checked at the address /chain
![chain](https://github.com/Willyees/meng_advanced_cw/blob/assets/assets/chain.png)


# Instructions
More in detail instructions can be found in [this](https://github.com/Willyees/meng_advanced_cw/blob/master/src/howtouse.txt) file.
