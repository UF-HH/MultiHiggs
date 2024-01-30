#ifndef GENPART_H
#define GENPART_H

#include "Candidate.h"
#include <map>
#include "BranchCollection.h"

class GenPart : public Candidate
{
public:
  GenPart () : Candidate(){typeId_=-1;}
  GenPart (int idx, NanoAODTree* nat) : Candidate(idx, nat){typeId_=-1; buildP4();}
  ~GenPart(){};
  std::unique_ptr<Candidate> clone() const override{
    GenPart *clonedGenPart = new GenPart(this->getIdx(), this->getNanoAODTree());
    clonedGenPart->setP4(this->P4());
    return std::unique_ptr<GenPart> (clonedGenPart);
  }

  // status flags
  bool isPrompt()                             {return checkBit(get_property((*this), GenPart_statusFlags), 0);}
  bool isDecayedLeptonHadron()                {return checkBit(get_property((*this), GenPart_statusFlags), 1);}
  bool isTauDecayProduct()                    {return checkBit(get_property((*this), GenPart_statusFlags), 2);}
  bool isPromptTauDecayProduct()              {return checkBit(get_property((*this), GenPart_statusFlags), 3);}
  bool isDirectTauDecayProduct()              {return checkBit(get_property((*this), GenPart_statusFlags), 4);}
  bool isDirectPromptTauDecayProduct()        {return checkBit(get_property((*this), GenPart_statusFlags), 5);}
  bool isDirectHadronDecayProduct()           {return checkBit(get_property((*this), GenPart_statusFlags), 6);}
  bool isHardProcess()                        {return checkBit(get_property((*this), GenPart_statusFlags), 7);}
  bool fromHardProcess()                      {return checkBit(get_property((*this), GenPart_statusFlags), 8);}
  bool isHardProcessTauDecayProduct()         {return checkBit(get_property((*this), GenPart_statusFlags), 9);}
  bool isDirectHardProcessTauDecayProduct()   {return checkBit(get_property((*this), GenPart_statusFlags), 10);}
  bool fromHardProcessBeforeFSR()             {return checkBit(get_property((*this), GenPart_statusFlags), 11);}
  bool isFirstCopy()                          {return checkBit(get_property((*this), GenPart_statusFlags), 12);}
  bool isLastCopy()                           {return checkBit(get_property((*this), GenPart_statusFlags), 13);}
  bool isLastCopyBeforeFSR()                  {return checkBit(get_property((*this), GenPart_statusFlags), 14);}

private:
  bool checkBit(int number, int bitpos) {return (number & (1 << bitpos));}
  void buildP4() override; 
  static const std::map<int, float> gen_mass_;
};

struct GenPartListCollection : public BranchCollection<std::vector<GenPart> >{
  std::vector<float> m;
  std::vector<float> pt;
  std::vector<float> eta;
  std::vector<float> phi;

  DEF_BRANCH_COLLECTION(GenPartListCollection);
  void Register(TString tag, std::unique_ptr<TTree>& tree_, std::map<std::string, bool>& branch_switches_) override;
  void Clear() override;
  void Fill(const std::vector<GenPart>& genparts) override;
};

struct GenPartCollection : public BranchCollection<GenPart> {
  float m;  
  float pt; 
  float eta;
  float phi;

  DEF_BRANCH_COLLECTION(GenPartCollection);
  void Register(TString tag, std::unique_ptr<TTree>& tree_, std::map<std::string, bool>& branch_switches_) override;
  void Clear() override;
  void Fill(const GenPart& part) override;
};

#endif
