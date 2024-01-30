/**
 ** class  : NanoAODTree_ReaderImpl
 ** author : L. Cadamuro (UF)
 ** date   : 27/12/2017
 ** brief  : interface to the Nano AOD Event ntuple. It contains the TTreeReader and the single branch readers.
 **        : comment out the branches you are not interested in to speed up
 **        :
 **        : NOTE: this is the implementation that uses the TTreeReader to run
 **        : Unfortunately a ROOT bug causes it to go segfault when some branches are not read
 **/

#ifndef NANOAODTREE_READERIMPL_H
#define NANOAODTREE_READERIMPL_H

#include "TROOT.h"
#include "TChain.h"
#include "TFile.h"
#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include "TTreeReaderArray.h"
#include "TriggerReader_ReaderImpl.h"
#include "NanoReaderValue.h"
#include "NanoReaderArray.h"

#include <vector>
#include <iostream>
#include <memory>

// #define ENABLE_JET      true
// #define ENABLE_FATJET   true
// #define ENABLE_ELECTRON true
// #define ENABLE_CaloMET  true

class NanoAODTree_ReaderImpl {
public:
    
  // methods
  NanoAODTree_ReaderImpl(TChain* chain) :
    fReader(chain)        ,
    trg_reader_(&fReader) ,
    old_tree_nr_(-1)      ,
    proc_first_ev_(false)
  {};
        
  ~NanoAODTree_ReaderImpl(){};

  TriggerReader_ReaderImpl& triggerReader(){return trg_reader_;}

  // bool Next() {return fReader.Next();}
  bool Next();
  bool getTrgOr() {return trg_reader_.getTrgOr();};
  bool getTrgResult(std::string path){return trg_reader_.getTrgResult(path); };
  std::vector<std::string> getTrgPassed() {return trg_reader_.getTrgPassed();};
  
  // the chain and TTreeReader
  TTreeReader   fReader;

  // the trigger reader - a special care is needed for branches that can disappear
  TriggerReader_ReaderImpl trg_reader_;

  // the count of the current ttree number, to verify at Next()
  int old_tree_nr_;
  bool proc_first_ev_;

  //XYH nat class
  template<class T> 
  void attachCustomValueBranch(const std::string& branchName, bool returnDefault = false, const T& defaultValue = T())
  {
    fCustomBranchMap.emplace(branchName, std::make_unique<NanoReaderValue<T>>(fReader, branchName.data()));
    static_cast<NanoReaderValue<T>*>(fCustomBranchMap[branchName].get())->SetReturnDefault(returnDefault, defaultValue);
  }

  template<class T> 
  std::vector<std::string> attachAllMatchingBranch(const std::string branchNameTemplate, bool returnDefault = false, const T& defaultValue = T())
  {
    TObjArray* theBranchList = fReader.GetTree()->GetListOfBranches();
    std::vector<std::string> listOfBranchNames;
    for(const auto & branch : *theBranchList)
      {
	std::string branchName = branch->GetName();
	
	//std::cout << "branchName = "<<branchName<<std::endl;
	if(branchName.find(branchNameTemplate) != std::string::npos)
	  {
	    attachCustomValueBranch<T>(branchName,returnDefault, defaultValue);
	    listOfBranchNames.emplace_back(branchName);
	  }
      }
    return listOfBranchNames;
  }

  template<class T> 
  T readCustomValueBranch(const std::string branchName)
  {
    if(static_cast<NanoReaderValue<T>*>(fCustomBranchMap.at(branchName).get()) == nullptr) std::cout<<"Merda"<<std::endl;
    return *static_cast<NanoReaderValue<T>*>(fCustomBranchMap.at(branchName).get())->Get();
  }        

  std::map<std::string, std::unique_ptr<NanoReaderValueBase>> fCustomBranchMap;

  // tree readers
  NanoReaderValue<UInt_t>    run                                  {fReader, "run"};
  NanoReaderValue<UInt_t>    luminosityBlock                      {fReader, "luminosityBlock"};
  NanoReaderValue<ULong64_t> event                                {fReader, "event"};
        
  NanoReaderValue<Float_t>   CaloMET_phi                          {fReader, "CaloMET_phi"};
  NanoReaderValue<Float_t>   CaloMET_pt                           {fReader, "CaloMET_pt"};
  NanoReaderValue<Float_t>   CaloMET_sumEt                        {fReader, "CaloMET_sumEt"};

