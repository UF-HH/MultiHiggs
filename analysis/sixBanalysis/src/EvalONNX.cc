#include "EvalONNX.h"
// #include "DebugUtils.h"

#include <boost/property_tree/json_parser.hpp>

using namespace std;

template <typename T>
std::vector<std::vector<T>> unflatten(std::vector<T> const &vec, int outer, int inner) {
  if (outer == -1)
    outer = vec.size() / inner;
  else if (inner == -1)
    inner = vec.size() / outer;

  if (outer * inner != (int)vec.size()) {
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

vector<float> EvalONNX::evaluate(map<string, vector<float>> inputs) {
  vector<vector<float>> data;
  for (string input_name : input_names) {
    vector<float> data_ = inputMap[input_name]->preprocess(inputs);
    data.push_back(data_);
  }

  vector<float> flat_output = ort->run(input_names, data, input_shapes)[0];
  vector<float> output = unflatten(flat_output, -1, 2)[1];
  return output;
}

EvalONNX::EvalONNX(string name, string graphPath, string modelName, string jsonName) {
  name_ = name;
  graphPath_ = graphPath;
  modelName_ = modelName;
  jsonName_ = jsonName;

  ort = std::make_unique<ONNXRuntime>(graphPath + "/" + modelName);

  pt::ptree root;
  // Load the json file in this ptree
  pt::read_json(graphPath + "/" + jsonName, root);

  input_names.clear();
  input_shapes.clear();
  for (pt::ptree::value_type &name : root.get_child("input_names")) {
    string input_name = name.second.data();
    input_names.push_back(input_name);
    inputMap[input_name] = new FeatureMap(root, input_name);
    input_shapes.push_back(inputMap[input_name]->shape);
  }
}

void EvalONNX::print() {
  cout << name_ << endl;
  cout << "path: " << graphPath_ << endl;
  for (string input_name : input_names)
    inputMap[input_name]->print();
}

FeatureMap::FeatureMap(pt::ptree root, string name) {
  name_ = name;
  length_ = root.get<int>(name + ".var_length");

  feature_names.clear();
  for (pt::ptree::value_type &var : root.get_child(name + ".var_names")) {
    string varname = var.second.data();

    feature_names.push_back(varname);
    features[varname] = new Feature(root, name_, varname);
  }

  std::vector<int64_t> shape_ = {1, (int64_t)feature_names.size(), (int64_t)length_};
  shape = shape_;
}

vector<float> FeatureMap::preprocess(map<string, vector<float>> inputs) {
  vector<float> data;
  for (string feature_name : feature_names) {
    vector<float> feature(inputs[feature_name]);
    features[feature_name]->preprocess(feature, length_);
    data.insert(data.end(), feature.begin(), feature.end());
  }
  return data;
}

void FeatureMap::print() {
  cout << "-" << name_ << endl;
  cout << "\tvar length: " << length_ << endl;
  for (string feature_name : feature_names)
    features[feature_name]->print();
}

Feature::Feature(pt::ptree root, string name, string var) {
  this->name = var;
  median = root.get<float>(name + ".var_infos." + var + ".median");
  norm_factor = root.get<float>(name + ".var_infos." + var + ".norm_factor");
  replace_inf_value = root.get<float>(name + ".var_infos." + var + ".replace_inf_value");
  lower_bound = root.get<float>(name + ".var_infos." + var + ".lower_bound");
  upper_bound = root.get<float>(name + ".var_infos." + var + ".upper_bound");
  pad = root.get<float>(name + ".var_infos." + var + ".pad");
}

void Feature::preprocess(vector<float> &feature, int pad_length) {
  // standardize features
  for (unsigned int i = 0; i < feature.size(); i++) {
    float value = norm_factor * (feature[i] - median);
    if (value > upper_bound)
      value = upper_bound;
    if (value < lower_bound)
      value = lower_bound;
    feature[i] = value;
  }

  // allow jagged features
  if (pad_length == -1)
    return;

  int padding = pad_length - feature.size();

  if (padding < 0) {  // truncate feature vector to pad_length
    feature.resize(feature.size() + padding);
  } else if (padding > 0) {  // pad feature vector to pad_length
    vector<float> pad_values(padding, pad);
    feature.insert(feature.end(), pad_values.begin(), pad_values.end());
  }
}

void Feature::print() {
  cout << "--" << name << endl;
  cout << "\tmedian:            " << median << endl;
  cout << "\tnorm factor:       " << norm_factor << endl;
  cout << "\treplace inf value: " << replace_inf_value << endl;
  cout << "\tlower bound:       " << lower_bound << endl;
  cout << "\tupper bound:       " << upper_bound << endl;
  cout << "\tpad:               " << pad << endl;
}