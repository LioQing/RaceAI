# RaceAI

A personal project to create a self-driving car using evolutionary machin learning and neural networks.

⚠️⚠️⚠️ This repository has been archived, further development will continue in [LioQing/simple-rl-driver](https://github.com/lioqing/simple-rl-driver) ⚠️⚠️⚠️

## Video


https://user-images.githubusercontent.com/46854695/230703415-a9d00dc5-63f5-42a6-ab50-9c155a94f627.mp4


## Features

- A track editor
- Configuration of population and reproduction process
- Player controlled car

## Techniques Used

- Evolutionary machine learning
- Multi-layer perceptron neural network
- Gradient descent

## Notes

- The neural network is trained to drive on the track.
  - It is not fast.
  - There are instances where it will stop driving forward.
- The neural network is not trained to make sharp turns.
  - It can at most make a around 120 degree turn if the turn is wide enough.
  - It can generally make a 90 degree turn safely.
