#ifndef PUWEIGHTSREADER_H
#define PUWEIGHTSREADER_H

#include <tuple>
#include <string>
#include <vector>

class PUWeightsReader {
public:
  PUWeightsReader(){}
  ~PUWeightsReader(){}
  void init_data(
		 std::string filename,
		 std::string name_PU_w = "PUweights",
		 std::string name_PU_w_up = "PUweights_up",
		 std::string name_PU_w_do = "PUweights_downs"
		 );
  // nominal, up, down
  std::tuple<double, double, double> get_weight(double PU);

private:
  int find_bin(double v);

  std::vector<double> bin_edges_;
  std::vector<double> PU_w_;
  std::vector<double> PU_w_up_;
  std::vector<double> PU_w_do_;
};

#endif
