#include "JetTools.h"
#include "GenJet.h"
#include "GenPart.h"
#include "Math/VectorUtil.h"

void JetTools::init_jec_shift(std::string JECFileName, std::string syst_name)
{
  jcp_ = std::unique_ptr<JetCorrectorParameters> (new JetCorrectorParameters(JECFileName, syst_name));
  jcu_ = std::unique_ptr<JetCorrectionUncertainty> (new JetCorrectionUncertainty(*jcp_));
}

void JetTools::init_smear(std::string JERScaleFactorFile, std::string JERResolutionFile, int random_seed)
{
  jetResolutionScaleFactor_ = std::unique_ptr<JME::JetResolutionScaleFactor> (new JME::JetResolutionScaleFactor (JERScaleFactorFile));
  jetResolution_            = std::unique_ptr<JME::JetResolution>            (new JME::JetResolution            (JERResolutionFile));
  rndm_generator_.SetSeed(random_seed);
}

std::vector<Jet> JetTools::jec_shift_jets(NanoAODTree& nat, const std::vector<Jet>& input_jets, bool direction_is_up)
{
  // calculation derived from the following twikis:
  // https://twiki.cern.ch/twiki/bin/view/CMS/JECUncertaintySources#Example_implementation
  // https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookJetEnergyCorrections#JetCorUncertainties

  // NOTE : the input jets must be unsmeared


  // https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_25/PhysicsTools/PatUtils/interface/ShiftedJetProducerT.h

  std::vector<Jet> result;
  result.reserve(input_jets.size());

  double shift = direction_is_up ? 1. : -1.;

  for(size_t ijet = 0; ijet < input_jets.size(); ++ijet)
    {
      jcu_->setJetPt  (input_jets.at(ijet).P4().Pt());
      jcu_->setJetEta (input_jets.at(ijet).P4().Eta());
      double corr_factor = jcu_->getUncertainty(direction_is_up);

      Jet jet = input_jets.at(ijet);
      double pt_i = jet.P4().Pt();
      jet.setP4(jet.P4() * (1 + shift * corr_factor) ); // set the shifted p4 ...

      // SUZANNE INVESTIGATING ONE-SIDED IMPACTS BY ARTIFICIALLY INJECTING A CORRECTION FACTOR TO SEE HOW THIS AFFECTS THE IMPACT PLOTS -- FIX ME LATER
      // jet.setP4(jet.P4() * (1 + shift * 0.5) ); // set the shifted p4 ...

      
      jet.buildP4Regressed(); // ... and reset the regressed p4 to be recomputed
      double pt_f = jet.P4().Pt();
      jet.set_jec_factor(1+shift*corr_factor);
      // std::cout << jet.get_jec_factor() << std::endl;
      result.emplace_back(jet);

    //  std::cout << "JetTools::jec_shift_jets : jet " << ijet << " : pt_i = " << pt_i << " : pt_f = " << pt_f << " : corr_factor = " << corr_factor << std::endl;
    }

  return result;    
}

