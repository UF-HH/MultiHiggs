#include "EvalNN.h"

#include <fstream>

std::vector<std::string> split(std::string str,std::string delim)
{
  std::vector<std::string> splitString;
  char strChar[str.size() + 1];
  strcpy(strChar,str.c_str());
  char *token = strtok(strChar,delim.c_str());
  while (token != NULL) {
    splitString.push_back(std::string(token));
    token = strtok(NULL,delim.c_str());
  }
  return splitString;
}

std::vector< std::vector<float> > read_scale_file(std::string scalePath)
{
  std::vector<std::vector<float>> data;
	
  std::ifstream fin;
  fin.open(scalePath);

  std::string line;

  int nline = 0;
  while ( !fin.eof() )
    {
      if (nline == 2) break;
		
      fin >> line;

      std::vector<std::string> line_data = split(line,",");
      std::vector<float> float_data;
      for(std::string ld : line_data) float_data.push_back( std::stof(ld) );
      data.push_back( float_data );
		
      nline++;
    }

  return data;
}

EvalNN::EvalNN(std::string graphPath,std::string input_name,std::vector<std::string> outputs_name,std::string modelName,std::string scaleName)
{
  graphPath_    = graphPath;
  modelName_    = modelName;
  scaleName_    = scaleName;
	
  graphDef_     = tensorflow::loadGraphDef(graphPath_+"/"+modelName_);
  session_      = tensorflow::createSession(graphDef_);
  input_name_   = input_name;
  outputs_name_ = outputs_name;

  auto scale_data = read_scale_file(graphPath_+"/"+scaleName_);
  scale_min_ = scale_data[0];
  scale_max_ = scale_data[1];
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

  // check and print the output
  // std::cout << " -> " << outputs[0].matrix<float>()(0, 0) << std::endl << std::endl;
  std::vector<float> out(outputs.size());
  for (unsigned int o = 0; o < outputs.size(); ++o)
    out.at(o) = outputs.at(o).matrix<float>()(0, 0);

  return out;
}