  NanoReaderValue<UInt_t>    nElectron                            {fReader, "nElectron"};
  NanoReaderArray<Float_t>   Electron_deltaEtaSC                  {fReader, "Electron_deltaEtaSC"};
  NanoReaderArray<Float_t>   Electron_dr03EcalRecHitSumEt         {fReader, "Electron_dr03EcalRecHitSumEt"};
  NanoReaderArray<Float_t>   Electron_dr03HcalDepth1TowerSumEt    {fReader, "Electron_dr03HcalDepth1TowerSumEt"};
  NanoReaderArray<Float_t>   Electron_dr03TkSumPt                 {fReader, "Electron_dr03TkSumPt"};
  NanoReaderArray<Float_t>   Electron_dxy                         {fReader, "Electron_dxy"};
  NanoReaderArray<Float_t>   Electron_dxyErr                      {fReader, "Electron_dxyErr"};
  NanoReaderArray<Float_t>   Electron_dz                          {fReader, "Electron_dz"};
  NanoReaderArray<Float_t>   Electron_dzErr                       {fReader, "Electron_dzErr"};
  NanoReaderArray<Float_t>   Electron_eCorr                       {fReader, "Electron_eCorr"};
  NanoReaderArray<Float_t>   Electron_eInvMinusPInv               {fReader, "Electron_eInvMinusPInv"};
  NanoReaderArray<Float_t>   Electron_energyErr                   {fReader, "Electron_energyErr"};
  NanoReaderArray<Float_t>   Electron_eta                         {fReader, "Electron_eta"};
  NanoReaderArray<Float_t>   Electron_hoe                         {fReader, "Electron_hoe"};
  NanoReaderArray<Float_t>   Electron_ip3d                        {fReader, "Electron_ip3d"};
  NanoReaderArray<Float_t>   Electron_mass                        {fReader, "Electron_mass"};
  NanoReaderArray<Float_t>   Electron_miniPFRelIso_all            {fReader, "Electron_miniPFRelIso_all"};
  NanoReaderArray<Float_t>   Electron_miniPFRelIso_chg            {fReader, "Electron_miniPFRelIso_chg"};
  NanoReaderArray<Float_t>   Electron_mvaSpring16GP               {fReader, "Electron_mvaSpring16GP"};
  NanoReaderArray<Float_t>   Electron_mvaSpring16HZZ              {fReader, "Electron_mvaSpring16HZZ"};
  NanoReaderArray<Float_t>   Electron_pfRelIso03_all              {fReader, "Electron_pfRelIso03_all"};
  NanoReaderArray<Float_t>   Electron_pfRelIso03_chg              {fReader, "Electron_pfRelIso03_chg"};
  NanoReaderArray<Float_t>   Electron_phi                         {fReader, "Electron_phi"};
  NanoReaderArray<Float_t>   Electron_pt                          {fReader, "Electron_pt"};
  NanoReaderArray<Float_t>   Electron_r9                          {fReader, "Electron_r9"};
  NanoReaderArray<Float_t>   Electron_sieie                       {fReader, "Electron_sieie"};
  NanoReaderArray<Float_t>   Electron_sip3d                       {fReader, "Electron_sip3d"};
  NanoReaderArray<Float_t>   Electron_mvaTTH                      {fReader, "Electron_mvaTTH"};
  NanoReaderArray<Int_t>     Electron_charge                      {fReader, "Electron_charge"};
  NanoReaderArray<Int_t>     Electron_cutBased                    {fReader, "Electron_cutBased"};
  NanoReaderArray<Int_t>     Electron_cutBased_HLTPreSel          {fReader, "Electron_cutBased_HLTPreSel"};
  NanoReaderArray<Int_t>     Electron_jetIdx                      {fReader, "Electron_jetIdx"};
  NanoReaderArray<Int_t>     Electron_pdgId                       {fReader, "Electron_pdgId"};
  NanoReaderArray<Int_t>     Electron_photonIdx                   {fReader, "Electron_photonIdx"};
  NanoReaderArray<Int_t>     Electron_tightCharge                 {fReader, "Electron_tightCharge"};
  NanoReaderArray<Int_t>     Electron_vidNestedWPBitmap           {fReader, "Electron_vidNestedWPBitmap"};
  NanoReaderArray<Bool_t>    Electron_convVeto                    {fReader, "Electron_convVeto"};
  NanoReaderArray<Bool_t>    Electron_cutBased_HEEP               {fReader, "Electron_cutBased_HEEP"};
  NanoReaderArray<Bool_t>    Electron_isPFcand                    {fReader, "Electron_isPFcand"};
  NanoReaderArray<UChar_t>   Electron_lostHits                    {fReader, "Electron_lostHits"};
  NanoReaderArray<Bool_t>    Electron_mvaSpring16GP_WP80          {fReader, "Electron_mvaSpring16GP_WP80"};
  NanoReaderArray<Bool_t>    Electron_mvaSpring16GP_WP90          {fReader, "Electron_mvaSpring16GP_WP90"};
  NanoReaderArray<Bool_t>    Electron_mvaSpring16HZZ_WPL          {fReader, "Electron_mvaSpring16HZZ_WPL"};
  NanoReaderArray<Bool_t>    Electron_mvaFall17V2Iso_WPL          {fReader, "Electron_mvaFall17V2Iso_WPL"};
  NanoReaderArray<Bool_t>    Electron_mvaFall17V2Iso_WP90         {fReader, "Electron_mvaFall17V2Iso_WP90"};
  NanoReaderArray<Bool_t>    Electron_mvaFall17V2Iso_WP80         {fReader, "Electron_mvaFall17V2Iso_WP80"};
  
  // Run-3 samples
  NanoReaderArray<Bool_t> Electron_mvaIso_WP80                 {fReader, "Electron_mvaIso_WP80"};
  NanoReaderArray<Bool_t> Electron_mvaIso_WP90                 {fReader, "Electron_mvaIso_WP90"};
  NanoReaderArray<Bool_t> Electron_mvaIso_WPL                  {fReader, "Electron_mvaIso_WPL"};
  
  // NanoReaderArray<Int_t>     Electron_genPartIdx                  {fReader, "Electron_genPartIdx"};
  // NanoReaderArray<UChar_t>   Electron_genPartFlav                 {fReader, "Electron_genPartFlav"};
  NanoReaderArray<Int_t>     Electron_genPartIdx                   {fReader, "Electron_genPartIdx"};
  NanoReaderArray<UChar_t>   Electron_genPartFlav                  {fReader, "Electron_genPartFlav"};

  NanoReaderArray<UChar_t>   Electron_cleanmask                   {fReader, "Electron_cleanmask"};

  // MET Filters
  NanoReaderValue<Bool_t> Flag_goodVertices                       {fReader, "Flag_goodVertices"}; // primary vertex filter
  NanoReaderValue<Bool_t> Flag_globalSuperTightHalo2016Filter     {fReader, "Flag_globalSuperTightHalo2016Filter"}; // beam halo filter
  NanoReaderValue<Bool_t> Flag_HBHENoiseFilter                    {fReader, "Flag_HBHENoiseFilter"}; // HBHE noise filter
  NanoReaderValue<Bool_t> Flag_HBHENoiseIsoFilter                 {fReader, "Flag_HBHENoiseIsoFilter"}; // HBHEiso noise filter
  NanoReaderValue<Bool_t> Flag_EcalDeadCellTriggerPrimitiveFilter {fReader, "Flag_EcalDeadCellTriggerPrimitiveFilter"}; // ECAL TP filter
  NanoReaderValue<Bool_t> Flag_BadPFMuonFilter                    {fReader, "Flag_BadPFMuonFilter"}; // Bad PF Muon Filter
  NanoReaderValue<Bool_t> Flag_eeBadScFilter                      {fReader, "Flag_eeBadScFilter"}; // ee badSC noise filter
  NanoReaderValue<Bool_t> Flag_ecalBadCalibFilter                 {fReader, "Flag_ecalBadCalibFilter"}; // ECAL bad calibration filter update (not for 2016)

