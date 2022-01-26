#ifndef DEBUGUTILS_H
#define DEBUGUTILS_H

#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include "Candidate.h"
#include "Jet.h"

// TODO reimplement DebugUtils to work with new Skim_functions


template <typename T>
std::string getObjDescr (const T& in, std::string pre = "", int wfield = 10);

template <>
std::string getObjDescr (const Jet& in, std::string pre, int wfield);

template <typename T>
void dumpObjColl (const std::vector<T>& in, std::string header = "", int wfield = 10);

#endif