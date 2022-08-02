#ifndef COMBINATORICS_H
#define COMBINATORICS_H

#include <iostream>
#include <vector>
#include <deque>
#include <algorithm>

/**
 * @brief Generate all unordered combinations of a list of integers
 * 
 * @param items list of intergers to make combinations of
 * @param k number of items in each combination
 * @return std::vector<std::vector<int>> of combinations 
 */
std::vector<std::vector<int>> combinations(const std::vector<int> items, int k);

/**
 * @brief Generate all unorder combinations of the range(items)
 * 
 * @param items number of items to make combinations of
 * @param k number of items in each combinations
 * @return std::vector<std::vector<int>>  of combinations 
 */
std::vector<std::vector<int>> combinations(int items, int k);

/**
 * @brief Generate all unordered groups of combinations in a list of intergers
 * 
 * @param items list of intergers to make combinations of
 * @param ks list of each group size
 * @return std::vector<std::vector<std::vector<int>>> of group combiations
 */
std::vector<std::vector<std::vector<int>>> combinations(const std::vector<int> items, std::deque<int> ks);


/**
 * @brief Generate all unordered groups of combinations in range(items)
 * 
 * @param items number of items to make combinations of
 * @param ks list of each group size
 * @return std::vector<std::vector<std::vector<int>>> of group combiations
 */
std::vector<std::vector<std::vector<int>>> combinations(int items, std::deque<int> ks);

std::vector<std::vector<std::vector<int>>> combinations(const std::vector<int> items, std::vector<int> ks_);
std::vector<std::vector<std::vector<int>>> combinations(int items, std::vector<int> ks_);

#endif // COMBINATORICS_H