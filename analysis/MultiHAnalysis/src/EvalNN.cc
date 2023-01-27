#include "EvalNN.h"

#include "TNamed.h"
#include "TH1.h"

std::string vector_string(std::vector<float> array)
{
  std::string str = "[ ";
  for (float element : array) str += std::to_string(element)+" ";
  str += "]";
  return str;
}

void debug_network(std::vector<float> inputs,std::vector<float> outputs)
{
  std::cout << "[INPUT]: " << vector_string(inputs) << std::endl;
  std::cout << "[OUTPUT]:" << vector_string(outputs) << std::endl;
}

EvalNN::EvalNN(std::string name,std::string graphPath,std::string input_name,std::string modelName,std::string configName)
{
  name_         = name;
  graphPath_    = graphPath;
  modelName_    = modelName;
  configName_   = configName;
	
  graphDef_     = tensorflow::loadGraphDef(graphPath_+"/"+modelName_);
  session_      = tensorflow::createSession(graphDef_);
  input_name_   = input_name;

  if (!config_.init(graphPath+"/"+configName_)) {
    std::cerr << "** [ERROR] config file does not exist" << std::endl;
  }

  int n_hidden_layers = config_.readIntOpt("model::num_hidden_layers");
  std::string output_function = config_.readStringOpt("model::output_activation_function");
  outputs_name_ = {"dense_"+std::to_string(n_hidden_layers)+"/"+output_function};

  scale_min_ = config_.readFloatListOpt("scaler::scale_min");
  scale_max_ = config_.readFloatListOpt("scaler::scale_max");
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
  for (unsigned int i = 0; i < n_inputs; ++i) {
    input.matrix<float>()(0, i) = (inputs[i] - scale_min_[i])/(scale_max_[i]-scale_min_[i]);
  }

  // define the output and run
  // std::cout << "session.run" << std::endl;
  std::vector<tensorflow::Tensor> outputs;
  tensorflow::run(session_, { { input_name_, input } }, outputs_name_, &outputs);

  auto output = outputs[0].tensor<float,2>();

  std::vector<float> out(output.size());
  for (int i = 0; i < output.size(); i++) out[i] = output(0,i);

  if (debug_) debug_network(inputs,out);
  return out;
}

void EvalNN::write(TFile& tfile)
{
  tfile.cd();
  
  auto base = tfile.mkdir(name_.c_str());
  base->cd();
  
  const cfgBlock cfg = config_.getCfg();
  for ( const auto it : cfg )
    { 
      std::string block = it.first;
      auto d_block = base->mkdir(block.c_str());
      d_block->cd();

      for ( const auto kv : it.second )
	{
	  std::string key = kv.first;
	  std::string value = kv.second;

	  TH1F kv_(key.c_str(),value.c_str(),1,0,1);
	  kv_.Write();
	}
      d_block->Write();
    }
  base->Write();
  tfile.cd();
}
