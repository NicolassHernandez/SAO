Welcome to Adaptive Optics Simulation Documentation!
====================================================

Introduction
++++++++++++
AOS is an attempt to gather together many common tools, equations and functions for Adaptive Optics.
The idea is to provide an alternative to the current model, where a new AO researcher must write their own library
of tools, many of which implement theory and ideas that have been in existance for over 20 years. AOS will hopefully
provide a common place to put these tools, which through use and bug fixes, should become reliable and well documented.

Installation
------------
AOS uses mainly standard library functions, and all attempts have been made to avoid adding unneccessary dependencies.
Currently, the library requires only

- numpy
- scipy
- astropy
- matplotlib

As shown in :numref:`my-figure-label`, the image demonstrates the main feature.

.. _my-figure-label:

.. figure:: _static/images/github-mark.png
   :alt: My Image Alt Text
   :align: center
   :width: 100px

Here is an example of Python code:

.. code-block:: python

   def hello_world():
      print("Hello, World!")

   hello_world()

Contents
++++++++

.. toctree::
   :maxdepth: 2
   :caption: Introduction

   pupil
   poisson_tutorial.ipynb

.. toctree::
   :maxdepth: 2
   :caption: First steps


.. toctree::
   :maxdepth: 2
   :caption: Managing the project

   additional


Here is a numbered equation:

.. math::
   :label: eq-einstein

   E = mc^2

As shown in :eq:`eq-einstein`, the equation for energy is given by Einstein.


Contributors
==================
1. Nicolás Hernández
2. Arturo Mardones
3. Benjamin Gonzalez
4. Rodrigo muñoz