  // Triggers
  NanoReaderValue<Bool_t> HLT_IsoMu24 {fReader, "HLT_IsoMu24"};
  NanoReaderValue<Bool_t> L1_QuadJet60er2p5{fReader, "L1_QuadJet60er2p5"};
  NanoReaderValue<Bool_t> L1_HTT280er{fReader, "L1_HTT280er"};
  NanoReaderValue<Bool_t> L1_HTT320er{fReader, "L1_HTT320er"};
  NanoReaderValue<Bool_t> L1_HTT360er{fReader, "L1_HTT360er"};
  NanoReaderValue<Bool_t> L1_HTT400er{fReader, "L1_HTT400er"};
  NanoReaderValue<Bool_t> L1_HTT450er{fReader, "L1_HTT450er"};
  NanoReaderValue<Bool_t> L1_HTT280er_QuadJet_70_55_40_35_er2p5{fReader, "L1_HTT280er_QuadJet_70_55_40_35_er2p5"};
  NanoReaderValue<Bool_t> L1_HTT320er_QuadJet_70_55_40_40_er2p5{fReader, "L1_HTT320er_QuadJet_70_55_40_40_er2p5"};
  NanoReaderValue<Bool_t> L1_HTT320er_QuadJet_80_60_er2p1_45_40_er2p3{fReader, "L1_HTT320er_QuadJet_80_60_er2p1_45_40_er2p3"};
  NanoReaderValue<Bool_t> L1_HTT320er_QuadJet_80_60_er2p1_50_45_er2p3{fReader, "L1_HTT320er_QuadJet_80_60_er2p1_50_45_er2p3"};
  NanoReaderValue<Bool_t> L1_Mu6_HTT240er{fReader, "L1_Mu6_HTT240er"};
  
  NanoReaderValue<UInt_t>    nFatJet                              {fReader, "nFatJet"};
  NanoReaderArray<Float_t>   FatJet_area                          {fReader, "FatJet_area"};
  NanoReaderArray<Float_t>   FatJet_pt                            {fReader, "FatJet_pt"};
  NanoReaderArray<Float_t>   FatJet_eta                           {fReader, "FatJet_eta"};
  NanoReaderArray<Float_t>   FatJet_mass                          {fReader, "FatJet_mass"};
  NanoReaderArray<Float_t>   FatJet_msoftdrop                     {fReader, "FatJet_msoftdrop"};
  NanoReaderArray<Float_t>   FatJet_n2b1                          {fReader, "FatJet_n2b1"};
  NanoReaderArray<Float_t>   FatJet_n3b1                          {fReader, "FatJet_n3b1"};
  NanoReaderArray<Float_t>   FatJet_phi                           {fReader, "FatJet_phi"};
  NanoReaderArray<Float_t>   FatJet_rawFactor                     {fReader, "FatJet_rawFactor"};
  NanoReaderArray<Int_t>     FatJet_jetId                         {fReader, "FatJet_jetId"};  
  NanoReaderArray<Float_t>   FatJet_tau1                          {fReader, "FatJet_tau1"};
  NanoReaderArray<Float_t>   FatJet_tau2                          {fReader, "FatJet_tau2"};
  NanoReaderArray<Float_t>   FatJet_tau3                          {fReader, "FatJet_tau3"};
  NanoReaderArray<Float_t>   FatJet_tau4                          {fReader, "FatJet_tau4"};
  NanoReaderArray<Int_t>     FatJet_subJetIdx1                    {fReader, "FatJet_subJetIdx1"};
  NanoReaderArray<Int_t>     FatJet_subJetIdx2                    {fReader, "FatJet_subJetIdx2"};
  NanoReaderArray<Int_t>     FatJet_genJetAK8Idx                  {fReader, "FatJet_genJetAK8Idx"};
  NanoReaderArray<Int_t>     FatJet_hadronFlavour                 {fReader, "FatJet_hadronFlavour"};
  NanoReaderArray<UChar_t>   FatJet_nBHadrons                     {fReader, "FatJet_nBHadrons"};
  NanoReaderArray<UChar_t>   FatJet_nCHadrons                     {fReader, "FatJet_nCHadrons"};
  NanoReaderArray<Int_t>     FatJet_nPFCand                       {fReader, "FatJet_nPFCand"};
  NanoReaderArray<Float_t>   FatJet_ParticleNetMD_probQCDb        {fReader, "FatJet_ParticleNetMD_probQCDb"};
  NanoReaderArray<Float_t>   FatJet_ParticleNetMD_probQCDbb       {fReader, "FatJet_ParticleNetMD_probQCDbb"};
  NanoReaderArray<Float_t>   FatJet_ParticleNetMD_probQCDc        {fReader, "FatJet_ParticleNetMD_probQCDc"};
  NanoReaderArray<Float_t>   FatJet_ParticleNetMD_probQCDcc       {fReader, "FatJet_ParticleNetMD_probQCDcc"};
  NanoReaderArray<Float_t>   FatJet_ParticleNetMD_probQCDothers   {fReader, "FatJet_ParticleNetMD_probQCDothers"};
  NanoReaderArray<Float_t>   FatJet_ParticleNetMD_probXbb         {fReader, "FatJet_ParticleNetMD_probXbb"};
  NanoReaderArray<Float_t>   FatJet_ParticleNetMD_probXcc         {fReader, "FatJet_ParticleNetMD_probXcc"};
  NanoReaderArray<Float_t>   FatJet_ParticleNetMD_probXqq         {fReader, "FatJet_ParticleNetMD_probXqq"};
  NanoReaderArray<Float_t>   FatJet_deepTagMD_H4qvsQCD            {fReader, "FatJet_deepTagMD_H4qvsQCD"};
  NanoReaderArray<Float_t>   FatJet_deepTagMD_HbbvsQCD            {fReader, "FatJet_deepTagMD_HbbvsQCD"};
  NanoReaderArray<Float_t>   FatJet_deepTagMD_TvsQCD              {fReader, "FatJet_deepTagMD_TvsQCD"};
  NanoReaderArray<Float_t>   FatJet_deepTagMD_WvsQCD              {fReader, "FatJet_deepTagMD_WvsQCD"};
  NanoReaderArray<Float_t>   FatJet_deepTagMD_ZvsQCD              {fReader, "FatJet_deepTagMD_ZvsQCD"};
  NanoReaderArray<Float_t>   FatJet_deepTagMD_bbvsLight           {fReader, "FatJet_deepTagMD_bbvsLight"};
  NanoReaderArray<Float_t>   FatJet_deepTagMD_ccvsLight           {fReader, "FatJet_deepTagMD_ccvsLight"};
  NanoReaderArray<Float_t>   FatJet_deepTag_QCD                   {fReader, "FatJet_deepTag_QCD"};
  NanoReaderArray<Float_t>   FatJet_deepTag_QCDothers             {fReader, "FatJet_deepTag_QCDothers"};
  NanoReaderArray<Float_t>   FatJet_deepTag_WvsQCD                {fReader, "FatJet_deepTag_WvsQCD"};
  NanoReaderArray<Float_t>   FatJet_deepTag_ZvsQCD                {fReader, "FatJet_deepTag_ZvsQCD"};
  NanoReaderArray<Float_t>   FatJet_btagCMVA                      {fReader, "FatJet_btagCMVA"};
  NanoReaderArray<Float_t>   FatJet_btagCSVV2                     {fReader, "FatJet_btagCSVV2"};
  NanoReaderArray<Float_t>   FatJet_btagDeepB                     {fReader, "FatJet_btagDeepB"};
  NanoReaderArray<Float_t>   FatJet_btagHbb                       {fReader, "FatJet_btagHbb"};
    
