Changelog 
=========

Whenever, one can verify the current version:

.. code-block:: python

    git tag --list

To make a good changelog file, we must make a good commit description.
Changelog uses the following categories to distribute the documentation:

1. Features: Commits that add new functionality.
2. Fixes: Commits that address bugs.
3. Chores: Commits that are maintenance tasks or refactors.
4. Breaking Changes: Commits that introduce backward-incompatible changes.

Example:

.. code-block:: python

    git commit -m "feat: add user authentication"

Tagging a new version
~~~~~~~~~~~~~~~~~~~~~

Tag a new version is done when enough advances were done.

.. code-block:: python
    
    git tag v1.1.0
    git push origin v1.1.0
    ./push_changelog.sh

To remove it make the following:

.. code-block:: python

    git tag -d v1.0.0
    git push origin :refs/tags/v1.0.0


Branches scheme
===============

The project is designed in a three diagram, where the main branch is the stable one from which we can 
provide user-versions to test. Below main, we have three type of branches with their respective roles:

1. Features: Commits that add new functionality.
2. Fixes: Commits that address bugs.
3. Chores: Commits that are maintenance tasks or refactors.

Each of them, have specialized issues branches that attack specific task to accomplish. They are naimed with an 
issue number and that issue is described in the project management.

.. graphviz::

   digraph {
       node [shape=circle, style=filled, color=lightblue, fixedsize=false];
       edge [color=gray, fontcolor=black];

       A [label="master"];
       B [label="main", shape=box, color=gray];

       C [label="fix/issue#3",width=1.5,height=1.5];
       D [label="chor/issue#45",width=1.5,height=1.5];
       E [label="feat/issue#13", width=1.5,height=1.5];

       A -> B [ dir="both",label="IC,PR,R requirements"];

       B -> C [ dir="both"];
       B -> D [ dir="both"];
       B -> E [label="IC requirement", dir="both"];
   }

