#include "SkimUtils.h"

#include "Math/Vector4D.h"
typedef ROOT::Math::PtEtaPhiMVector p4_t;

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

// helper: copies the pt/eta/phi/p4 branches from a candidate OBJ to the output tree
// NOTE: requires the matching of the names (and enforces it)
#define COPY_m_pt_eta_phi_p4(OBJ) \
    ot.OBJ ## _m   = ei. OBJ -> P4().M(); \
    ot.OBJ ## _pt  = ei. OBJ -> P4().Pt(); \
    ot.OBJ ## _eta = ei. OBJ -> P4().Eta(); \
    ot.OBJ ## _phi = ei. OBJ -> P4().Phi(); \
    ot.OBJ ## _p4  = ei. OBJ -> P4();

#define COPY_m_pt_ptRegressed_eta_phi_p4(OBJ) \
    ot.OBJ ## _m            = ei. OBJ -> P4().M(); \
    ot.OBJ ## _pt           = ei. OBJ -> P4().Pt(); \
    ot.OBJ ## _ptRegressed  = ei. OBJ -> P4Regressed().Pt(); \
    ot.OBJ ## _eta          = ei. OBJ -> P4().Eta(); \
    ot.OBJ ## _phi          = ei. OBJ -> P4().Phi(); \
    ot.OBJ ## _p4           = ei. OBJ -> P4();

//helperM same as above, but encloses the obj (a boost::optional is expected) in a if clause to check whether it is initialized
#define COPY_OPTIONAL_m_pt_eta_phi_p4(OBJ) \
    if (ei.OBJ) { \
        ot.OBJ ## _m   = ei. OBJ -> P4().M(); \
        ot.OBJ ## _pt  = ei. OBJ -> P4().Pt(); \
        ot.OBJ ## _eta = ei. OBJ -> P4().Eta(); \
        ot.OBJ ## _phi = ei. OBJ -> P4().Phi(); \
        ot.OBJ ## _p4  = ei. OBJ -> P4(); \
    }

#define COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(OBJ) \
    if (ei.OBJ) { \
    ot.OBJ ## _m            = ei. OBJ -> P4().M(); \
    ot.OBJ ## _pt           = ei. OBJ -> P4().Pt(); \
    ot.OBJ ## _ptRegressed  = ei. OBJ -> P4Regressed().Pt(); \
    ot.OBJ ## _eta          = ei. OBJ -> P4().Eta(); \
    ot.OBJ ## _phi          = ei. OBJ -> P4().Phi(); \
    ot.OBJ ## _p4           = ei. OBJ -> P4();\
    }
// --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - --- - 

int SkimUtils::appendFromFileList (TChain* chain, string filename)
{
    //cout << "=== inizio parser ===" << endl;
    std::ifstream infile(filename.c_str());
    std::string line;
    int nfiles = 0;
    while (std::getline(infile, line))
    {
        line = line.substr(0, line.find("#", 0)); // remove comments introduced by #
        while (line.find(" ") != std::string::npos) line = line.erase(line.find(" "), 1); // remove white spaces
        while (line.find("\n") != std::string::npos) line = line.erase(line.find("\n"), 1); // remove new line characters
        while (line.find("\r") != std::string::npos) line = line.erase(line.find("\r"), 1); // remove carriage return characters
        if (!line.empty()) // skip empty lines
        {
            chain->Add(line.c_str());
            ++nfiles;
        }
     }
    return nfiles;
}


