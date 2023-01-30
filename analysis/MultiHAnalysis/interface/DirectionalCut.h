#ifndef DirectionalCut_h
#define DirectionalCut_h

#include <string>
#include <cmath>
#include "CfgParser.h"

template <typename T>
class DirectionalCut {
  enum DirectionalCutType {kGT, kGEQ, kLT, kLEQ, kEQ, kNEQ};
 
 public:
  
 DirectionalCut(CfgParser &config, const std::string& name)
   : fValue(config.readFloatOpt(name+std::string("Value"))) {
    std::string direction = config.readStringOpt(name+std::string("Direction"));
    if (direction == "EQ" || direction == "==") fCutDirection = kEQ;
    else if (direction == "NEQ" || direction == "!=") fCutDirection = kNEQ;
    else if (direction == "GT"  || direction == ">")  fCutDirection = kGT;
    else if (direction == "GEQ" || direction == ">=") fCutDirection = kGEQ;
    else if (direction == "LT"  || direction == "<")  fCutDirection = kLT;
    else if (direction == "LEQ" || direction == "<=") fCutDirection = kLEQ;
  }
  
 DirectionalCut(const std::string direction, const double value)
   : fValue(value) {
    if (direction == "EQ" || direction == "==") fCutDirection = kEQ;
    else if (direction == "NEQ" || direction == "!=") fCutDirection = kNEQ;
    else if (direction == "GT"  || direction == ">") fCutDirection = kGT;
    else if (direction == "GEQ" || direction == ">=") fCutDirection = kGEQ;
    else if (direction == "LT"  || direction == "<") fCutDirection =kLT;
    else if (direction == "LEQ" || direction == "<=") fCutDirection =kLEQ;
  }
  
  ~DirectionalCut() { }
  
  bool passedCut(const T testValue) const 
  {
    if (fCutDirection == kEQ)
      return std::fabs(testValue-fValue) < 0.0001;
    if (fCutDirection == kNEQ)
      return std::fabs(testValue-fValue) > 0.0001;
    if (fCutDirection == kGT)
      return (testValue > fValue);
    if (fCutDirection == kGEQ)
      return (testValue >= fValue);
    if (fCutDirection == kLT)
      return (testValue < fValue);
    if (fCutDirection == kLEQ)
      return (testValue <= fValue);
    return false; // never reached
  }
  
  T getCutValue(void) const{ return fValue;}
  DirectionalCutType getCutDirection(void) const{ return fCutDirection;}
  std::string getCutValueString(void) const{ return std::to_string(fValue); }
  std::string getCutDirectionString(void) const{
    if (fCutDirection == kEQ) return "==";
    else if (fCutDirection == kNEQ) return "!=";
    else if (fCutDirection == kGT) return ">";
    else if (fCutDirection == kGEQ) return ">=";
    else if (fCutDirection == kLT) return "<";
    else if (fCutDirection == kLEQ) return "<=";
    else return "Unknown";
  }
  
 private:
  T fValue;
  DirectionalCutType fCutDirection;
};

#endif



