#include "BaseOutTree.h"

using namespace std;

BaseOutTree::BaseOutTree(std::string name, std::string title, std::string clsLogName)
{
  tree_ = std::unique_ptr<TTree> (new TTree(name.c_str(), title.c_str()));
  clsLogName_ = clsLogName;
}

bool BaseOutTree::declareUserIntBranch (std::string name, int defaultClearValue)
{
  // check if the branch exists -- the check in the same collection is done by UserVal internally, but I have to do the cross-checks
  if (userFloats_.hasVal(name)){
    cout << "[WARNING] " << clsLogName_ << " : declareUserIntBranch : branch " << name << " was already found as a userFloat, cannot create it" << endl;
    return false;
  }
    
  if (!userInts_.addVal(name, defaultClearValue)){
    cout << "[WARNING] " << clsLogName_ << " : declareUserIntBranch : branch " << name << " was already found as a userInt, cannot create it" << endl;
    return false;
  }

  cout << "[INFO] " << clsLogName_ << " : creating userIntBranch " << name << " (" << defaultClearValue << ")" << endl;

  // set the branch
  tree_->Branch(name.c_str(), userInts_.getValPtr(name));
  return true;
}

bool BaseOutTree::declareUserFloatBranch (std::string name, float defaultClearValue)
{
  // check if the branch exists -- the check in the same collection is done by UserVal internally, but I have to do the cross-checks
  if (userInts_.hasVal(name)){
    cout << "[WARNING] " << clsLogName_ << " : declareUserFloatBranch : branch " << name << " was already found as a userInt, cannot create it" << endl;
    return false;
  }
    
  if (!userFloats_.addVal(name, defaultClearValue)){
    cout << "[WARNING] " << clsLogName_ << " : declareUserFloatBranch : branch " << name << " was already found as a userFloat, cannot create it" << endl;
    return false;
  }

  cout << "[INFO] " << clsLogName_ << " : creating userFloatBranch " << name << " (" << defaultClearValue << ")" << endl;

  // set the branch
  tree_->Branch(name.c_str(), userFloats_.getValPtr(name));
  return true;
}

bool BaseOutTree::declareUserIntBranchList(std::vector<std::string> nameList, int defaultClearValue)
{
  for(const auto& name : nameList)
    {
      bool success = declareUserIntBranch(name, defaultClearValue);
      if(!success) return false;
    }
  return true;
}
