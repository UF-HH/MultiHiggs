#ifndef BRANCH_COLLECTION_H
#define BRANCH_COLLECTION_H

/**
 * @file BranchCollection.h
 * @author Evan Koenig
 * @brief Template class for constructing a collection of branches from any class
 * @version 0.1
 * @date 2023-03-14
 * 
 */

#include <boost/optional.hpp>
#include <iostream>
#include "TString.h"
#include "TTree.h"

/**
 * @brief Registers all branches in collection with the variable name as a prefix
 * 
 */
#define REGISTER_BRANCH_COLLECTION(COLL) (COLL.Register(#COLL, tree_, branch_switches))

/**
 * @brief Checks first to see if attribute is to be saved to TTree
 * 
 */
#define CHECK_BRANCH(attr)                 \
  if (this->is_enabled(#attr)) {           \
    tree_->Branch(tag + "_" #attr, &attr); \
  }

/**
 * @brief Macro for defining constructors for BranchCollections
 * 
 */
#define DEF_BRANCH_COLLECTION(CLASSNAME) \
  CLASSNAME() : BranchCollection(){};    \
  CLASSNAME(std::vector<std::string> branches) : BranchCollection(branches){};

template <typename T>
class BranchCollection {
public:
  BranchCollection(){};
  BranchCollection(std::vector<std::string> branches_) : branches(branches_){};

  void Register(std::unique_ptr<TTree>& tree_) { Register(tree_, branch_switches); }

  virtual void Register(TString tag, std::unique_ptr<TTree>& tree_, std::map<std::string, bool>& branch_switches_) = 0;
  virtual void Clear() = 0;

  void FillOptional(boost::optional<T>& obj) {
    if (obj)
      this->Fill(obj.get());
  };
  virtual void Fill(const T&) = 0;

protected:
  std::vector<std::string> branches;
  std::map<std::string, bool> branch_switches;
  bool is_enabled(std::string opt, bool default_value = true) {
    auto search = branch_switches.find(opt);
    if (search == branch_switches.end()) {
      // If not found in switches check if any variables in branches
      if (branches.size() > 0) {
        // If so return if the variable is in branches
        return std::count(branches.begin(), branches.end(), opt);
      }

      return default_value;  // if no opt given, enabled by default
    }
    return search->second;  // otherwise, use the value of the option
  };
};

#endif  // BRANCH_COLLECTION_H
