# PySide Jupyter Experiments

This repository contains some experiments with PySide and Jupyter about how to integrate PySide/Qt event loop with
IPykernel event loop.
The following experiments are available:

## Using Matplotlib event loop as most found examples do.

This is the simplest example, but it has some drawbacks:

- The matplotlib backend is forced to Qt and can't be changed, which prevents the use of other backends such as widgets
  in notebooks.

## Using IPython/asyncio event loop in conjunction with QAsync custom event loop.

This is slightly more complex, but it allows the use of any matplotlib backend.