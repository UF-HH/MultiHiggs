#include "ParamsMap.h"

bool ParamsMap::has_section (std::string section){
    return (params_.find(section) != params_.end());
}

bool ParamsMap::has_param (std::string section, std::string name) {

    // check for section
    auto it_sec = params_.find(section);
    if (it_sec == params_.end()) // no section found
        return false;
    
    // check for name
    auto& section_params = it_sec->second;
    auto it_name = section_params.find(name);

    if (it_name == section_params.end())
        return false;
    
    return true;
}

// void ParamsMap::insert_section(std::string section){
//     if has_section(section)
//         throw (std::runtime_error(std::string("ParamsMap: section ") + section + std::string(" already exists, cannot insert")));
    
//     params_[section] = single_section_map_t();
// }

// single_section_map_t& ParamsMap::get_section(std::string section){
//     auto it = params_.find(name);
//     if (it == params_.end())
//         throw (std::runtime_error(std::string("ParamsMap: section ") + section + std::string(" does not exists, cannot get it")));
//     return it->second;
// }