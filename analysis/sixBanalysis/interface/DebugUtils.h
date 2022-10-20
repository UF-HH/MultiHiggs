#ifndef DEBUGUTILS_H
#define DEBUGUTILS_H

#include <string>
#include <vector>
#include <sstream>
#include <iostream>
#include "Candidate.h"
#include "Jet.h"

template <typename T>
std::string getObjDescr (const T& in, std::string pre="", int wfield=10) {
  std::ostringstream ss;
  ss << pre;
  ss << " .. pT = " << std::setw(wfield) << in.P4().Pt();
  ss << " .. eta = " << std::setw(wfield) << in.P4().Eta();
  ss << " .. phi = " << std::setw(wfield) << in.P4().Phi();
  ss << " .. m = " << std::setw(wfield) << in.P4().M();
  std::string s = ss.str();
  return s;
}

template <>
std::string getObjDescr (const Jet& in, std::string pre, int wfield) {
  std::ostringstream ss;
  ss << pre;
  ss << " .. pT = " << std::setw(wfield) << in.P4().Pt();
  ss << " .. eta = " << std::setw(wfield) << in.P4().Eta();
  ss << " .. phi = " << std::setw(wfield) << in.P4().Phi();
  ss << " .. m = " << std::setw(wfield) << in.P4().M();
  ss << " .. DeepJet = " << std::setw(wfield) << get_property (in, Jet_btagDeepFlavB);
  std::string s = ss.str();
  return s;
}


template <typename T>
void dumpObjColl (const std::vector<T>& in, std::string header="", int wfield=10) {
  std::cout << header << std::endl;
  std::cout << "..... collection size : " << in.size() << std::endl;
  for (const T& x : in)
    std::cout << getObjDescr(x, "--- ", wfield) << std::endl;
}

template <typename T>
void dump (const T& in, std::string header="", int wfield=10) {
  std::cout << in << " ";
}

template <typename T>
void dump (const std::vector<T>& in, std::string header="", int wfield=10) {
  for (const T&x :in)
    dump(x);
  std::cout << std::endl;
}

template <typename T>
void dumpVector(const std::vector<T>& in, std::string header="", int wfield=10) {
  std::cout << header << std::endl;
  std::cout << "..... collection size : " << in.size() << std::endl;
  dump(in);
  std::cout << std::endl;
}

#endif