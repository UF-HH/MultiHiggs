#include "NormWeightTree.h"

using namespace std;

NormWeightTree::NormWeightTree (string name, string title) :
  BaseOutTree(name, title, "NormWeightTree")
{
  void init_branches(NanoAODTree& nat);
  verbosity_ = 1;
}

void NormWeightTree::init_weights(NanoAODTree& nat, std::map<std::string, std::string> pu_data){
    
  init_gen_weight();
  init_pu_weight(
		 pu_data.at("filename"),
		 pu_data.at("name_PU_w"),
		 pu_data.at("name_PU_w_up"),
		 pu_data.at("name_PU_w_do")
		 );
  init_pdf_weight(nat);
  init_scale_weight(nat);
  init_ps_weight(nat);
}

void NormWeightTree::read_weights(NanoAODTree &nat)
{
  read_gen_weight   (nat);
  read_pu_weight    (nat);
  read_pdf_weight   (nat);
  read_scale_weight (nat);
  read_ps_weight    (nat);
}

// -----------------------------------------------
// initialisations

void NormWeightTree::make_branches(weight_t &weight){
  tree_->Branch(weight.name.c_str(), &weight.w);
  for (uint is = 0; is < weight.syst_val.size(); ++is)
    tree_->Branch(weight.syst_name.at(is).c_str(), &weight.syst_val.at(is));
}

void NormWeightTree::init_gen_weight(){
  gen_w_.w         = 1.0;
  gen_w_.name      = "genWeight";
  gen_w_.syst_val  = {}; // no systematic for gen weight
  gen_w_.syst_name = {};
  if (verbosity_ >= 1)
    cout << "[INFO] NormWeightTree : initialising gen weights" << endl;
  make_branches(gen_w_);
}

void NormWeightTree::init_pu_weight(std::string filename, std::string name_PU_w, std::string name_PU_w_up, std::string name_PU_w_do){

  if (verbosity_ >= 1)
    cout << "[INFO] NormWeightTree : PU weights will use file " << filename << " and histo " << name_PU_w  << " . up/down: " << name_PU_w_up << "/" << name_PU_w_do << endl;
  pu_wread_.init_data(filename, name_PU_w, name_PU_w_up, name_PU_w_do);

  pu_w_.w         = 1.0;
  pu_w_.name      = "PUWeight";
  pu_w_.syst_val  = {1.0, 1.0};
  pu_w_.syst_name = {"PUWeight_up", "PUWeight_down"};
  if (verbosity_ >= 1)
    cout << "[INFO] NormWeightTree : initialising PU weights with " << pu_w_.syst_val.size() << " variations" << endl;
  make_branches(pu_w_);    
}

void NormWeightTree::init_pdf_weight(NanoAODTree &nat){
  uint n_pdf_weight = *(nat.nLHEPdfWeight);
  pdf_w_.w    = 1.0;
  pdf_w_.name = "LHEPdfWeight";
  pdf_w_.syst_val.resize(n_pdf_weight);
  pdf_w_.syst_name.resize(n_pdf_weight);
  for (uint is = 0; is < n_pdf_weight; ++is){
    pdf_w_.syst_val.at(is)  = 0;
    pdf_w_.syst_name.at(is) = string("LHEPdfWeight") + string("_var") + std::to_string(is);
  }
  if (verbosity_ >= 1)
    cout << "[INFO] NormWeightTree : initialising PDF weights with " << pdf_w_.syst_val.size() << " variations" << endl;
  make_branches(pdf_w_);
}

void NormWeightTree::init_scale_weight(NanoAODTree &nat){
  uint n_scale_weight = *(nat.nLHEScaleWeight);
  scale_w_.w    = 1.0;
  scale_w_.name = "LHEScaleWeight";
  scale_w_.syst_val.resize(n_scale_weight);
  scale_w_.syst_name.resize(n_scale_weight);
  for (uint is = 0; is < n_scale_weight; ++is){
    scale_w_.syst_val.at(is)  = 0;
    scale_w_.syst_name.at(is) = string("LHEScaleWeight") + string("_var") + std::to_string(is);
  }
  if (verbosity_ >= 1)
    cout << "[INFO] NormWeightTree : initialising scale weights with " << scale_w_.syst_val.size() << " variations" << endl;
  make_branches(scale_w_);
}

