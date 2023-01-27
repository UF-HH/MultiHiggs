 #include "TTBar_functions.h"
#include "Math/VectorUtil.h"
#include "Math/Vector3D.h"
#include "Math/Functions.h"

#include "BuildClassifierInput.h"

// #include "DebugUtils.h"

#include <iostream>
#include <tuple>
#include <algorithm>

#include "Electron.h"
#include "Muon.h"

using namespace std;

std::vector<Jet> TTBar_functions::select_jets(NanoAODTree &nat, EventInfo &ei, const std::vector<Jet> &in_jets)
{
  std::vector<Jet> jets = in_jets;
  stable_sort(jets.begin(), jets.end(), [](const Jet& a, const Jet& b) -> bool {
    return ( get_property (a, Jet_btagDeepFlavB) > get_property (b, Jet_btagDeepFlavB) ); }
    ); // sort jet by deepjet score (highest to lowest)

  if (jets.size() < 2)
    return jets;
  ei.bjet1 = jets.at(0);
  ei.bjet2 = jets.at(1);
  if (ei.bjet1->P4().Pt() < ei.bjet2->P4().Pt()) // sort by pt
    std::swap(ei.bjet1, ei.bjet2);

  return jets;

  // int n_out = std::min<int>(jets.size(), 6);
  // jets.resize(n_out);

  // for (auto& jet : jets)
  //     std::cout << jet.P4().Pt() << " " << get_property (jet, Jet_btagDeepFlavB) << std::endl;
  // std::cout << std::endl << std::endl;

  // return jets;

}
