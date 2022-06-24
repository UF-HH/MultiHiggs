#ifndef EVALONNX_H
#define EVALONNX_H

#include "PhysicsTools/ONNXRuntime/interface/ONNXRuntime.h"

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <boost/property_tree/ptree.hpp>

using namespace cms::Ort;
namespace pt = boost::property_tree;

struct Feature {
  Feature(pt::ptree root, std::string name, std::string var);
  void preprocess(std::vector<float> &feature, int pad_length = -1);
  void print();

  std::string name;
  float median;
  float norm_factor;
  float replace_inf_value;
  float lower_bound;
  float upper_bound;
  float pad;
};

struct FeatureMap {
  FeatureMap(pt::ptree root, std::string name);
  std::vector<float> preprocess(std::map<std::string, std::vector<float>> inputs);
  void print();

  std::string name_;
  int length_;
  std::vector<std::string> feature_names;
  std::map<std::string, Feature*> features;
  std::vector<int64_t> shape;
};

class EvalONNX {
public:
  EvalONNX(std::string name,
           std::string graphPath,
           std::string modelName = "model.onnx",
           std::string jsonName = "preprocess.json");
  std::vector<float> evaluate(std::map<std::string, std::vector<float>> inputs);
  void print();

private:
  
  std::string name_;
  std::string graphPath_;
  std::string modelName_;
  std::string jsonName_;

  std::unique_ptr<ONNXRuntime> ort;
  std::vector<std::string> input_names;
  std::map<std::string, FeatureMap*> inputMap;
  std::vector<std::vector<int64_t>> input_shapes;
};

#endif  // EVALONNX_H