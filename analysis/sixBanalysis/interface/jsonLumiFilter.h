#ifndef JSONLUMIFILTER_H
#define JSONLUMIFILTER_H

/*
** class  : jsonLumiFilter
** author : L. Cadamuro (UF)
** date   : 22/02/2018
** brief  : check if a run/lumi is in the data validation json
*/

#include <vector>
#include <string>
#include <unordered_map>

class jsonLumiFilter
{
    typedef std::pair <unsigned int, unsigned int> lumirange;

    public:
        jsonLumiFilter(){verbose_ = false;};
        jsonLumiFilter(std::string jsonfile) : jsonLumiFilter() {loadJSON(jsonfile);}
        ~jsonLumiFilter(){};
        void loadJSON(std::string jsonfile);
        bool isValid(unsigned int run, unsigned int lumi);
        void setVerbose(bool val) {verbose_ = val;}
        void dumpJSON();
    private:
        std::unordered_map<unsigned int, std::vector<lumirange>> mask_;
        bool verbose_;

};

#endif