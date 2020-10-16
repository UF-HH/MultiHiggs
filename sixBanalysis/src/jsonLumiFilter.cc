#include <iostream>
#include "jsonLumiFilter.h"
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>

using namespace std;
namespace pt = boost::property_tree;

void jsonLumiFilter::loadJSON(std::string jsonfile)
{
    pt::ptree root;

    // Load the json file in this ptree
    pt::read_json(jsonfile, root);
    auto all = root.get_child(""); // accesses base level of the tree

    std::vector<unsigned int> runs;
    for (pt::ptree::value_type &lumi : all)
        runs.push_back(std::stoul(lumi.first));

    if (verbose_)
        cout << "... JSON: read " << runs.size() << " runs" << endl;

    for (unsigned int run : runs)
    {
        
        if (mask_.find(run) != mask_.end())
            throw std::runtime_error("Malformed lumi mask JSON. Run number " + std::to_string(run) + " found twice");
        
        mask_[run] = std::vector<lumirange>(0); // and empty vector
        
        auto lumis = root.get_child(std::to_string(run));
        for (pt::ptree::value_type &lumipair : lumis) // all the single lumi intervals
        {
            if (lumipair.second.size() != 2)
               throw std::runtime_error("Malformed lumi mask JSON. Run number " + std::to_string(run) + " has a lumi interval with != 2 elements"); 
            
            // cout <<"RUN " << run << "[";
            // for (pt::ptree::value_type &ll : lumipair.second) // the lower and upper lumi boundaries
            // {
            //     cout << ll.second.data() << " ";
            // }
            // cout << "]" << endl;

            auto iter1 = lumipair.second.begin();
            auto iter2 = ++(lumipair.second.begin());
            lumirange lr = make_pair(
                iter1->second.get_value<unsigned int>(),
                iter2->second.get_value<unsigned int>()
            );

            // cout << lr.first << " " << lr.second << endl;
            mask_.at(run).push_back(lr);
        }
    }
}

bool jsonLumiFilter::isValid(unsigned int run, unsigned int lumi)
{
    auto ilumis = mask_.find(run);
    if (ilumis == mask_.end())
        return false;

    // NOTE: one can assume that the lumi ranges are ordered and make a wiser search
    // but checking on the 2016 JSON, each entry has at most 6 ranges, so it's probably efficient to make a simple scan

    for (auto& lrange : ilumis->second)
    {
        if (lumi >= lrange.first && lumi <= lrange.second)
            return true;
    }
    return false;
}

void jsonLumiFilter::dumpJSON()
{
    for (auto irun = mask_.begin(); irun != mask_.end(); ++irun)
    {
        auto& lranges = irun->second;
        cout << "RUN " << irun->first << " ";
        for (auto& lumipair : lranges)
        {
            cout << "[" << lumipair.first << ", " << lumipair.second << "] ";
        }
        cout << endl;
    }
}