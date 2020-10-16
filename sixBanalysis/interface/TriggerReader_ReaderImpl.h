#ifndef TRIGGERREADER_READERIMPL_H
#define TRIGGERREADER_READERIMPL_H

/*
** class   : TriggerReader_ReaderImpl
** author  : L.Cadamuro (UF)
** date    : 28/12/2017
** brief   : interface to select and read trigger decision in NanoaOD
** note    : readers_ is a vector<unique_ptr<NanoReader>>, so that
**           readers_.at(i) returns a unique_ptr
**           *(readers_.at(i)) returns a NanoReader
**           *(*(readers_.at(i))) returns the true/false value
**           as syntax is very error-prone, a couple of helper functions to get the readers and the results directly are stored as private members
*/

#include "NanoReaderValue.h"
#include "TTreeReader.h"
#include <string>
#include <memory>
#include <map>

class TriggerReader_ReaderImpl{
    public:
        TriggerReader_ReaderImpl(TTreeReader* reader);
        ~TriggerReader_ReaderImpl(){};
        void addTrigger(std::string trgName);
        void setTriggers(std::vector<std::string> trgNames);
        std::vector<std::unique_ptr<NanoReaderValue<bool>>>& getRefToReadersPtrVector(){return readers_;}
        bool getTrgOr();
        bool getTrgResult(std::string trgName);
        std::vector<std::string> getTrgPassed();

    private:
        NanoReaderValue<bool>& getRefToReader(int idx) {return *(readers_.at(idx));}
        bool getTrgResult(int idx) {return *getRefToReader(idx);}

        std::vector<std::unique_ptr<NanoReaderValue<bool>>> readers_;
        std::map<std::string, int> name_to_idx_;
        TTreeReader* main_reader_;
};

#endif