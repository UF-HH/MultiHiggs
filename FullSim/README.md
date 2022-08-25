## Instructions to produce private MC samples

You can follow the example contained in ``Era_2018/NMSSM_XYH_YToHH_6b_MX_600_MY_400``

1. log into a **sl7 machine** (you can to that on fnal)
2. ``cmsrel CMSSW_10_6_19_patch2``
3. ``cd CMSSW_10_6_19_patch2/src ; git clone https://github.com/UF-HH/sixB``
4. under ``FullSim/Summer2018UL`` create a folder for the sample you want to produce
5. copy the Template folder contents and the corresponding gridpack into that folder.
6. edit the gridpack name in ``genSim_step.py``
7. in ``crabConfig.py``, edit the gridpack name, the files to send, and the request and output
8. submit ``crabConfig.py`` on CRAB using ``crab submit crabConfig.py``

NOTE: you can create both mini and nanoAOD (set the sequence you need in ``scriptExe.sh``). Using ``miniAOD_step_fake.py`` or ``nanoAOD_step_fake.py`` in the ``crabConfig.py`` will tell CRAB what type of output file to transmit to the storage.

Quick instructions to build more folders starting from the example one.
Assumes that all the gridpacks and outputs are called the same and just differ for the mass values

```
# copy gridpacks
for d in NMSSM_XYH_YToHH_6b_MX_450_MY_300 NMSSM_XYH_YToHH_6b_MX_500_MY_300 ; do cp NMSSM_XYH_YToHH_6b_MX_600_MY_400/* $d ; cp ${d}_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz ${d} ; done

# change inputs
for d in NMSSM_XYH_YToHH_6b_MX_450_MY_300 NMSSM_XYH_YToHH_6b_MX_500_MY_300 ; do cd ${d}; sed -i "s/NMSSM_XYH_YToHH_6b_MX_600_MY_400/${d}/" genSim_step.py ; sed -i "s/NMSSM_XYH_YToHH_6b_MX_600_MY_400/${d}/" crabConfig.py ; cd .. ; done

# submit to CRAB
for d in NMSSM_XYH_YToHH_6b_MX_450_MY_300 NMSSM_XYH_YToHH_6b_MX_500_MY_300 ; do echo $d; cd $d ; crab submit -c crabConfig.py ; cd .. ; done
```