std::vector<Jet> JetTools::smear_jets(NanoAODTree& nat, const std::vector<Jet>& input_jets, Variation jer_var, Variation breg_jer_var)
{
  JME::JetParameters jetParameters;
  jetParameters.setRho(*(nat.fixedGridRhoFastjetAll));
  int numberOfGenJets = *(nat.nGenJet);

  std::vector<Jet> smeared_jets = input_jets;

  for(auto& jet : smeared_jets){
    //same method of https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_25/PhysicsTools/PatUtils/interface/SmearedJetProducerT.h
    jetParameters.setJetEta(jet.P4().Eta());
    jetParameters.setJetPt(jet.P4().Pt());

    double tmpJER_ScaleFactor = jetResolutionScaleFactor_->getScaleFactor(jetParameters, jer_var);
    double tmpJER_Resolution  = jetResolution_->getResolution(jetParameters);

    int genJetId = get_property(jet,Jet_genJetIdx);

    //Get the unsmeared jetP4 (before any procedure)
    p4_t unsmeared_jetP4 = jet.P4();

    //JER smearfactor for normal jets
    double smearFactor;
    if(genJetId >= 0 && genJetId < numberOfGenJets) {  //generated jet was found and saved -> JER smearfactor for normal jets
      // https://cms-jerc.web.cern.ch/JER/
      // 1 + (s_JER - 1) * (pT - pT_gen) / pT
      smearFactor     = 1. + (tmpJER_ScaleFactor - 1.) * (jet.P4().Pt() - nat.GenJet_pt.At(genJetId))/jet.P4().Pt();
      // std::cout << "JetTools::smear_jets : genJetId = " << genJetId << ", smearFactor = " << smearFactor << std::endl;
    }
    else if(tmpJER_ScaleFactor > 1.) {
      double sigma     = tmpJER_Resolution * std::sqrt(tmpJER_ScaleFactor * tmpJER_ScaleFactor - 1);
      smearFactor     = 1. + rndm_generator_.Gaus(0., sigma);
      // std::cout << "JetTools::smear_jets : tmpJER_ScaleFactor = " << tmpJER_ScaleFactor << ", smearFactor = " << smearFactor << std::endl;
    }
    else{
      smearFactor = 1.;
      // std::cout << "JetTools::smear_jets : smearFactor = " << smearFactor << std::endl;
    }

    double MIN_JET_ENERGY = 1e-2;

    if (jet.P4().E() * smearFactor < MIN_JET_ENERGY) {
      smearFactor = MIN_JET_ENERGY / jet.P4().E();
    }
        
        //Make standard smearing to the jet
        jet.setP4(unsmeared_jetP4 * smearFactor);
        // std::cout << "JetTools::smear_jets : unsmeared_jet.P4.Pt() = " << unsmeared_jetP4.Pt() << std::endl;
        // std::cout << "JetTools::smear_jets : jet.P4().Pt() = " << jet.P4().Pt() << std::endl;

        //Procedure for b-regressed jets 
        //Step1: Check if genjet is found, then use the dedicated smearing and regression
        double bregcorr          = jet.getBregCorr();
        double smearedbreg_jetpt = unsmeared_jetP4.Pt()* bregcorr;
        double smearedbreg_jeten = unsmeared_jetP4.E() * bregcorr; 
        if(genJetId >= 0 && genJetId < numberOfGenJets) //generated jet was found and saved
        {
            //Get the genjet P4
            GenJet genjet = GenJet(genJetId, &nat);
            p4_t genjetP4 = genjet.P4();
            p4_t gennuP4 (0,0,0,0);
            //Compute the nearby neutrinos p4
            for (uint igp = 0; igp < *(nat.nGenPart); ++igp)
            {
                GenPart nu (igp, &nat);
                if (     get_property(nu, GenPart_status) == 1  && 
                    (abs(get_property(nu, GenPart_pdgId)) == 12 || 
                     abs(get_property(nu, GenPart_pdgId)) == 14 ||
                     abs(get_property(nu, GenPart_pdgId)) == 16) )
                {
                    if( ROOT::Math::VectorUtil::DeltaR(genjetP4, nu.P4()) < 0.4)
                        gennuP4 = gennuP4 + nu.P4();
                }
            }
            //Add the neutrinos to the genjet
            p4_t genjetwithnuP4 = genjetP4 + gennuP4;
            //Derive the new values of regressed/smeared pt and energy to build the dedicated regressed p4
            float resSmear;
            if (breg_jer_var      == Variation::NOMINAL)
                resSmear = 1.1;
            else if (breg_jer_var == Variation::UP)
                resSmear = 1.2;
                // resSmear = 1.8;
            else if (breg_jer_var == Variation::DOWN)
                resSmear = 1.0;
                // resSmear = 0.5;
            else
                throw std::runtime_error("JetTools::smear_jets : did not recognise b jet variation");

            double dpt         = smearedbreg_jetpt - genjetwithnuP4.Pt();
            smearedbreg_jetpt  = genjetwithnuP4.Pt() + resSmear*dpt;
            double den         = smearedbreg_jeten - genjetwithnuP4.E();
            smearedbreg_jeten  = genjetwithnuP4.E()  + resSmear*den;
            
	//Save the correct p4 for b-regressed jets
	ROOT::Math::PtEtaPhiEVector smearedbreg_jetP4_ptetaphie;
	smearedbreg_jetP4_ptetaphie.SetCoordinates (smearedbreg_jetpt, unsmeared_jetP4.Eta(), unsmeared_jetP4.Phi(), smearedbreg_jeten);
	p4_t smearedbreg_jetP4;
	smearedbreg_jetP4 = smearedbreg_jetP4_ptetaphie;
	jet.setP4Regressed(smearedbreg_jetP4);
      }
        
    else // Step2: Keep standard smearing and build standard P4Regressed with it
      {
	jet.buildP4Regressed();
      } 
  
    jet.set_smear_factor(smearFactor);
    jet.set_breg_factor(bregcorr);
  }

  return smeared_jets;
}
