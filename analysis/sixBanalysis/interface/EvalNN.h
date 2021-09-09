/*
** class   : EvalNN
** author  : L. Cadamuro (UF)
** date    : 21/07/2018
** brief   : evaluate the NN regression for the muon pT assignment
*/

// all from the examples here: https://gitlab.cern.ch/mrieger/CMSSW-TensorFlowExamples/blob/master/GraphLoading/plugins/GraphLoading.cc
// and some inspired googling

#ifndef EVALNN_H
#define EVALNN_H

#include <string>
#include <iostream>
#include "CfgParser.h"
#include "PhysicsTools/TensorFlow/interface/TensorFlow.h"
#include "TFile.h"

class EvalNN {
public:
  EvalNN(
	 std::string name,
	 std::string graphPath,
	 std::string input_name = "dense_input",
	 std::string modelName = "model.pb",
	 std::string configName = "model.cfg"
	 ) ;
  ~EvalNN();
  std::vector<float> evaluate (const std::vector<float>& inputs);
  void set_output(std::string output) { outputs_name_ = {output}; }
  void set_debug(bool debug) { debug_ = debug; }
  void write(TFile& tfile);

private:
  bool debug_ = false;

  std::string name_;
  std::string graphPath_;
  std::string modelName_;
  std::string configName_;

  CfgParser config_;
  tensorflow::GraphDef* graphDef_;
  tensorflow::Session*  session_;

  std::vector<float> scale_min_;
  std::vector<float> scale_max_;

  std::string input_name_;
  std::vector<std::string> outputs_name_;

};

#endif