void NormWeightTree::init_ps_weight(NanoAODTree &nat){
  uint n_ps_weight = *(nat.nPSWeight);
  ps_w_.w    = 1.0;
  ps_w_.name = "PSWeight";
  ps_w_.syst_val.resize(n_ps_weight);
  ps_w_.syst_name.resize(n_ps_weight);
  for (uint is = 0; is < n_ps_weight; ++is){
    ps_w_.syst_val.at(is)  = 0;
    ps_w_.syst_name.at(is) = string("PSWeight") + string("_var") + std::to_string(is);
  }
  if (verbosity_ >= 1)
    cout << "[INFO] NormWeightTree : initialising PS weights with " << ps_w_.syst_val.size() << " variations" << endl;
  make_branches(ps_w_);
}

// -----------------------------------------------
// reading

void NormWeightTree::read_gen_weight(NanoAODTree &nat){
  gen_w_.w = *(nat.genWeight);
}

void NormWeightTree::read_pu_weight(NanoAODTree &nat){

  float PU     = *(nat.Pileup_nTrueInt);
  auto weights = pu_wread_.get_weight(PU); // nominal, up, down
  pu_w_.w              = std::get<0>(weights); 
  pu_w_.syst_val.at(0) = std::get<1>(weights);
  pu_w_.syst_val.at(1) = std::get<2>(weights);
}

void NormWeightTree::read_pdf_weight(NanoAODTree &nat){
    
  // pdf_w_.w = 1.0; // leave as default
  uint nvars = *(nat.nLHEPdfWeight);
  if (nvars != pdf_w_.syst_val.size()){
    cout << "[ERROR] : NormWeightTree : there are " << nvars << "variations in the event and  " << pdf_w_.syst_val.size() << " variations expected" << endl;
    throw std::runtime_error("NormWeightTree : pdf weight size mismatch");
  }
  for (uint is = 0; is < nvars; ++is){
    pdf_w_.syst_val.at(is) = nat.LHEPdfWeight.At(is);
  }
}

void NormWeightTree::read_scale_weight(NanoAODTree &nat){
   
  // scale_w_.w = 1.0; // leave as default
  uint nvars = *(nat.nLHEScaleWeight);
  if (nvars != scale_w_.syst_val.size())
    {
      cout << "[ERROR] : NormWeightTree : there are " << nvars << "variations in the event and  " << scale_w_.syst_val.size() << " variations expected" << endl;
      throw std::runtime_error("NormWeightTree : scale weight size mismatch");
    }
  for (uint is = 0; is < nvars; ++is)
    {
      scale_w_.syst_val.at(is) = nat.LHEScaleWeight.At(is);
    }
}

void NormWeightTree::read_ps_weight(NanoAODTree &nat){
    
  // ps_w_.w = 1.0; // leave as default
  uint nvars = *(nat.nPSWeight);
  if (nvars != ps_w_.syst_val.size())
    {
      cout << "[ERROR] : NormWeightTree : there are " << nvars << "variations in the event and  " << ps_w_.syst_val.size() << " variations expected" << endl;
      throw std::runtime_error("NormWeightTree : ps weight size mismatch");
    }
  for (uint is = 0; is < nvars; ++is)
    {
      ps_w_.syst_val.at(is) = nat.PSWeight.At(is);
    }
}

// -----------------------------------------------
// extra weights

void NormWeightTree::add_weight(std::string wname, std::vector <std::string> wsystsname){

  if (verbosity_ >= 1){
    cout << "[INFO] NormWeightTree : adding an external weight named " << wname << " with " << wsystsname.size() << " syst variations (listed below)" << endl;
    for (auto s : wsystsname){
      cout << "   - " << s << endl;
    }
  }

  weight_t def_w;
  def_w.w         = 1.0;
  def_w.name      = wname;
  def_w.syst_val = std::vector<double>(wsystsname.size(), 1.0);
  def_w.syst_name = wsystsname;

  if (!extra_weights_.addVal(wname, def_w)){
    cout << "[ERROR] : NormWeightTree : could not add the weight " << wname << endl;
    throw std::runtime_error("NormWeightTree : user weight not added");
  }
  extra_weights_names_.emplace_back(wname);

  // create branches
  tree_->Branch(wname.c_str(), &(extra_weights_.getVal(wname).w));
  for (uint is = 0; is < wsystsname.size(); ++is){
    tree_->Branch(wsystsname.at(is).c_str(), &(extra_weights_.getVal(wname).syst_val.at(is)));
  }
}
