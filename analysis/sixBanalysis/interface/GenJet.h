#ifndef GENJET_H
#define GENJET_H

#include "Candidate.h"

class GenJet : public Candidate
{
    public:
        GenJet () : Candidate(){}
        GenJet (int idx, NanoAODTree* nat) : Candidate(idx, nat){buildP4();}
        ~GenJet(){};
        std::unique_ptr<Candidate> clone() const {
        	GenJet *clonedGenJet = new GenJet(this->getIdx(), this->getNanoAODTree());
        	clonedGenJet->setP4(this->P4());
        	return std::unique_ptr<GenJet> (clonedGenJet);
        }
    private:
        void buildP4(); 
};

#endif