  NanoReaderValue<UInt_t>    nGenJetAK8                           {fReader, "nGenJetAK8"};
  NanoReaderArray<Float_t>   GenJetAK8_eta                        {fReader, "GenJetAK8_eta"};
  NanoReaderArray<Float_t>   GenJetAK8_mass                       {fReader, "GenJetAK8_mass"};
  NanoReaderArray<Float_t>   GenJetAK8_phi                        {fReader, "GenJetAK8_phi"};
  NanoReaderArray<Float_t>   GenJetAK8_pt                         {fReader, "GenJetAK8_pt"};
  
  NanoReaderValue<UInt_t>    nGenJet                              {fReader, "nGenJet"};
  NanoReaderArray<Float_t>   GenJet_eta                           {fReader, "GenJet_eta"};
  NanoReaderArray<Float_t>   GenJet_mass                          {fReader, "GenJet_mass"};
  NanoReaderArray<Float_t>   GenJet_phi                           {fReader, "GenJet_phi"};
  NanoReaderArray<Float_t>   GenJet_pt                            {fReader, "GenJet_pt"};
        
  NanoReaderValue<UInt_t>    nGenPart                             {fReader, "nGenPart"};
  NanoReaderArray<Float_t>   GenPart_eta                          {fReader, "GenPart_eta"};
  NanoReaderArray<Float_t>   GenPart_mass                         {fReader, "GenPart_mass"};
  NanoReaderArray<Float_t>   GenPart_phi                          {fReader, "GenPart_phi"};
  NanoReaderArray<Float_t>   GenPart_pt                           {fReader, "GenPart_pt"};
  NanoReaderArray<Int_t>     GenPart_genPartIdxMother             {fReader, "GenPart_genPartIdxMother"};
  NanoReaderArray<Int_t>     GenPart_pdgId                        {fReader, "GenPart_pdgId"};
  NanoReaderArray<Int_t>     GenPart_status                       {fReader, "GenPart_status"};
  NanoReaderArray<Int_t>     GenPart_statusFlags                  {fReader, "GenPart_statusFlags"};
        
  NanoReaderValue<Float_t>   Generator_x1                         {fReader, "Generator_x1"};
  NanoReaderValue<Float_t>   Generator_x2                         {fReader, "Generator_x2"};
        
  NanoReaderValue<UInt_t>    nGenVisTau                           {fReader, "nGenVisTau"};
  NanoReaderArray<Float_t>   GenVisTau_eta                        {fReader, "GenVisTau_eta"};
  NanoReaderArray<Float_t>   GenVisTau_mass                       {fReader, "GenVisTau_mass"};
  NanoReaderArray<Float_t>   GenVisTau_phi                        {fReader, "GenVisTau_phi"};
  NanoReaderArray<Float_t>   GenVisTau_pt                         {fReader, "GenVisTau_pt"};
  NanoReaderArray<Int_t>     GenVisTau_charge                     {fReader, "GenVisTau_charge"};
  NanoReaderArray<Int_t>     GenVisTau_genPartIdxMother           {fReader, "GenVisTau_genPartIdxMother"};
  NanoReaderArray<Int_t>     GenVisTau_status                     {fReader, "GenVisTau_status"};
        
  NanoReaderValue<Float_t>   genWeight                            {fReader, "genWeight"};
  NanoReaderValue<Float_t>   LHEWeight_originalXWGTUP             {fReader, "LHEWeight_originalXWGTUP"};
  NanoReaderValue<UInt_t>    nLHEPdfWeight                        {fReader, "nLHEPdfWeight"};
  NanoReaderArray<Float_t>   LHEPdfWeight                         {fReader, "LHEPdfWeight"};
  NanoReaderValue<UInt_t>    nLHEScaleWeight                      {fReader, "nLHEScaleWeight"};
  NanoReaderArray<Float_t>   LHEScaleWeight                       {fReader, "LHEScaleWeight"};
  NanoReaderValue<UInt_t>    nPSWeight                            {fReader, "nPSWeight"};
  NanoReaderArray<Float_t>   PSWeight                             {fReader, "PSWeight"};
        
  NanoReaderValue<UInt_t>    nJet                                 {fReader, "nJet"};
  NanoReaderArray<Float_t>   Jet_area                             {fReader, "Jet_area"};
  NanoReaderArray<Float_t>   Jet_btagCMVA                         {fReader, "Jet_btagCMVA"};
  NanoReaderArray<Float_t>   Jet_btagCSVV2                        {fReader, "Jet_btagCSVV2"};
  NanoReaderArray<Float_t>   Jet_btagDeepB                        {fReader, "Jet_btagDeepB"};
  NanoReaderArray<Float_t>   Jet_btagDeepC                        {fReader, "Jet_btagDeepC"};
  NanoReaderArray<Float_t>   Jet_btagDeepFlavB                    {fReader, "Jet_btagDeepFlavB"};
  NanoReaderArray<Float_t>   Jet_btagPNetBvsAll                   {fReader, "Jet_btagPNetBvsAll"};
  NanoReaderArray<Float_t>   Jet_btagDeepFlavC                    {fReader, "Jet_btagDeepFlavC"};
  NanoReaderArray<Float_t>   Jet_chEmEF                           {fReader, "Jet_chEmEF"};
  NanoReaderArray<Float_t>   Jet_chHEF                            {fReader, "Jet_chHEF"};
  NanoReaderArray<Float_t>   Jet_eta                              {fReader, "Jet_eta"};
  NanoReaderArray<Float_t>   Jet_mass                             {fReader, "Jet_mass"};
  NanoReaderArray<Float_t>   Jet_neEmEF                           {fReader, "Jet_neEmEF"};
  NanoReaderArray<Float_t>   Jet_neHEF                            {fReader, "Jet_neHEF"};
  NanoReaderArray<Float_t>   Jet_phi                              {fReader, "Jet_phi"};
  NanoReaderArray<Float_t>   Jet_pt                               {fReader, "Jet_pt"};
  NanoReaderArray<Float_t>   Jet_qgl                              {fReader, "Jet_qgl"};
  NanoReaderArray<Float_t>   Jet_rawFactor                        {fReader, "Jet_rawFactor"};
  NanoReaderArray<Float_t>   Jet_bRegCorr                         {fReader, "Jet_bRegCorr"};
  NanoReaderArray<Float_t>   Jet_bRegRes                          {fReader, "Jet_bRegRes"};        
  NanoReaderArray<Int_t>     Jet_electronIdx1                     {fReader, "Jet_electronIdx1"};
  NanoReaderArray<Int_t>     Jet_electronIdx2                     {fReader, "Jet_electronIdx2"};
  NanoReaderArray<Int_t>     Jet_jetId                            {fReader, "Jet_jetId"};
  NanoReaderArray<Int_t>     Jet_muonIdx1                         {fReader, "Jet_muonIdx1"};
  NanoReaderArray<Int_t>     Jet_muonIdx2                         {fReader, "Jet_muonIdx2"};
  NanoReaderArray<Int_t>     Jet_nConstituents                    {fReader, "Jet_nConstituents"};
  NanoReaderArray<Int_t>     Jet_nElectrons                       {fReader, "Jet_nElectrons"};
  NanoReaderArray<Int_t>     Jet_nMuons                           {fReader, "Jet_nMuons"};
  NanoReaderArray<Int_t>     Jet_puId                             {fReader, "Jet_puId"};

