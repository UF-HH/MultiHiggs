#include "TorchUtils.h"

using namespace std;
using namespace Eigen;

Eigen::MatrixXf TorchUtils::to_eigen(std::vector<std::vector<float>> data)
{
    Eigen::MatrixXf eMatrix(data.size(), data[0].size());
    for (int i = 0; i < data.size(); ++i)
        eMatrix.row(i) = Eigen::VectorXf::Map(&data[i][0], data[0].size());
    return eMatrix;
}

void TorchUtils::print_matrix(const MatrixXf mat, string name)
{
    int n = mat.rows();
    int m = mat.cols();

    cout << name << "(" << n << "," << m << "): " << endl;
    cout << "--------------------" << endl;
    cout << mat << endl;
    cout << "--------------------" << endl << endl;
}

void TorchUtils::print_vector(const vector<float> vec, string name)
{
    int m = vec.size();
    cout << name << "(" << m << "): {" << endl;
    for (int j = 0; j < m; j++)
    {
        printf("%f,", vec[j]);
    }
    printf("\n}\n");
}

void TorchUtils::compare_matrix(const MatrixXf true_mat, const MatrixXf test)
{
    int m = true_mat.cols();
    int n = true_mat.rows();

    if (m != test.cols() || n != test.rows())
    {
        printf("Test matrix doesn't have the same size as the true matrix\n");
    }

    float compare = (true_mat - test).squaredNorm();
    printf("Matrix Element Comparison to True: %f\n", compare);
}

void TorchUtils::Layer::set_weights(vector<vector<float>> weights)
{
    int m = weights.size();
    int n = weights[0].size();

    int n_out = this->weights.cols();
    int n_in = this->weights.rows();
    if (n != n_in || m != n_out)
    {
        printf("Expected weights(%i,%i), but got weights(%i,%i)\n", n_out, n_in, m, n);
    }

    this->weights = to_eigen(weights);
}

void TorchUtils::Layer::set_bias(vector<vector<float>> bias)
{
    int m = bias.size();
    int n_out = this->bias.rows();
    if (m != n_out)
    {
        printf("Expected bias(%i), but got bias(%i)\n", n_out, m);
    }

    this->bias = to_eigen(bias);
}

void TorchUtils::Layer::set_parameters(vector<vector<float>> weights, vector<vector<float>> bias)
{
    set_weights(weights);
    set_bias(bias);
}

void TorchUtils::Layer::print_parameters()
{
    cout << "Layer: " << name << endl;
    print_matrix(weights, "--weights");
    print_matrix(bias, "--bias");
}

void TorchUtils::ReLu::apply(MatrixXf &x)
{
    int rows = x.rows();
    int cols = x.cols();
    for (int i = 0; i < rows; i++)
    {
        for (int j = 0; j < cols; j++)
        {
            if (x(i,j) < 0)
                x(i, j) = 0;
        }
    }
}

TorchUtils::Linear::Linear(int n, int m) : Layer()
{
    name = "linear";
    n_in = n;
    n_out = m;
    weights = MatrixXf(n, m);
    bias = MatrixXf(m, 1);
}

void TorchUtils::Linear::apply(MatrixXf &x)
{
    // Compute the Linear algebra for the transform
    x = x * weights.transpose() + MatrixXf::Ones(x.rows(), 1) * bias;
}

TorchUtils::GCNConv::GCNConv(int n, int m)
{
    linear = new Linear(n, m);
}

void TorchUtils::GCNConv::apply(Eigen::MatrixXf &x, vector<vector<int>> &edge_index, Eigen::MatrixXf &edge_attr)
{
    linear->apply(x);
    return propagate(x, edge_index, edge_attr);
}

Eigen::MatrixXf TorchUtils::GCNConv::message(Eigen::MatrixXf &x, vector<vector<int>> &edge_index, Eigen::MatrixXf &edge_attr)
{
    int n_features = x.cols();

    vector<int> rows = edge_index[0];
    MatrixXf x_j = x(rows,Eigen::placeholders::all);

    /**
     * @brief Message Implementation 1
     * Add edge attr to all features
     */
    MatrixXf msg = x_j + edge_attr * MatrixXf::Ones(1, n_features);
    relu.apply(msg);
    return msg;
}

void scatter_add(Eigen::MatrixXf &x, vector<vector<int>> &edge_index, Eigen::MatrixXf &msg)
{
    vector<int> cols = edge_index[1];

    int n_edges = cols.size();
    int n_node_features = x.cols();
    MatrixXf out = MatrixXf::Zero(x.rows(), x.cols());
    for (int i = 0; i < n_edges; i++)
    {
        for (int j = 0; j < n_node_features; j++)
        {
            out(cols[i], j) += msg(i, j);
        }
    }
    x = out;
}

void TorchUtils::GCNConv::aggregate(Eigen::MatrixXf &x, vector<vector<int>> &edge_index, Eigen::MatrixXf &edge_attr, Eigen::MatrixXf &msg)
{
    /**
     * @brief Currently using add aggregate function
     * TODO implement scatter max
     *
     */
    scatter_add(x, edge_index, msg);
}

void TorchUtils::GCNConv::propagate(Eigen::MatrixXf &x, vector<vector<int>> &edge_index, Eigen::MatrixXf &edge_attr)
{
    Eigen::MatrixXf msg = message(x, edge_index, edge_attr);
    aggregate(x, edge_index, edge_attr, msg);
}