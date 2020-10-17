#include "TriggerReader_ReaderImpl.h"

TriggerReader_ReaderImpl::TriggerReader_ReaderImpl(TTreeReader* reader) : main_reader_(reader)
{}

void TriggerReader_ReaderImpl::addTrigger(std::string trgName)
{
    // skip if name is in the trigger list
    if (name_to_idx_.find(trgName) != name_to_idx_.end())
    {
        std::cout << "** INFO: TriggerReader_ReaderImpl : trigger " << trgName << " is already set, skipping" << std::endl;
        return;
    }

    std::unique_ptr<NanoReaderValue<bool>> readr (new NanoReaderValue<bool>(*main_reader_, trgName.c_str()));
    readr->SetReturnDefault(true, false); // if branch does not exist, return false
    readers_.push_back(std::move(readr));
    name_to_idx_[trgName] = readers_.size()-1;
}

void TriggerReader_ReaderImpl::setTriggers(std::vector<std::string> trgNames)
{
    for (std::string& s : trgNames)
        addTrigger(s);
}

bool TriggerReader_ReaderImpl::getTrgOr()
{
    bool the_or = false;
    for (auto& rd_ptr : readers_)
        the_or = (the_or || (*(rd_ptr->Get())) );
    return the_or;
}

bool TriggerReader_ReaderImpl::getTrgResult(std::string trgName)
{
    if (name_to_idx_.find(trgName) == name_to_idx_.end())
    {
        std::cout << "** WARNING: TriggerReader_ReaderImpl : the requested trigger " << trgName << " was not declared, returning false" << std::endl;
        return false;
    }

    int idx = name_to_idx_[trgName];
    return getTrgResult(idx);
}

std::vector<std::string> TriggerReader_ReaderImpl::getTrgPassed()
{
    std::vector<std::string> listOfPassedTriggers;

    for(auto & trigger : name_to_idx_)
    {
        if(getTrgResult(trigger.first)) listOfPassedTriggers.emplace_back(trigger.first);    
    }

    return listOfPassedTriggers;
}


