#ifndef BUILD_CLASSIFIER_INPUT
#define BUILD_CLASSIFIER_INPUT

#include "Math/VectorUtil.h"
#include "Math/Vector3D.h"
#include "Math/Functions.h"

#include <iostream>
#include <tuple>
#include <algorithm>

#include "Jet.h"

std::vector<std::vector<int>> get_6jet_index_combos(int n,int r=6);

std::vector<float> build_6jet_classifier_input(std::vector<Jet> in_jets);

std::vector<float> build_6jet_classifier_input(const std::vector<Jet>& in_jets,const std::vector<int>& indices);

std::vector<float> build_3dijet_classifier_input(std::vector<Jet> in_jets);

std::vector<float> build_3dijet_classifier_input(const std::vector<Jet>& in_jets,const std::vector<int>& indices);

std::vector<float> build_2jet_classifier_input(std::vector<Jet> in_jets);

std::vector<float> build_2jet_classifier_input(const std::vector<Jet>& in_jets,const std::vector<int>& indices);

#endif
