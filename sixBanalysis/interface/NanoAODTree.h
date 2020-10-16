// Switch the implementation of the NanoAODReader and the corresponding trigger reader from one class to the other
// NOTE: you must ensure that the class you select has the interface and public members that are used in the rest of the code

#include "NanoAODTree_ReaderImpl.h"
#include "TriggerReader_ReaderImpl.h"
typedef NanoAODTree_ReaderImpl   NanoAODTree;
typedef TriggerReader_ReaderImpl TriggerReader;

// #include "NanoAODTree_SetBranchImpl.h"
// #include "TriggerReader_SetBranchImpl.h"
// typedef NanoAODTree_SetBranchImpl   NanoAODTree;
// typedef TriggerReader_SetBranchImpl TriggerReader;