Installation instruction
========================

Install `Anaconda python 3 <https://www.anaconda.com/download/>`_

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
optional step but highly recommended
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
* open anaconda navigator
* go to environment tab
* create new python 3 environment(name is irrelevant)
* in the environment tab select your newly created environment
* click the arrow and select open in terminal

^^^^^^^^^^^^^^^^^^^^^^^^^
dependencies installation
^^^^^^^^^^^^^^^^^^^^^^^^^
in terminal and type the following command

qt installation::

    conda install -c anaconda pyqt

vtk installation::

    conda install -c conda-forge vtk

tbb installation::

    conda install -c conda-forge tbb-devel

