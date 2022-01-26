#ifndef BASEOUTTREE_H
#define BASEOUTTREE_H

/**
 ** class  : BaseOutTree
 ** author : L. Cadamuro (UF)
 ** date   : 17/03/2021
 ** brief  : basic output tree class with userfloats and userints
 ** NOTE   : meant to be used for other derived classes that implement the needed variables
 **/

#include "TTree.h"
#include "UserValCollection.h"
#include <string>
#include <memory>

class BaseOutTree {
public:
  BaseOutTree(std::string name, std::string title, std::string clsLogName = "BaseOutTree");
  ~BaseOutTree(){}

  int fill()  {return tree_->Fill();}
  int write() {return tree_->Write();}
    
  // returns false if the branch could not be created, true if all ok
  // the second optional value specifies what the branch should be reset to at clear()
  bool declareUserIntBranch    (std::string name, int defaultClearValue = 0);
  bool declareUserFloatBranch  (std::string name, float defaultClearValue = 0.0);
  bool declareUserIntBranchList(std::vector<std::string> nameList, int defaultClearValue = 0);

  // throws an exception if the branch name was not declared
  int&   userInt   (std::string name) {return userInts_   . getVal(name);}
  float& userFloat (std::string name) {return userFloats_ . getVal(name);}

  // access the underlying TTree
  TTree* getTree() {return tree_.get();}

protected:
  std::unique_ptr<TTree> tree_;
  std::string clsLogName_; // name to appear in log messages

  // for user declared branches
  UserValCollection<float> userFloats_;
  UserValCollection<int>   userInts_;
};

#endif
