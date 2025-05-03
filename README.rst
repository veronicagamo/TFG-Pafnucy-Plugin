.. |organization| replace:: scipion-chem
.. |repository| replace:: scipion-chem-pafnucy

========================================
Pafnucy Scipion Plugin
========================================
**Documentation under development, sorry for the inconvenience**

Scipion framework plugin for ligand–protein affinity prediction using the Pafnucy deep learning model.

========================================
Install this plugin
========================================
You will need to use `Scipion3 <https://scipion-em.github.io/docs/docs/scipion-modes/how-to-install.html>`_ to run these protocols.

Pafnucy and its dependencies will be installed automatically by the plugin.

- **Install the stable version**

    Through the plugin manager GUI by launching Scipion and following **Others** >> **Plugin Manager**

    or

.. parsed-literal::

    scipion3 installp -p \ |repository|\ 

- **Developer's version**

    1. Download the repository:

    .. parsed-literal::

        git clone https://github.com/\ |organization|\ /\ |repository|\ .git

    2. Install:

    .. parsed-literal::

        scipion3 installp -p /path/to/\ |repository|\  --devel

========================================
Protocols
========================================
This plugin provides the following protocols:

- **ProtChemPafnuncy**: Predicts ligand–protein binding affinity using Pafnucy.
- **ProtChemPafnuncyPrepare**: Prepares ligand–target complexes in the HDF5 format required by Pafnucy.

========================================
Packages & environments
========================================
Packages installed by this plugin can be found in ``/path/to/scipion/software/em/``.

The following conda environments will be created:

- pafnucy-``version``

As of now, Scipion does not automatically remove conda environments upon plugin uninstallation. Please consider manually removing this environment to free up disk space.

========================================
External software
========================================
This plugin integrates the following software:

.. _pafnucy: https://github.com/oddt/pafnucy
.. |pafnucy| replace:: **Pafnucy**

- |pafnucy|_: A deep learning model for protein–ligand binding affinity prediction based on 3D grid representations.

========================================
Changelog
========================================
All the recent version changes can be found `here <https://github.com/scipion-chem/scipion-chem-pafnucy/blob/devel/CHANGES.rst>`_.

