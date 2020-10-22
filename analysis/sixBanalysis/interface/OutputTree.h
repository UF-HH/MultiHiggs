#ifndef OUTPUTTREE_H
#define OUTPUTTREE_H

/**
** class  : OutputTree
** author : L. Cadamuro (UF)
** date   : 10/01/2018
** brief  : the output tree of the skims
** NOTE   : for every new variable added:
**        : 1) add the member variable
**        : 2) add the corresponing branch in init_branches()
**        : 3) set the variable clearing in clear()
**        :
**        : remember that the variables are set (from the EventInfo) in the SkimUtils::fill_output_tree function
**        : so put the set instructions of the new variables there
**/

#include "TTree.h"
#include "Math/Vector4D.h"
typedef ROOT::Math::PtEtaPhiMVector p4_t;

#include "UserValCollection.h"
#include <string>
#include <memory>

// helper: declares the m/pt/eta/phi/p4 of a variable OBJ
#define DECLARE_m_pt_eta_phi_p4(OBJ) \
    float OBJ ## _m; \
    float OBJ ## _pt; \
    float OBJ ## _eta; \
    float OBJ ## _phi; \
    p4_t  OBJ ## _p4;

// helper: declares the m/pt/eta/phi/p4 of a variable OBJ
#define DECLARE_m_pt_ptRegressed_eta_phi_p4(OBJ) \
    float OBJ ## _m; \
    float OBJ ## _pt; \
    float OBJ ## _ptRegressed; \
    float OBJ ## _eta; \
    float OBJ ## _phi; \
    p4_t  OBJ ## _p4;

class OutputTree {
    
    public:
        OutputTree (bool savetlv = false, std::string name = "sixBtree", std::string title = "sixBtree");
        ~OutputTree(){};
        
        void clear(); // to be called to reset the var values
        int fill()  {return tree_->Fill();}
        int write() {return tree_->Write();}
    
        // returns false if the branch could not be created, true if all ok
        // thje second optional value specifies what the branch should be reset to at clear()
        bool declareUserIntBranch   (std::string name, int defaultClearValue = 0);
        bool declareUserFloatBranch (std::string name, float defaultClearValue = 0.0);
        //XYH
        bool declareUserIntBranchList(std::vector<std::string> nameList, int defaultClearValue = 0);

        // throws an exception if the branch name was not declared
        int&   userInt   (std::string name) {return userInts_   . getVal(name);}
        float& userFloat (std::string name) {return userFloats_ . getVal(name);}

        //////////////////////////
        //// saved variables
        //////////////////////////

        unsigned int           Run;
        unsigned int           LumiSec;
        unsigned long long int Event;

        DECLARE_m_pt_eta_phi_p4(gen_X_fc);
        DECLARE_m_pt_eta_phi_p4(gen_X);
        DECLARE_m_pt_eta_phi_p4(gen_Y);
        DECLARE_m_pt_eta_phi_p4(gen_HX);
        DECLARE_m_pt_eta_phi_p4(gen_HY1);
        DECLARE_m_pt_eta_phi_p4(gen_HY2);

        DECLARE_m_pt_eta_phi_p4(gen_HX_b1);
        DECLARE_m_pt_eta_phi_p4(gen_HX_b2);
        DECLARE_m_pt_eta_phi_p4(gen_HY1_b1);
        DECLARE_m_pt_eta_phi_p4(gen_HY1_b2);
        DECLARE_m_pt_eta_phi_p4(gen_HY2_b1);
        DECLARE_m_pt_eta_phi_p4(gen_HY2_b2);

        DECLARE_m_pt_eta_phi_p4(gen_HX_b1_genjet);
        DECLARE_m_pt_eta_phi_p4(gen_HX_b2_genjet);
        DECLARE_m_pt_eta_phi_p4(gen_HY1_b1_genjet);
        DECLARE_m_pt_eta_phi_p4(gen_HY1_b2_genjet);
        DECLARE_m_pt_eta_phi_p4(gen_HY2_b1_genjet);
        DECLARE_m_pt_eta_phi_p4(gen_HY2_b2_genjet);

        DECLARE_m_pt_ptRegressed_eta_phi_p4(gen_HX_b1_recojet);
        DECLARE_m_pt_ptRegressed_eta_phi_p4(gen_HX_b2_recojet);
        DECLARE_m_pt_ptRegressed_eta_phi_p4(gen_HY1_b1_recojet);
        DECLARE_m_pt_ptRegressed_eta_phi_p4(gen_HY1_b2_recojet);
        DECLARE_m_pt_ptRegressed_eta_phi_p4(gen_HY2_b1_recojet);
        DECLARE_m_pt_ptRegressed_eta_phi_p4(gen_HY2_b2_recojet);
        int gen_bs_N_reco_match;
        int gen_bs_N_reco_match_in_acc;
        double gen_bs_match_recojet_minv;
        double gen_bs_match_in_acc_recojet_minv;

        DECLARE_m_pt_eta_phi_p4(X);
        DECLARE_m_pt_eta_phi_p4(Y);
        DECLARE_m_pt_eta_phi_p4(HX);
        DECLARE_m_pt_eta_phi_p4(HY1);
        DECLARE_m_pt_eta_phi_p4(HY2);

        DECLARE_m_pt_ptRegressed_eta_phi_p4(HX_b1);
        DECLARE_m_pt_ptRegressed_eta_phi_p4(HX_b2);
        DECLARE_m_pt_ptRegressed_eta_phi_p4(HY1_b1);
        DECLARE_m_pt_ptRegressed_eta_phi_p4(HY1_b2);
        DECLARE_m_pt_ptRegressed_eta_phi_p4(HY2_b1);
        DECLARE_m_pt_ptRegressed_eta_phi_p4(HY2_b2);


        // DECLARE_m_pt_eta_phi_p4(gen_H1)
        // DECLARE_m_pt_ptRegressed_eta_phi_p4(HH_btag_b1)
        
    
    private:
        void init_branches();
        std::unique_ptr<TTree> tree_;
        const bool savetlv_;
        
        // for user declared branches
        UserValCollection<float> userFloats_;
        UserValCollection<int>   userInts_;
};

#endif