  NanoReaderArray<Int_t>     Jet_genJetIdx                         {fReader, "Jet_genJetIdx"};
  NanoReaderArray<Int_t>     Jet_hadronFlavour                     {fReader, "Jet_hadronFlavour"};
  NanoReaderArray<Int_t>     Jet_partonFlavour                     {fReader, "Jet_partonFlavour"};

  NanoReaderValue<Float_t>   LHE_HT                                {fReader, "LHE_HT"};
  NanoReaderValue<Float_t>   LHE_HTIncoming                        {fReader, "LHE_HTIncoming"};
  NanoReaderValue<Float_t>   LHE_Vpt                               {fReader, "LHE_Vpt"};
  NanoReaderValue<UChar_t>   LHE_Njets                             {fReader, "LHE_Njets"};
  NanoReaderValue<UChar_t>   LHE_Nb                                {fReader, "LHE_Nb"};
  NanoReaderValue<UChar_t>   LHE_Nc                                {fReader, "LHE_Nc"};
  NanoReaderValue<UChar_t>   LHE_Nuds                              {fReader, "LHE_Nuds"};
  NanoReaderValue<UChar_t>   LHE_Nglu                              {fReader, "LHE_Nglu"};
  NanoReaderValue<UChar_t>   LHE_NpNLO                             {fReader, "LHE_NpNLO"};
  NanoReaderValue<UChar_t>   LHE_NpLO                              {fReader, "LHE_NpLO"};

  NanoReaderValue<Float_t>   L1PreFiringWeight_Nom                 {fReader, "L1PreFiringWeight_Nom"};
  NanoReaderValue<Float_t>   L1PreFiringWeight_Up                  {fReader, "L1PreFiringWeight_Up"};
  NanoReaderValue<Float_t>   L1PreFiringWeight_Dn                  {fReader, "L1PreFiringWeight_Dn"};
        
  NanoReaderValue<Float_t>   GenMET_phi                           {fReader, "GenMET_phi"};
  NanoReaderValue<Float_t>   GenMET_pt                            {fReader, "GenMET_pt"};
  NanoReaderValue<Float_t>   MET_MetUnclustEnUpDeltaX             {fReader, "MET_MetUnclustEnUpDeltaX"};
  NanoReaderValue<Float_t>   MET_MetUnclustEnUpDeltaY             {fReader, "MET_MetUnclustEnUpDeltaY"};
  NanoReaderValue<Float_t>   MET_covXX                            {fReader, "MET_covXX"};
  NanoReaderValue<Float_t>   MET_covXY                            {fReader, "MET_covXY"};
  NanoReaderValue<Float_t>   MET_covYY                            {fReader, "MET_covYY"};
  NanoReaderValue<Float_t>   MET_phi                              {fReader, "MET_phi"};
  NanoReaderValue<Float_t>   MET_pt                               {fReader, "MET_pt"};
  NanoReaderValue<Float_t>   MET_significance                     {fReader, "MET_significance"};
  NanoReaderValue<Float_t>   MET_sumEt                            {fReader, "MET_sumEt"};

  NanoReaderValue<Float_t>   PuppiMET_phi                         {fReader, "PuppiMET_phi"};
  NanoReaderValue<Float_t>   PuppiMET_pt                          {fReader, "PuppiMET_pt"};
  NanoReaderValue<Float_t>   PuppiMET_sumEt                       {fReader, "PuppiMET_sumEt"};
        
  NanoReaderValue<Float_t>   RawMET_phi                           {fReader, "RawMET_phi"};
  NanoReaderValue<Float_t>   RawMET_pt                            {fReader, "RawMET_pt"};
  NanoReaderValue<Float_t>   RawMET_sumEt                         {fReader, "RawMET_sumEt"};
        
