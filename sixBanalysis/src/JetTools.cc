#include "JetTools.h"

// from CMSSW libraries
#include "JetMETCorrections/Modules/interface/JetResolution.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"

void JetTools::init_smear(std::string JERScaleFactorFile, std::string JERResolutionFile, int random_seed);
{
    jetResolutionScaleFactor_ = std::unique_ptr<JME::JetResolutionScaleFactor> (new JME::JetResolutionScaleFactor (JERScaleFactorFile));
    jetResolution_            = std::unique_ptr<JME::JetResolution>            (new JME::JetResolution            (JERResolutionFile));
    gRandom->SetSeed(random_seed);
}

std::vector<Jet> JetTools::smear_jets(NanoAODTree& nat, std::vector<Jet> input_jets, Variation variation)
{

    JME::JetParameters jetParameters;
    jetParameters.setRho(*(nat.fixedGridRhoFastjetAll));
    int numberOfGenJets = *(nat.nGenJet);

    for(auto &iJet : jets){
        //same method of https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_25/PhysicsTools/PatUtils/interface/SmearedJetProducerT.h
        jetParameters.setJetEta(iJet.P4().Eta());
        jetParameters.setJetPt(iJet.P4().Pt());

        float tmpJER_ScaleFactor = jetResolutionScaleFactor_->getScaleFactor(jetParameters, variation  );
        float tmpJER_Resolution  = jetResolution_->getResolution(jetParameters);

        int genJetId = get_property(iJet,Jet_genJetIdx); //Before was bugged, int genJetId = abs(get_property(iJet,Jet_genJetIdx));

        //Get the unsmeared jetP4 (before any procedure)
        p4_t unsmeared_jetP4 = iJet.P4();

        //JER smearfactor for normal jets
        float smearFactor;
        if(genJetId>=0 && genJetId < numberOfGenJets) //generated jet was found and saved
        {
            //JER smearfactor for normal jets
            smearFactor     = 1. + (tmpJER_ScaleFactor - 1.) * (iJet.P4().Pt() - nat.GenJet_pt.At(genJetId))/iJet.P4().Pt();
        }
        else if(tmpJER_ScaleFactor > 1.)
        {
            float sigma     = tmpJER_Resolution * std::sqrt(tmpJER_ScaleFactor * tmpJER_ScaleFactor - 1);
            smearFactor     = 1. + gRandom->Gaus(0., sigma);
        }
        else
        {
            smearFactor = 1.;
        }

        float MIN_JET_ENERGY = 1e-2;

        if (iJet.P4().Energy() * smearFactor < MIN_JET_ENERGY)
        {
            smearFactor = MIN_JET_ENERGY / iJet.P4().Energy();
        }
        
        //Make standard smearing to the jet
        iJet.setP4(unsmeared_jetP4 * smearFactor);

        //Procedure for b-regressed jets 
        //Step1: Check if genjet is found, then use the dedicated smearing and regression
        float bregcorr          = Get_bRegCorr(iJet);
        float smearedbreg_jetpt = unsmeared_jetP4.Pt()*bregcorr;
        float smearedbreg_jeten = unsmeared_jetP4.E()*bregcorr; 
        if(genJetId >= 0 && genJetId < numberOfGenJets) //generated jet was found and saved
        {
            //Get the genjet P4
            GenJet genjet           = GenJet(genJetId, &nat);
            p4_t genjetP4 = genjet.P4();
            p4_t gennuP4, genjetwithnuP4;
            //Compute the nearby neutrinos p4
            for (uint igp = 0; igp < *(nat.nGenPart); ++igp)
            {
                GenPart nu (igp, &nat);
                if (     get_property(nu, GenPart_status) == 1  && 
                    (abs(get_property(nu, GenPart_pdgId)) == 12 || 
                     abs(get_property(nu, GenPart_pdgId)) == 14 ||
                     abs(get_property(nu, GenPart_pdgId)) == 16) )
                {
                    if( genjetP4.DeltaR( nu.P4() ) < 0.4) gennuP4 = gennuP4 + nu.P4();
                }
            }
            //Add the neutrinos to the genjet
            genjetwithnuP4 = genjetP4 + gennuP4;
            //Derive the new values of regressed/smeared pt and energy to build the dedicated regressed p4
            float resSmear = 1.1; //recommended nominal scale factor //TODO:Add the variations of this scale factor
            float dpt          = smearedbreg_jetpt - genjetwithnuP4.Pt();
            smearedbreg_jetpt  = genjetwithnuP4.Pt() + resSmear*dpt;
            float den          = smearedbreg_jeten - genjetwithnuP4.E();
            smearedbreg_jeten  = genjetwithnuP4.E()  + resSmear*den;
            //Save the correct p4 for b-regressed jets
            p4_t smearedbreg_jetP4;
            smearedbreg_jetP4.SetPtEtaPhiE(smearedbreg_jetpt, unsmeared_jetP4.Eta(), unsmeared_jetP4.Phi(), smearedbreg_jeten);
            iJet.setP4Regressed(smearedbreg_jetP4);    
        }
        
        else // Step2: Keep standard smearing and build standard P4Regressed with it
        {
           iJet.buildP4Regressed();
        } 
  
    }

    return jets;
}