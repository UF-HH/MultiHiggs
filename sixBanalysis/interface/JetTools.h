#ifndef JETFUNCTIONS_H
#define JETFUNCTIONS_H

/**
** class  : Jet_functions
** author : L. Cadamuro (UF)
** date   : 16/10/2020
** brief  : Functions for generic handling of jets (scale, smear, etc..)
**/

#include "Jet.h"
#include "NanoAODTree.h"
#include <vector>

class JetFunctions{
    
    public:
        void init_smear(std::string JERScaleFactorFile, std::string JERResolutionFile, int random_seed);

        std::vector<Jet> smear_jets(NanoAODTree& nat, std::vector<Jet> input_jets, Variation variation);

    private:
        std::unique_ptr<JME::JetResolutionScaleFactor> jetResolutionScaleFactor_;
        std::unique_ptr<JME::JetResolution>            jetResolution_;

};

#endif // JETFUNCTIONS_H