  NanoReaderValue<Float_t>   TkMET_phi                            {fReader, "TkMET_phi"};
  NanoReaderValue<Float_t>   TkMET_pt                             {fReader, "TkMET_pt"};
  NanoReaderValue<Float_t>   TkMET_sumEt                          {fReader, "TkMET_sumEt"};

        
  NanoReaderValue<UInt_t>    nMuon                                {fReader, "nMuon"};
  NanoReaderArray<Float_t>   Muon_dxy                             {fReader, "Muon_dxy"};
  NanoReaderArray<Float_t>   Muon_dxyErr                          {fReader, "Muon_dxyErr"};
  NanoReaderArray<Float_t>   Muon_dz                              {fReader, "Muon_dz"};
  NanoReaderArray<Float_t>   Muon_dzErr                           {fReader, "Muon_dzErr"};
  NanoReaderArray<Float_t>   Muon_eta                             {fReader, "Muon_eta"};
  NanoReaderArray<Float_t>   Muon_ip3d                            {fReader, "Muon_ip3d"};
  NanoReaderArray<Float_t>   Muon_mass                            {fReader, "Muon_mass"};
  NanoReaderArray<Float_t>   Muon_miniPFRelIso_all                {fReader, "Muon_miniPFRelIso_all"};
  NanoReaderArray<Float_t>   Muon_miniPFRelIso_chg                {fReader, "Muon_miniPFRelIso_chg"};
  NanoReaderArray<Float_t>   Muon_pfRelIso03_all                  {fReader, "Muon_pfRelIso03_all"};
  NanoReaderArray<Float_t>   Muon_pfRelIso03_chg                  {fReader, "Muon_pfRelIso03_chg"};
  NanoReaderArray<Float_t>   Muon_pfRelIso04_all                  {fReader, "Muon_pfRelIso04_all"};
  NanoReaderArray<Float_t>   Muon_phi                             {fReader, "Muon_phi"};
  NanoReaderArray<Float_t>   Muon_pt                              {fReader, "Muon_pt"};
  NanoReaderArray<Float_t>   Muon_ptErr                           {fReader, "Muon_ptErr"};
  NanoReaderArray<Float_t>   Muon_segmentComp                     {fReader, "Muon_segmentComp"};
  NanoReaderArray<Float_t>   Muon_sip3d                           {fReader, "Muon_sip3d"};
  NanoReaderArray<Float_t>   Muon_mvaTTH                          {fReader, "Muon_mvaTTH"};
  NanoReaderArray<Int_t>     Muon_charge                          {fReader, "Muon_charge"};
  NanoReaderArray<Int_t>     Muon_jetIdx                          {fReader, "Muon_jetIdx"};
  NanoReaderArray<Int_t>     Muon_nStations                       {fReader, "Muon_nStations"};
  NanoReaderArray<Int_t>     Muon_nTrackerLayers                  {fReader, "Muon_nTrackerLayers"};
  NanoReaderArray<Int_t>     Muon_pdgId                           {fReader, "Muon_pdgId"};
  NanoReaderArray<Int_t>     Muon_tightCharge                     {fReader, "Muon_tightCharge"};
  NanoReaderArray<UChar_t>   Muon_highPtId                        {fReader, "Muon_highPtId"};
  NanoReaderArray<Bool_t>    Muon_isPFcand                        {fReader, "Muon_isPFcand"};
  NanoReaderArray<Bool_t>    Muon_mediumId                        {fReader, "Muon_mediumId"};
  NanoReaderArray<Bool_t>    Muon_softId                          {fReader, "Muon_softId"};
  NanoReaderArray<Bool_t>    Muon_tightId                         {fReader, "Muon_tightId"};
  NanoReaderArray<Bool_t>    Muon_looseId                         {fReader, "Muon_looseId"};
        
  NanoReaderValue<UInt_t>    nPhoton                              {fReader, "nPhoton"};
  NanoReaderArray<Float_t>   Photon_eCorr                         {fReader, "Photon_eCorr"};
  NanoReaderArray<Float_t>   Photon_energyErr                     {fReader, "Photon_energyErr"};
  NanoReaderArray<Float_t>   Photon_eta                           {fReader, "Photon_eta"};
  NanoReaderArray<Float_t>   Photon_hoe                           {fReader, "Photon_hoe"};
  NanoReaderArray<Float_t>   Photon_mass                          {fReader, "Photon_mass"};
  NanoReaderArray<Float_t>   Photon_mvaID                         {fReader, "Photon_mvaID"};
  NanoReaderArray<Float_t>   Photon_pfRelIso03_all                {fReader, "Photon_pfRelIso03_all"};
  NanoReaderArray<Float_t>   Photon_pfRelIso03_chg                {fReader, "Photon_pfRelIso03_chg"};
  NanoReaderArray<Float_t>   Photon_phi                           {fReader, "Photon_phi"};
  NanoReaderArray<Float_t>   Photon_pt                            {fReader, "Photon_pt"};
  NanoReaderArray<Float_t>   Photon_r9                            {fReader, "Photon_r9"};
  NanoReaderArray<Float_t>   Photon_sieie                         {fReader, "Photon_sieie"};
  NanoReaderArray<Int_t>     Photon_charge                        {fReader, "Photon_charge"};
  NanoReaderArray<Int_t>     Photon_cutBased                      {fReader, "Photon_cutBased"};
  NanoReaderArray<Int_t>     Photon_electronIdx                   {fReader, "Photon_electronIdx"};
  NanoReaderArray<Int_t>     Photon_jetIdx                        {fReader, "Photon_jetIdx"};
  NanoReaderArray<Int_t>     Photon_pdgId                         {fReader, "Photon_pdgId"};
  NanoReaderArray<Int_t>     Photon_vidNestedWPBitmap             {fReader, "Photon_vidNestedWPBitmap"};
  NanoReaderArray<Bool_t>    Photon_electronVeto                  {fReader, "Photon_electronVeto"};
  NanoReaderArray<Bool_t>    Photon_mvaID_WP80                    {fReader, "Photon_mvaID_WP80"};
  NanoReaderArray<Bool_t>    Photon_mvaID_WP90                    {fReader, "Photon_mvaID_WP90"};
  NanoReaderArray<Bool_t>    Photon_pixelSeed                     {fReader, "Photon_pixelSeed"};
        
  NanoReaderValue<Int_t>      Pileup_nPU                           {fReader, "Pileup_nPU"};
  NanoReaderValue<Float_t>    Pileup_nTrueInt                      {fReader, "Pileup_nTrueInt"};
        
  NanoReaderValue<Float_t>   fixedGridRhoFastjetAll               {fReader, "fixedGridRhoFastjetAll"};
  NanoReaderValue<Float_t>   fixedGridRhoFastjetCentralCalo       {fReader, "fixedGridRhoFastjetCentralCalo"};
  NanoReaderValue<Float_t>   fixedGridRhoFastjetCentralNeutral    {fReader, "fixedGridRhoFastjetCentralNeutral"};
        
  NanoReaderValue<UInt_t>     nGenDressedLepton                    {fReader, "nGenDressedLepton"};
  NanoReaderArray<Float_t>    GenDressedLepton_eta                 {fReader, "GenDressedLepton_eta"};
  NanoReaderArray<Float_t>    GenDressedLepton_mass                {fReader, "GenDressedLepton_mass"};
  NanoReaderArray<Float_t>    GenDressedLepton_phi                 {fReader, "GenDressedLepton_phi"};
  NanoReaderArray<Float_t>    GenDressedLepton_pt                  {fReader, "GenDressedLepton_pt"};
  NanoReaderArray<Int_t>      GenDressedLepton_pdgId               {fReader, "GenDressedLepton_pdgId"};
        
