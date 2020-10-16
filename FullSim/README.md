## Instructions to produce private MC samples

You can follow the example contained in ``Era_2018/NMSSM_XYH_YToHH_6b_MX_600_MY_400``

1. log into a **sl6 machine** (you can to that on lxplus)
2. ``cmsrel CMSSW_10_2_22``
3. ``cd CMSSW_10_2_22/src ; git clone https://github.com/UF-HH/sixB``
4. under ``FullSim/Era_2018`` create a folder for the sample you want to produce
5. copy the gridpack into that folder. Some 13 TeV gridpacks are available here: ``/eos/uscms/store/user/lcadamur/NMSSM_XYH_YToHH_6b_gridpacks``
6. edit the gridpack name into ``genSim_step.py``
7. in ``crabConfig.py``, edit the gridpack name into the files to send and the request and output
8. submit ``crabConfig.py`` on CRAB

NOTE: you can create both mini and nanoAOD (set the sequence you need in ``scriptExe.sh``). Using ``miniAOD_step_fake.py`` or ``nanoAOD_step_fake.py`` in the ``crabConfig.py`` will tell CRAB what type of output file to transmit to the storage.

