
#include <iostream>
#include <string>
#include <vector>

#include <Eigen/Dense>
#include <Eigen/Core>

#include "TorchUtils.h"

using namespace std;
using namespace Eigen;

const vector<vector<float>> test_x = {{0.1513, 0.1034, 0.4494, 0.4344, 0.9990},
                                      {0.0842, 0.0815, 0.4713, 0.3194, 0.9291},
                                      {0.0667, 0.0745, 0.5992, 0.8489, 1.0000},
                                      {0.0373, 0.0551, 0.5486, 0.1089, 0.9995},
                                      {0.0328, 0.0556, 0.4983, 0.7707, 0.6503},
                                      {0.0277, 0.0343, 0.3750, 0.9698, 0.9985},
                                      {0.0103, 0.0219, 0.6110, 0.9342, 0.4759},
                                      {0.0082, 0.0188, 0.6338, 0.7912, 0.0130},
                                      {0.0124, 0.0147, 0.3801, 0.3667, 0.7325},
                                      {0.0136, 0.0143, 0.3729, 0.8628, 0.0335}};

const vector<vector<int>> test_edge_index = {{0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2,
                                              3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 7, 7, 8},
                                             {1, 2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5, 6, 7, 8, 9, 3, 4, 5, 6, 7, 8, 9,
                                              4, 5, 6, 7, 8, 9, 5, 6, 7, 8, 9, 6, 7, 8, 9, 7, 8, 9, 8, 9, 9}};

const vector<vector<float>> test_edge_attr = {{0.0714},
                                              {0.2848},
                                              {0.2153},
                                              {0.2049},
                                              {0.2847},
                                              {0.3346},
                                              {0.2759},
                                              {0.0777},
                                              {0.2644},
                                              {0.3049},
                                              {0.1452},
                                              {0.2689},
                                              {0.2270},
                                              {0.2649},
                                              {0.3204},
                                              {0.0919},
                                              {0.2868},
                                              {0.1617},
                                              {0.1074},
                                              {0.2269},
                                              {0.0519},
                                              {0.0477},
                                              {0.3550},
                                              {0.2174},
                                              {0.2063},
                                              {0.1859},
                                              {0.1197},
                                              {0.2054},
                                              {0.2226},
                                              {0.2231},
                                              {0.1672},
                                              {0.1453},
                                              {0.1306},
                                              {0.2651},
                                              {0.1322},
                                              {0.2276},
                                              {0.2701},
                                              {0.2355},
                                              {0.0635},
                                              {0.0876},
                                              {0.3390},
                                              {0.2325},
                                              {0.3502},
                                              {0.2540},
                                              {0.2943}};

void test_Linear()
{
  vector<vector<float>> vec_x = test_x;
  MatrixXf x = TorchUtils::to_eigen(vec_x);
  vector<vector<float>> vec_edge_attr = test_edge_attr;
  MatrixXf edge_attr = TorchUtils::to_eigen(vec_edge_attr);
  vector<vector<int>> edge_index = test_edge_index;

  printf("Testing TorchUtils::Linear Layer...\n");
  TorchUtils::Linear linear(5, 2);
  linear.print_parameters();

  printf("Setting parameters...\n");
  linear.set_parameters({{-0.4911, 0.8553, 0.5390, 0.1936, 0.7807},
                         {-0.6773, -0.3715, 0.2942, 0.5200, 0.7096}},
                        {{0.2344, 0.3054}});
  linear.print_parameters();

  printf("Applying Linear layer on ...\n");
  TorchUtils::print_matrix(x, "org");

  vector<vector<float>> vec_exp_x = {{1.3548, 1.2315},
                                     {1.3040, 1.1821},
                                     {1.5334, 1.5598},
                                     {1.3603, 1.1869},
                                     {1.1914, 1.2713},
                                     {1.4196, 1.5970},
                                     {1.1299, 1.2935},
                                     {0.7515, 0.8999},
                                     {1.0887, 1.1138},
                                     {0.6342, 0.8730}};
  MatrixXf exp_x = TorchUtils::to_eigen(vec_exp_x);
  TorchUtils::print_matrix(exp_x, "exp");
  linear.apply(x);
  TorchUtils::print_matrix(x, "new");
  TorchUtils::compare_matrix(exp_x, x);

  printf("Finished Testing TorchUtils::Linear Layer\n");
}

