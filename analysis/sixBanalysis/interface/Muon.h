#ifndef MUON_H
#define MUON_H

#include "Candidate.h"

class Muon : public Candidate
{
    public:
        Muon () : Candidate(){typeId_=13;}
        Muon (int idx, NanoAODTree* nat) : Candidate(idx, nat){typeId_=13; buildP4();}
        ~Muon(){};
        std::unique_ptr<Candidate> clone() const override{
        	Muon *clonedMuon = new Muon(this->getIdx(), this->getNanoAODTree());
        	clonedMuon->setP4(this->P4());
        	return std::unique_ptr<Muon> (clonedMuon);
        }
    private:
        void buildP4() override; 
};

#endif