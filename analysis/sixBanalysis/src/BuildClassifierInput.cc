#include "BuildClassifierInput.h"

std::vector<std::vector<int>> get_6jet_index_combos(int n,int r)
{
  std::vector<std::vector<int>> index_combos;
	
  std::vector<bool> v(n);
  std::fill(v.end() - r, v.end(), true);
	
  do {
    std::vector<int> combo;
    for (int i = 0; i < n; ++i) {
      if (v[i]) {
	combo.push_back(i);
      }
    }
    index_combos.push_back(combo);
  } while (std::next_permutation(v.begin(), v.end()));
  return index_combos;
}

float get_dijet_dr(const Jet& j1,const Jet& j2)
{
  return ROOT::Math::VectorUtil::DeltaR( j1.P4Regressed(),j2.P4Regressed() );
}

float get_dijet_pt(const Jet& j1,const Jet& j2)
{
  return (j1.P4Regressed()+j2.P4Regressed()).Pt();
}

std::vector<float> build_6jet_classifier_input(std::vector<Jet> in_jets)
{
  std::vector<float> input_array;
  if (in_jets.size() != 6) return input_array;
	
  std::vector<std::vector<float>> input_matrix;
  // std::sort(in_jets.begin(),in_jets.end(),[](Jet& j1,Jet& j2){ return j1.get_pt()>j2.get_pt(); });

  int nvar = 5;
  for (int i = 0; i < nvar; i++) input_matrix.push_back(std::vector<float>());
  p4_t com = in_jets[0].P4Regressed() + in_jets[1].P4Regressed() + in_jets[2].P4Regressed() + in_jets[3].P4Regressed() + in_jets[4].P4Regressed() + in_jets[5].P4Regressed();

  for (Jet& j : in_jets)
    {
      input_matrix[0].push_back( j.get_pt() );
      input_matrix[1].push_back( j.get_eta() );
      input_matrix[2].push_back( j.get_phi() );
      input_matrix[3].push_back( j.get_btag() );
      input_matrix[4].push_back( (j.P4Regressed() - com).Pt() );
    }

  for ( std::vector<float> input : input_matrix ) input_array.insert(input_array.end(),input.begin(),input.end());

  return input_array;
}

std::vector<float> build_6jet_classifier_input(const std::vector<Jet>& in_jets,const std::vector<int>& indices)
{
  std::vector<Jet> input_jets;
  for (int i : indices) input_jets.push_back( in_jets[i] );
  return build_6jet_classifier_input(input_jets);
}

std::vector<float> build_3dijet_classifier_input(std::vector<Jet> in_jets)
{
  std::vector<float> input_array;
  if (in_jets.size() != 6) return input_array;
  std::vector< std::vector<Jet> > dijets = {
    {in_jets[0],in_jets[1]},
    {in_jets[2],in_jets[3]},
    {in_jets[4],in_jets[5]}
  };

  std::sort(dijets.begin(),dijets.end(),[](std::vector<Jet> d1,std::vector<Jet> d2){ return get_dijet_pt(d1[0],d1[1]) > get_dijet_pt(d2[0],d2[1]); });
  for (int i = 0; i < 3; i++) std::sort(dijets[i].begin(),dijets[i].end(),[](Jet& j1,Jet& j2){ return j1.get_pt()>j2.get_pt(); });

  std::vector<std::vector<float>> input_matrix;
  int nvars = 6;
  for (int i = 0; i < nvars; i++) input_matrix.push_back(std::vector<float>());
  
  for ( std::vector<Jet> jet_pair : dijets )
    {
      for (Jet& j : jet_pair)
	{
	  input_matrix[0].push_back( j.get_pt() );
	  input_matrix[1].push_back( j.get_eta() );
	  input_matrix[2].push_back( j.get_phi() );
	  input_matrix[3].push_back( j.get_btag() );
	}
      input_matrix[4].push_back( get_dijet_pt(jet_pair[0],jet_pair[1]) );
      input_matrix[5].push_back( get_dijet_dr(jet_pair[0],jet_pair[1]) );
    }
  
  for ( std::vector<float> input : input_matrix ) input_array.insert(input_array.end(),input.begin(),input.end());
  return input_array;
}

std::vector<float> build_3dijet_classifier_input(const std::vector<Jet>& in_jets,const std::vector<int>& indices)
{ 
  std::vector<Jet> input_jets;
  for (int i : indices) input_jets.push_back( in_jets[i] );
  return build_3dijet_classifier_input(input_jets);
}


std::vector<float> build_2jet_classifier_input(std::vector<Jet> in_jets)
{
  std::vector<float> input_array;
  if (in_jets.size() != 2) return input_array;
	
  std::vector<std::vector<float>> input_matrix;
  
  std::sort(in_jets.begin(),in_jets.end(),[](Jet& j1,Jet& j2){ return j1.get_pt()>j2.get_pt(); });

  int nvar = 5;
  for (int i = 0; i < nvar; i++) input_matrix.push_back(std::vector<float>());

  for (Jet& j : in_jets)
    {
      input_matrix[0].push_back( j.get_pt() );
      input_matrix[1].push_back( j.get_eta() );
      input_matrix[2].push_back( j.get_phi() );
      input_matrix[3].push_back( j.get_btag() );
    }
  input_matrix[4].push_back( get_dijet_dr(in_jets[0],in_jets[1]) );

  for ( std::vector<float> input : input_matrix ) input_array.insert(input_array.end(),input.begin(),input.end());

  return input_array;
}

std::vector<float> build_2jet_classifier_input(const std::vector<Jet>& in_jets,const std::vector<int>& indices)
{
  std::vector<Jet> input_jets;
  for (int i : indices) input_jets.push_back( in_jets[i] );
  return build_2jet_classifier_input(input_jets);
}