void test_GCNConv()
{
  vector<vector<float>> vec_x = test_x;
  MatrixXf x = TorchUtils::to_eigen(vec_x);
  vector<vector<float>> vec_edge_attr = test_edge_attr;
  MatrixXf edge_attr = TorchUtils::to_eigen(vec_edge_attr);
  vector<vector<int>> edge_index = test_edge_index;

  printf("Testing TorchUtils::GCNConv Layer...\n");
  TorchUtils::GCNConv conv(5, 2);
  printf("Setting parameters...\n");
  conv.set_parameters({{-0.4911, 0.8553, 0.5390, 0.1936, 0.7807},
                       {-0.6773, -0.3715, 0.2942, 0.5200, 0.7096}},
                      {{0.2344, 0.3054}});
  conv.print_parameters();

  printf("Applying GCNConv layer on ...\n");
  TorchUtils::print_matrix(x, "org");
  vector<vector<float>> vec_exp_x = {{0.0000, 0.0000},
                                     {1.4262, 1.3029},
                                     {3.2485, 3.0033},
                                     {4.7145, 4.4956},
                                     {6.3401, 5.9479},
                                     {7.8357, 7.5234},
                                     {9.3076, 9.1727},
                                     {10.6312, 10.6599},
                                     {11.9820, 12.1591},
                                     {13.1018, 13.3042}};
  MatrixXf exp_x = TorchUtils::to_eigen(vec_exp_x);
  conv.apply(x, edge_index, edge_attr);
  TorchUtils::print_matrix(x, "new");
  TorchUtils::compare_matrix(exp_x, x);

  printf("Finished Testing TorchUtils::GCNConv Layer\n");
}

void test_Eigen()
{
  std::vector<std::vector<float>> x = test_x;
  MatrixXf mat_x = TorchUtils::to_eigen(x);
  TorchUtils::print_matrix(mat_x, "org");

  std::vector<std::vector<float>> w = {{-0.4911, 0.8553, 0.5390, 0.1936, 0.7807},
                                       {-0.6773, -0.3715, 0.2942, 0.5200, 0.7096}};
  MatrixXf mat_w = TorchUtils::to_eigen(w);
  TorchUtils::print_matrix(mat_w, "weights");

  std::vector<std::vector<float>> b = {{0.2344, 0.3054}};
  MatrixXf mat_b = TorchUtils::to_eigen(b);
  TorchUtils::print_matrix(mat_b, "bias");

  TorchUtils::print_matrix(mat_x * mat_w.transpose() + MatrixXf::Ones(mat_x.rows(), 1) * mat_b, "w*x+b");
}

void test_Slicing()
{
  vector<vector<float>> vec_x = test_x;
  MatrixXf x = TorchUtils::to_eigen(vec_x);
  vector<vector<float>> vec_edge_attr = test_edge_attr;
  MatrixXf edge_attr = TorchUtils::to_eigen(vec_edge_attr);
  vector<vector<int>> edge_index = test_edge_index;

  vector<int> rows = edge_index[0];
  MatrixXf x_j = x(rows, Eigen::placeholders::all);
  TorchUtils::print_matrix(x_j, "x_j");

  TorchUtils::print_matrix(edge_attr * MatrixXf::Ones(1, 5), "edge_attr");
}

void test_ScatterAdd()
{
  vector<vector<float>> vec_x = test_x;
  MatrixXf x = TorchUtils::to_eigen(vec_x);
  vector<vector<float>> vec_edge_attr = test_edge_attr;
  MatrixXf edge_attr = TorchUtils::to_eigen(vec_edge_attr);
  vector<vector<int>> edge_index = test_edge_index;

  vector<int> cols = edge_index[1];

  int n_edges = cols.size();
  int n_node_features = x.cols();
  MatrixXf out = MatrixXf::Zero(x.rows(), x.cols());
  for (int i = 0; i < n_edges; i++)
  {
    for (int j = 0; j < n_node_features; j++)
    {
      out(cols[i], j) += edge_attr(i, 0);
    }
  }
  TorchUtils::print_matrix(out);
}

int main()
{
  // test_Linear();
  test_GCNConv();
  // test_Eigen();
  // test_Slicing();
  // test_ScatterAdd();
}
