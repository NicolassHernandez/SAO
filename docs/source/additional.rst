Changelog 
=========

Syntax
++++++
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
+++++++++++++++++++++

Tag a new version is done when enough advances were done.

.. code-block:: python
    
    git tag v1.1.0
    git push origin v1.1.0
    ./push_changelog.sh

To remove it make the following:

.. code-block:: python

    git tag -d v1.0.0
    git push origin :refs/tags/v1.0.0


Branches
========

Introduction
++++++++++++
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


Branch useful codes
+++++++++++++++++++

1. List of branches:

.. code-block:: python

    git branch -a

2. Creation of a local branch:

.. code-block:: python

    git checkout -b child
    git push origin child #pushing a local to create remote branch

3. Deletion of a branch:

.. code-block:: python

    git checkout -d child #normal
    git checkout -D child #forced
    git push origin --delete child #remote branch

4. Switch among branches

.. code-block:: python

    git checkout main
    git checkout child

5. Merge the content of a given branch into another

.. code-block:: python

    git checkout another
    git fetch origin
    git merge given
    git push origin another


Begin to work with issues
=========================

1) Clone the rpeository into your local machine:

.. code-block:: python

    git clone https://github.com/NicolassHernandez/SAO.git

2) Create an issue in github web and associate a local branch which is generated as:

.. code-block:: python

    git fetch origin
    git checkout 6-create-zernike

The number indicates the #number tag used to link with the issue.

3) After your work in that branch is done, you can merge with main and push it

.. code-block:: python

    git checkout main
    git merge 6-create-zernike
    git push origin main
    git branch -D 6-create-zernike

Your issue must be closed in github web and is automatically passed to clompeted stage.

To finally delete your local branch:

