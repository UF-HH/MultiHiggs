#ifndef JET_H
#define JET_H

#include "Candidate.h"

class Jet : public Candidate
{
    public:
        Jet () : Candidate(){typeId_=1;}
        Jet (int idx, NanoAODTree* nat) : Candidate(idx, nat){
            typeId_=1;
            buildP4Regressed();
            buildP4(); 
        }
        ~Jet(){};
        std::unique_ptr<Candidate> clone() const override{
        	Jet *clonedJet = new Jet(this->getIdx(), this->getNanoAODTree());
        	clonedJet->setP4Regressed(this->P4Regressed());
            clonedJet->setP4(this->P4());
        	return std::unique_ptr<Jet> (clonedJet);
        }
        float getBregCorr();
        float getBregRes();
        p4_t P4Regressed() const      {return p4Regressed_;}
        void setP4Regressed( p4_t p4Regressed) {p4Regressed_ = p4Regressed;}
        
        p4_t p4Regressed_;
        void buildP4Regressed(); 

    private:
        void buildP4() override; 

};

#endif