  NanoReaderValue<UInt_t>    nSoftActivityJet                     {fReader, "nSoftActivityJet"};
  NanoReaderArray<Float_t>   SoftActivityJet_eta                  {fReader, "SoftActivityJet_eta"};
  NanoReaderArray<Float_t>   SoftActivityJet_phi                  {fReader, "SoftActivityJet_phi"};
  NanoReaderArray<Float_t>   SoftActivityJet_pt                   {fReader, "SoftActivityJet_pt"};
  NanoReaderValue<Float_t>   SoftActivityJetHT                    {fReader, "SoftActivityJetHT"};
  NanoReaderValue<Float_t>   SoftActivityJetHT10                  {fReader, "SoftActivityJetHT10"};
  NanoReaderValue<Float_t>   SoftActivityJetHT2                   {fReader, "SoftActivityJetHT2"};
  NanoReaderValue<Float_t>   SoftActivityJetHT5                   {fReader, "SoftActivityJetHT5"};
  NanoReaderValue<Int_t>     SoftActivityJetNjets10               {fReader, "SoftActivityJetNjets10"};
  NanoReaderValue<Int_t>     SoftActivityJetNjets2                {fReader, "SoftActivityJetNjets2"};
  NanoReaderValue<Int_t>     SoftActivityJetNjets5                {fReader, "SoftActivityJetNjets5"};
        
  NanoReaderValue<UInt_t>    nSubJet                              {fReader, "nSubJet"};
  NanoReaderArray<Float_t>   SubJet_btagCMVA                      {fReader, "SubJet_btagCMVA"};
  NanoReaderArray<Float_t>   SubJet_btagCSVV2                     {fReader, "SubJet_btagCSVV2"};
  NanoReaderArray<Float_t>   SubJet_btagDeepB                     {fReader, "SubJet_btagDeepB"};
  NanoReaderArray<Float_t>   SubJet_eta                           {fReader, "SubJet_eta"};
  NanoReaderArray<Float_t>   SubJet_mass                          {fReader, "SubJet_mass"};
  NanoReaderArray<Float_t>   SubJet_n2b1                          {fReader, "SubJet_n2b1"};
  NanoReaderArray<Float_t>   SubJet_n3b1                          {fReader, "SubJet_n3b1"};
  NanoReaderArray<Float_t>   SubJet_phi                           {fReader, "SubJet_phi"};
  NanoReaderArray<Float_t>   SubJet_pt                            {fReader, "SubJet_pt"};
  NanoReaderArray<Float_t>   SubJet_tau1                          {fReader, "SubJet_tau1"};
  NanoReaderArray<Float_t>   SubJet_tau2                          {fReader, "SubJet_tau2"};
  NanoReaderArray<Float_t>   SubJet_tau3                          {fReader, "SubJet_tau3"};
  NanoReaderArray<Float_t>   SubJet_tau4                          {fReader, "SubJet_tau4"};

  NanoReaderArray<Float_t>   SubGenJetAK8_eta                     {fReader, "SubGenJetAK8_eta"};
  NanoReaderArray<Float_t>   SubGenJetAK8_mass                    {fReader, "SubGenJetAK8_mass"};
  NanoReaderArray<Float_t>   SubGenJetAK8_phi                     {fReader, "SubGenJetAK8_phi"};
  NanoReaderArray<Float_t>   SubGenJetAK8_pt                      {fReader, "SubGenJetAK8_pt"};
  NanoReaderValue<UInt_t>    nSubGenJetAK8                        {fReader, "nSubGenJetAK8"};
  
  NanoReaderValue<UInt_t>    nTau                                 {fReader, "nTau"};
  NanoReaderArray<Float_t>   Tau_chargedIso                       {fReader, "Tau_chargedIso"};
  NanoReaderArray<Float_t>   Tau_dxy                              {fReader, "Tau_dxy"};
  NanoReaderArray<Float_t>   Tau_dz                               {fReader, "Tau_dz"};
  NanoReaderArray<Float_t>   Tau_eta                              {fReader, "Tau_eta"};
  NanoReaderArray<Float_t>    Tau_footprintCorr                    {fReader, "Tau_footprintCorr"};
  NanoReaderArray<Float_t>   Tau_leadTkDeltaEta                   {fReader, "Tau_leadTkDeltaEta"};
  NanoReaderArray<Float_t>   Tau_leadTkDeltaPhi                   {fReader, "Tau_leadTkDeltaPhi"};
  NanoReaderArray<Float_t>   Tau_leadTkPtOverTauPt                {fReader, "Tau_leadTkPtOverTauPt"};
  NanoReaderArray<Float_t>   Tau_mass                             {fReader, "Tau_mass"};
  NanoReaderArray<Float_t>   Tau_neutralIso                       {fReader, "Tau_neutralIso"};
  NanoReaderArray<Float_t>   Tau_phi                              {fReader, "Tau_phi"};
  NanoReaderArray<Float_t>   Tau_photonsOutsideSignalCone         {fReader, "Tau_photonsOutsideSignalCone"};
  NanoReaderArray<Float_t>   Tau_pt                               {fReader, "Tau_pt"};
  NanoReaderArray<Float_t>   Tau_puCorr                           {fReader, "Tau_puCorr"};
  NanoReaderArray<Float_t>   Tau_rawAntiEle                       {fReader, "Tau_rawAntiEle"};
  NanoReaderArray<Float_t>   Tau_rawIso                           {fReader, "Tau_rawIso"};
  NanoReaderArray<Float_t>   Tau_rawMVAnewDM                      {fReader, "Tau_rawMVAnewDM"};
  NanoReaderArray<Float_t>   Tau_rawMVAoldDM                      {fReader, "Tau_rawMVAoldDM"};
  NanoReaderArray<Float_t>   Tau_rawMVAoldDMdR03                  {fReader, "Tau_rawMVAoldDMdR03"};
  NanoReaderArray<Int_t>     Tau_charge                           {fReader, "Tau_charge"};
  NanoReaderArray<Int_t>     Tau_decayMode                        {fReader, "Tau_decayMode"};
  NanoReaderArray<Int_t>     Tau_jetIdx                           {fReader, "Tau_jetIdx"};
  NanoReaderArray<Int_t>     Tau_rawAntiEleCat                    {fReader, "Tau_rawAntiEleCat"};
  NanoReaderArray<UChar_t>   Tau_idAntiEle                        {fReader, "Tau_idAntiEle"};
  NanoReaderArray<UChar_t>   Tau_idAntiMu                         {fReader, "Tau_idAntiMu"};
  NanoReaderArray<Bool_t>    Tau_idDecayMode                      {fReader, "Tau_idDecayMode"};
  NanoReaderArray<Bool_t>    Tau_idDecayModeNewDMs                {fReader, "Tau_idDecayModeNewDMs"};
  NanoReaderArray<UChar_t>   Tau_idMVAnewDM                       {fReader, "Tau_idMVAnewDM"};
  NanoReaderArray<UChar_t>   Tau_idMVAoldDM                       {fReader, "Tau_idMVAoldDM"};
  NanoReaderArray<UChar_t>   Tau_idMVAoldDMdR03                   {fReader, "Tau_idMVAoldDMdR03"};
                
