#include "DiJet.h"

#include "Math/VectorUtil.h"
#include "Math/Vector3D.h"
#include "Math/Functions.h"

DiJet::DiJet(Jet& j1,Jet& j2)
{
  p4 = j1.P4Regressed() + j2.P4Regressed();
  dr_ = ROOT::Math::VectorUtil::DeltaR( j1.P4Regressed(),j2.P4Regressed() );

  std::vector<int> jet_signalId = { j1.get_signalId(),j2.get_signalId() };
  std::sort(jet_signalId.begin(),jet_signalId.end());

  int j1_id = jet_signalId[0]; int j2_id = jet_signalId[1];

  int id_diff = j2_id - j1_id;
  int id2_mod = j2_id % 2;
  int id = j1_id/2;

  if ( id_diff == 1 && id2_mod == 1 )
    signalId = id;
}
