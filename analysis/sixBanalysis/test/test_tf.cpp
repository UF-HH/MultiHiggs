#include "EvalNN.h"

#include <iostream>
#include <string>
#include <vector>

using namespace std;

string vector_string(vector<float> array)
{
  string str = "[";
  for (float element : array) str += to_string(element)+" ";
  str += "]";
  return str;
}

int main() {

  string f_6j_classifier = "models/6jet_classifier/";

  cout << "[INFO] Testing Classifier: " << f_6j_classifier << endl;

  // tensorflow::GraphDef* graphDef = tensorflow::loadGraphDef(f_2j_classifier);
  EvalNN network(f_6j_classifier);
    
  vector<float> inputs = {120.153,  114.914,  75.994,  75.099,  61.896,  61.564, -0.525,
                          -0.278, -0.992,  0.311, -1.057, -1.844, -1.140,  1.660,  0.878,
                          2.717,  3.042, -1.256,  0.778,  0.700,  0.401,  0.996,  0.003,
                          0.996,  108.143,  124.577,  80.956,  79.714,  67.812,  42.099};
    
  vector<float> outputs = network.evaluate(inputs);

  cout << "[INPUT]: " << vector_string(inputs) << endl;
  cout << "[OUTPUT]:" << vector_string(outputs) << endl;
}