void SkimUtils::fill_output_tree(OutputTree& ot, NanoAODTree& nat, EventInfo& ei)
{

    // set the variables for resonant analysis
    ot.Run      = *ei.Run;
    ot.LumiSec  = *ei.LumiSec;
    ot.Event    = *ei.Event;

    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_X_fc);
    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_X);
    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_Y);
    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HX);
    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY1);
    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY2);

    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HX_b1);
    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HX_b2);
    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY1_b1);
    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY1_b2);
    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY2_b1);
    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY2_b2);

    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HX_b1_genjet);
    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HX_b2_genjet);
    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY1_b1_genjet);
    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY1_b2_genjet);
    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY2_b1_genjet);
    COPY_OPTIONAL_m_pt_eta_phi_p4(gen_HY2_b2_genjet);

    COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_HX_b1_recojet);
    COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_HX_b2_recojet);
    COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_HY1_b1_recojet);
    COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_HY1_b2_recojet);
    COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_HY2_b1_recojet);
    COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(gen_HY2_b2_recojet);
    if (ei.gen_bs_N_reco_match)        ot.gen_bs_N_reco_match        = *ei.gen_bs_N_reco_match;
    if (ei.gen_bs_N_reco_match_in_acc) ot.gen_bs_N_reco_match_in_acc = *ei.gen_bs_N_reco_match_in_acc;
    if (ei.gen_bs_match_recojet_minv)        ot.gen_bs_match_recojet_minv        = *ei.gen_bs_match_recojet_minv;
    if (ei.gen_bs_match_in_acc_recojet_minv) ot.gen_bs_match_in_acc_recojet_minv = *ei.gen_bs_match_in_acc_recojet_minv;

    COPY_OPTIONAL_m_pt_eta_phi_p4(X);
    COPY_OPTIONAL_m_pt_eta_phi_p4(Y);
    COPY_OPTIONAL_m_pt_eta_phi_p4(HX);
    COPY_OPTIONAL_m_pt_eta_phi_p4(HY1);
    COPY_OPTIONAL_m_pt_eta_phi_p4(HY2);

    COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HX_b1);
    COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HX_b2);
    COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HY1_b1);
    COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HY1_b2);
    COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HY2_b1);
    COPY_OPTIONAL_m_pt_ptRegressed_eta_phi_p4(HY2_b2);

    // fill the tree
    ot.fill();

}

void SkimUtils::init_gen_weights(OutputTree &ot, NormWeightTree &nwt)
{
    // create userfloats for systematics read from file directly
    auto& gen_weight   = nwt.get_gen_weight();
    auto& pu_weight    = nwt.get_pu_weight();
    auto& pdf_weight   = nwt.get_pdf_weight();
    auto& scale_weight = nwt.get_scale_weight();
    auto& ps_weight    = nwt.get_ps_weight();

    ot.declareUserFloatBranch(gen_weight.name, 1.0);
    for (auto n : gen_weight.syst_name)
        ot.declareUserFloatBranch(n, 1.0);

    ot.declareUserFloatBranch(pu_weight.name, 1.0);
    for (auto n : pu_weight.syst_name)
        ot.declareUserFloatBranch(n, 1.0);

    ot.declareUserFloatBranch(pdf_weight.name, 1.0);
    for (auto n : pdf_weight.syst_name)
        ot.declareUserFloatBranch(n, 1.0);

    ot.declareUserFloatBranch(scale_weight.name, 1.0);
    for (auto n : scale_weight.syst_name)
        ot.declareUserFloatBranch(n, 1.0);

    ot.declareUserFloatBranch(ps_weight.name, 1.0);
    for (auto n : ps_weight.syst_name)
        ot.declareUserFloatBranch(n, 1.0);
}

void SkimUtils::copy_gen_weights(OutputTree &ot, NormWeightTree &nwt)
{
    // copy the values and the structures for systematics
    auto& gen_weight   = nwt.get_gen_weight();
    auto& pu_weight    = nwt.get_pu_weight();
    auto& pdf_weight   = nwt.get_pdf_weight();
    auto& scale_weight = nwt.get_scale_weight();
    auto& ps_weight    = nwt.get_ps_weight();

    ot.userFloat(gen_weight.name) = gen_weight.w;
    for (uint iw = 0; iw < gen_weight.syst_name.size(); ++iw){
        auto n = gen_weight.syst_name.at(iw);
        ot.userFloat(n) = gen_weight.syst_val.at(iw);
    }

    ot.userFloat(pu_weight.name) = pu_weight.w;
    for (uint iw = 0; iw < pu_weight.syst_name.size(); ++iw){
        auto n = pu_weight.syst_name.at(iw);
        ot.userFloat(n) = pu_weight.syst_val.at(iw);
    }   

    ot.userFloat(pdf_weight.name) = pdf_weight.w;
    for (uint iw = 0; iw < pdf_weight.syst_name.size(); ++iw){
        auto n = pdf_weight.syst_name.at(iw);
        ot.userFloat(n) = pdf_weight.syst_val.at(iw);
    }

    ot.userFloat(scale_weight.name) = scale_weight.w;
    for (uint iw = 0; iw < scale_weight.syst_name.size(); ++iw){
        auto n = scale_weight.syst_name.at(iw);
        ot.userFloat(n) = scale_weight.syst_val.at(iw);
    }

    ot.userFloat(ps_weight.name) = ps_weight.w;
    for (uint iw = 0; iw < ps_weight.syst_name.size(); ++iw){
        auto n = ps_weight.syst_name.at(iw);
        ot.userFloat(n) = ps_weight.syst_val.at(iw);
    }
}
