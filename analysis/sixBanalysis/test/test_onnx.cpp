#include "PhysicsTools/ONNXRuntime/interface/ONNXRuntime.h"

#include <iostream>
#include <string>
#include <vector>

#include "DebugUtils.h"
#include "EvalONNX.h"

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp> 

#include "Skim_functions.h"
#include "EightB_functions.h"

#include "TFile.h"
#include "TROOT.h"
#include "TH1F.h"

using namespace std;
using namespace cms::Ort;
namespace pt = boost::property_tree;

#include "NanoAODTree.h"
#include "SkimUtils.h"
namespace su = SkimUtils;

template<typename T>
std::vector<T> flatten(std::vector<std::vector<T>> const &vec)
{
    std::vector<T> flattened;
    for (auto const &v: vec) {
        flattened.insert(flattened.end(), v.begin(), v.end());
    }
    return flattened;
}

template<typename T>
std::vector<std::vector<T>> unflatten(std::vector<T> const &vec, int outer, int inner)
{
  if (outer == -1)
    outer = vec.size() / inner;
  else if (inner == -1)
    inner = vec.size() / outer;

  if (outer * inner != (int)vec.size())
  {
    string msg = "Cannot shape vector of size " + to_string(vec.size()) + " to size (" + to_string(outer) + ", " +
                 to_string(inner) + ")";
    throw std::length_error(msg);
  }

  std::vector<std::vector<T>> unflattened;
  for (int i = 0; i < inner; i++) {
    int start = i * outer;
    int end = start + outer;

    std::vector<T> column;
    column.insert(column.end(), vec.begin() + start, vec.begin() + end);
    unflattened.push_back(column);
  }

  return unflattened;
}

float compare_vectors(std::vector<std::vector<float>> test, std::vector<std::vector<float>> targ)
{
  int test_outer = test.size();
  int test_inner = test[0].size();

  int targ_outer = targ.size();
  int targ_inner = targ[0].size();

  if (test_outer != targ_outer || test_inner != targ_inner)
    throw std::length_error("test vector shape (" + to_string(test_outer) + ", " + to_string(test_inner) +
                            ") does not match targ vector shape (" + to_string(targ_outer) + ", " +
                            to_string(targ_inner) + ")");

  float difference = 0;
  for (int col = 0; col < targ.size(); col++)
  {
    vector<float> targ_col = targ[col];
    vector<float> test_col = test[col];
    for (int row = 0; row < targ_col.size(); row++) {
      difference = pow(targ_col[row] - test_col[row], 2);
    }
  }
  return difference;
}

void test_json() 
{
  cout << "Testing JSON Parsing" << endl;

  string json_path =
      "/uscms_data/d3/ekoenig/8BAnalysis/studies/weaver-benchmark/x_yy_4h_8b/models/graph_dijet/export/preprocess.json";

  
  pt::ptree root;

  // Load the json file in this ptree
  pt::read_json(json_path, root);

  vector<string> input_names;
  for (pt::ptree::value_type &name : root.get_child("input_names"))
  {
    input_names.push_back(name.second.data());
  }
  dumpVector(input_names);

  FeatureMap fl(root, input_names[0]);
  fl.print();
}

void test_eval_onnx()
{
  cout << "Testing EvalONNX" << endl;
  string name = "graph_dijet";
  string path = "/uscms_data/d3/ekoenig/8BAnalysis/studies/weaver-benchmark/x_yy_4h_8b/models/graph_dijet/export/";
  string file =
      "/eos/uscms/store/user/ekoenig/8BAnalysis/NTuples/2018/preselection/t8btag_minmass/NMSSM_XYY_YToHH_8b/"
      "NMSSM_XYY_YToHH_8b_MX_1000_MY_450_accstudies.root";

  

  EvalONNX gnn(name, path);

  // Process One Event
}

int main() 
{
    // test_onnx();
    // test_json();
    test_eval_onnx();
}