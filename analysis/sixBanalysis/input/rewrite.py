filename = "PrivateMC_2021/NMSSM_XYH_YToHH_6b_MX_700_MY_400.txt"

skip = [910, 721, 656, 651, 839, 793, 729, 671, 727, 650, 225, 681, 805, 653, 628, 734, 525, 945, 64, 938, 778, 674, 355, 519, 167, 165, 169, 162, 712, 568]

with open(filename, "w") as fi:
    for i in range(1,1000):
        if i in skip: continue
        fi.write(f'root://cmseos.fnal.gov//store/group/lpchbb/srosenzw/XYH_test_privateMC/CRAB_PrivateMC/srosenzw_NMSSM_XYH_YToHH_6b_MX_700_MY_400_sl7_nano_500k/210411_185620/0000/nanoAOD_step_{i}.root\n')

    fi.write('root://cmseos.fnal.gov//store/group/lpchbb/srosenzw/XYH_test_privateMC/CRAB_PrivateMC/srosenzw_NMSSM_XYH_YToHH_6b_MX_700_MY_400_sl7_nano_500k/210411_185620/0001/nanoAOD_step_1000.root\n')
