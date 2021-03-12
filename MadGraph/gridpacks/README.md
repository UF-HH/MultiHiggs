## Gridpack generation

Tools to generate the inputs to CMS gridpack scripts.
Instructions for use

1) clone the cms genproduction repository: https://github.com/cms-sw/genproductions
2) make a new folder ``NMSSM_XYH_YToHH_6b`` under ``genproductions/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/``
3) copy the ``Template`` folder and the ``generate_grid.py`` script in the folder created above
4) ``python generate_grid.py`` to generate inputs for a given mX, mY pair (you can edit the python file list)
5) run the gridpack generation scripts for every input (see instructions here: https://twiki.cern.ch/twiki/bin/viewauth/CMS/QuickGuideMadGraph5aMCatNLO )
