#ifndef SKIMUTILS_H
#define SKIMUTILS_H

/**
 ** class  : SkimUtils
 ** author : L. Cadamuro (UF)
 ** date   : 10/01/2018
 ** brief  : utilities for i/o of the skims
 **/

#include "TChain.h"
#include "TString.h"

#include "NanoAODTree.h"
#include "NormWeightTree.h"
#include "OutputTree.h"
#include "EventInfo.h"

#include <string>

namespace SkimUtils
{
  // open input txt file and append all the files it contains to TChain
  int appendFromFileList (TChain* chain, std::string filename);

  // copy the information contained in the EventInfo to the OutputTree, and call the Fill() command
  void fill_output_tree(OutputTree& ot, NanoAODTree& nat, EventInfo& ei);

  // initialises in OutputTree the same structure contained in NormWeightTree
  void init_gen_weights(OutputTree& ot, NormWeightTree& nwt);

  // copies in OutputTree the weights contained in NormWeightTree
  void copy_gen_weights(OutputTree& ot, NormWeightTree& nwt);
}

#endif