  NanoReaderValue<UInt_t>    nTrigObj                             {fReader, "nTrigObj"};
  NanoReaderArray<Float_t>   TrigObj_pt                           {fReader, "TrigObj_pt"};
  NanoReaderArray<Float_t>   TrigObj_eta                          {fReader, "TrigObj_eta"};
  NanoReaderArray<Float_t>   TrigObj_phi                          {fReader, "TrigObj_phi"};
  NanoReaderArray<Float_t>   TrigObj_l1pt                         {fReader, "TrigObj_l1pt"};
  NanoReaderArray<Float_t>   TrigObj_l1pt_2                       {fReader, "TrigObj_l1pt_2"};
  NanoReaderArray<Float_t>   TrigObj_l2pt                         {fReader, "TrigObj_l2pt"};
  NanoReaderArray<Int_t>     TrigObj_id                           {fReader, "TrigObj_id"};
  NanoReaderArray<Int_t>     TrigObj_l1iso                        {fReader, "TrigObj_l1iso"};
  NanoReaderArray<Int_t>     TrigObj_l1charge                     {fReader, "TrigObj_l1charge"};
  NanoReaderArray<Int_t>     TrigObj_filterBits                   {fReader, "TrigObj_filterBits"};
        
  NanoReaderValue<Int_t>      genTtbarId                           {fReader, "genTtbarId"};
        
  NanoReaderValue<UInt_t>    nOtherPV                             {fReader, "nOtherPV"};
  NanoReaderArray<Float_t>   OtherPV_z                            {fReader, "OtherPV_z"};
        
  NanoReaderValue<Float_t>   PV_ndof                              {fReader, "PV_ndof"};
  NanoReaderValue<Float_t>   PV_x                                 {fReader, "PV_x"};
  NanoReaderValue<Float_t>   PV_y                                 {fReader, "PV_y"};
  NanoReaderValue<Float_t>   PV_z                                 {fReader, "PV_z"};
  NanoReaderValue<Float_t>   PV_chi2                              {fReader, "PV_chi2"};
  NanoReaderValue<Float_t>   PV_score                             {fReader, "PV_score"};
  NanoReaderValue<Int_t>     PV_npvs                              {fReader, "PV_npvs"};
  NanoReaderValue<Int_t>     PV_npvsGood                          {fReader, "PV_npvsGood"};
        
  NanoReaderValue<UInt_t>    nSV                                  {fReader, "nSV"};
  NanoReaderArray<Float_t>   SV_dlen                              {fReader, "SV_dlen"};
  NanoReaderArray<Float_t>   SV_dlenSig                           {fReader, "SV_dlenSig"};
  NanoReaderArray<Float_t>   SV_pAngle                            {fReader, "SV_pAngle"};
                
  NanoReaderArray<Int_t>     GenJetAK8_partonFlavour               {fReader, "GenJetAK8_partonFlavour"};
  NanoReaderArray<UChar_t>   GenJetAK8_hadronFlavour               {fReader, "GenJetAK8_hadronFlavour"};
  NanoReaderArray<Int_t>     GenJet_partonFlavour                  {fReader, "GenJet_partonFlavour"};
  NanoReaderArray<UChar_t>   GenJet_hadronFlavour                  {fReader, "GenJet_hadronFlavour"};
        
  NanoReaderArray<Int_t>     Muon_genPartIdx                       {fReader, "Muon_genPartIdx"};
  NanoReaderArray<UChar_t>   Muon_genPartFlav                      {fReader, "Muon_genPartFlav"};
        
  NanoReaderArray<Int_t>     Photon_genPartIdx                     {fReader, "Photon_genPartIdx"};
  NanoReaderArray<UChar_t>   Photon_genPartFlav                    {fReader, "Photon_genPartFlav"};

  NanoReaderArray<Int_t>     Tau_genPartIdx                        {fReader, "Tau_genPartIdx"};
  NanoReaderArray<UChar_t>   Tau_genPartFlav                       {fReader, "Tau_genPartFlav"};
        
  NanoReaderValue<Float_t>   MET_fiducialGenPhi                    {fReader, "MET_fiducialGenPhi"};
  NanoReaderValue<Float_t>   MET_fiducialGenPt                     {fReader, "MET_fiducialGenPt"};
        
  NanoReaderArray<UChar_t>   Jet_cleanmask                        {fReader, "Jet_cleanmask"};
  NanoReaderArray<UChar_t>   Muon_cleanmask                       {fReader, "Muon_cleanmask"};
  NanoReaderArray<UChar_t>   Photon_cleanmask                     {fReader, "Photon_cleanmask"};
  NanoReaderArray<UChar_t>   Tau_cleanmask                        {fReader, "Tau_cleanmask"};
        
  NanoReaderArray<Float_t>   SV_chi2                              {fReader, "SV_chi2"};
  NanoReaderArray<Float_t>   SV_eta                               {fReader, "SV_eta"};
  NanoReaderArray<Float_t>   SV_mass                              {fReader, "SV_mass"};
  NanoReaderArray<Float_t>   SV_ndof                              {fReader, "SV_ndof"};
  NanoReaderArray<Float_t>   SV_phi                               {fReader, "SV_phi"};
  NanoReaderArray<Float_t>   SV_pt                                {fReader, "SV_pt"};
  NanoReaderArray<Float_t>   SV_x                                 {fReader, "SV_x"};
  NanoReaderArray<Float_t>   SV_y                                 {fReader, "SV_y"};
  NanoReaderArray<Float_t>   SV_z                                 {fReader, "SV_z"};
};

#endif
