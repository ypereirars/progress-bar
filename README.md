# A Simple Progress Bar
It's a simple progress bar similar to the one in Tensorflow.

## Motivation
Learn how to write and overwrite to console and config setup of a project.

## How to Use
First clone the project then install it:

```bash
$ git clone https://github.com/ypereirars/progress-bar.git 
$ pip install .
```
Then import the bar and use it:
```
from progress_bar import ProgressBar

bar = ProgressBar(100)
for _ in range(100):
    bar.update()
```
Once it's bar is fully filled, the `update` method calls `finish`, producing the following output:

```
100/100 [===============================] - 9.93s 0.0993s/sample - loss: 3.0319 accuracy: 0.8784
```

_Any comments and suggestions are welcome!_