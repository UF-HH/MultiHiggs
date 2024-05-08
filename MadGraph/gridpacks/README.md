## Gridpack generation

Tools to generate the inputs to CMS gridpack scripts.
Instructions for use

1) clone the cms genproduction repository: https://github.com/cms-sw/genproductions with ``git clone https://github.com/cms-sw/genproductions.git --depth=1``
2) make a new folder ``NMSSM_XYH_YToHH_6b`` under ``genproductions/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/``
3) copy the ``Template`` folder and the ``generate_grid.py`` script in the folder created above
4) ``python generate_grid.py`` to generate inputs for a given mX, mY pair (you can edit the python file list)
5) run the gridpack generation scripts for every input (see instructions here: https://twiki.cern.ch/twiki/bin/viewauth/CMS/QuickGuideMadGraph5aMCatNLO )

NOTE: The current master branch (as of 08/2021) is the recommended default for UL production
[1] [Info for MC production for Ultra Legacy Campaigns 2016, 2017, 2018](https://cms-pdmv.gitbook.io/project/mccontact/info-for-mc-production-for-ultra-legacy-campaigns-2016-2017-2018)
[2] https://github.com/cms-sw/genproductions/


