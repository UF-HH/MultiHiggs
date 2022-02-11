#ifndef TORCHUTILS_H
#define TORCHUTILS_H

#include <iostream>
#include <vector>
#include <string>

#include <Eigen/Dense>


namespace TorchUtils
{
    Eigen::MatrixXf to_eigen(std::vector<std::vector<float>> data);
    void print_matrix(const Eigen::MatrixXf mat, std::string name = "array");
    void print_vector(const std::vector<float> vec, std::string name = "array");
    /**
     * @brief Compute the chi2 sum for all the elements
     *
     * @param true_mat matrix to reference
     * @param test matrix to test
     */
    void compare_matrix(const Eigen::MatrixXf true_mat, const Eigen::MatrixXf test);

    struct Layer
    {
        std::string name = "layer";
        Eigen::MatrixXf weights;
        Eigen::MatrixXf bias;

        void apply(Eigen::MatrixXf &x);
        void set_weights(std::vector<std::vector<float>> weights);
        void set_bias(std::vector<std::vector<float>> bias);
        void set_parameters(std::vector<std::vector<float>> weights, std::vector<std::vector<float>> bias);
        void print_parameters();
    };

    struct Linear : public Layer
    {
        int n_in;
        int n_out;

        /**
         * @brief Construct a new Linear object
         *
         * @param n number of input features
         * @param m number of output features
         */
        Linear(int n, int m);
        void apply(Eigen::MatrixXf &x);
    };

    struct ReLu : public Layer
    {
        void apply(Eigen::MatrixXf &x);
    };

    struct GCNConv
    {
        int n_in;
        int n_out;
        Linear *linear;
        ReLu relu;

        GCNConv(int n, int m);
        void apply(Eigen::MatrixXf &x, std::vector<std::vector<int>> &edge_index, Eigen::MatrixXf &edge_attr);
        Eigen::MatrixXf message(Eigen::MatrixXf &x, std::vector<std::vector<int>> &edge_index, Eigen::MatrixXf &edge_attr);
        void aggregate(Eigen::MatrixXf &x, std::vector<std::vector<int>> &edge_index, Eigen::MatrixXf &edge_attr, Eigen::MatrixXf &msg);
        void propagate(Eigen::MatrixXf &x, std::vector<std::vector<int>> &edge_index, Eigen::MatrixXf &edge_attr);

        void set_weights(std::vector<std::vector<float>> weights) { linear->set_weights(weights); }
        void set_bias(std::vector<std::vector<float>> bias) { linear->set_bias(bias); }
        void set_parameters(std::vector<std::vector<float>> weights, std::vector<std::vector<float>> bias) { linear->set_parameters(weights, bias); }
        void print_parameters() { linear->print_parameters(); }
    };
}
#endif // TORHCUTILS_H