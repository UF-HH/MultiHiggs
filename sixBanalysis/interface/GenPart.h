#ifndef GENPART_H
#define GENPART_H

#include "Candidate.h"
#include <map>

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

#endif