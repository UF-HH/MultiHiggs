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
#include "PhysicsTools/TensorFlow/interface/TensorFlow.h"

class EvalNN {
public:
	EvalNN(
		   std::string graphPath,
		   std::string input_name = "input_1",
		   std::vector<std::string> outputs_name = {"regr/BiasAdd", "discr/Sigmoid"}
		   ) ;
	~EvalNN();
	std::vector<float> evaluate (const std::vector<float>& inputs);

private:
	std::string graphPath_;

	tensorflow::GraphDef* graphDef_;
	tensorflow::Session*  session_;

	std::string input_name_;
	std::vector<std::string> outputs_name_;

};

EvalNN::EvalNN(
			   std::string graphPath,
			   std::string input_name,
			   std::vector<std::string> outputs_name
			   )
{
    graphPath_    = graphPath;
    graphDef_     = tensorflow::loadGraphDef(graphPath_);
    session_      = tensorflow::createSession(graphDef_);
    input_name_   = input_name;
    outputs_name_ = outputs_name;
}

EvalNN::~EvalNN()
{
    // close the session
    tensorflow::closeSession(session_);
    session_ = nullptr;

    // delete the graph
    delete graphDef_;
    graphDef_ = nullptr;
}

std::vector<float> EvalNN::evaluate (const std::vector<float>& inputs)
{
    long long int n_inputs = inputs.size();
    tensorflow::Tensor input(tensorflow::DT_FLOAT, { 1, n_inputs });
    for (unsigned int i = 0; i < n_inputs; ++i)
        input.matrix<float>()(0, i) = inputs.at(i);

    // define the output and run
    // std::cout << "session.run" << std::endl;
    std::vector<tensorflow::Tensor> outputs;
    tensorflow::run(session_, { { input_name_, input } }, outputs_name_, &outputs);

    // check and print the output
    // std::cout << " -> " << outputs[0].matrix<float>()(0, 0) << std::endl << std::endl;
    std::vector<float> out(outputs.size());
    for (unsigned int o = 0; o < outputs.size(); ++o)
        out.at(o) = outputs.at(o).matrix<float>()(0, 0);

    return out;
}

#endif
