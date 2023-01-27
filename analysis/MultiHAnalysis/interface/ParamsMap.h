#ifndef PARAMSMAP_H
#define PARAMSMAP_H

/**
 ** class  : ParamsMap
 ** author : L. Cadamuro (UF)
 ** date   : 14/12/2021
 ** brief  : Class for storing generic parameters (std::any) to be passed to the sixB function to steer code execution
 **        : parameters are saved with a "section" and a "name" keyword, where a section is the set of parameters needed to a specific function
 **/

#include <any>
#include <string>
#include <unordered_map>
#include <utility>
#include <vector>
#include <iostream>
#include <type_traits>

// ----------------------------------------------------------------
// override the ostream operator to printout vectors
template <typename T>
std::ostream& operator<< (std::ostream& out, const std::vector<T>& v) {
    if ( !v.empty() ) {
        out << '[';
        for (auto x = v.begin(); x != v.end(); ++x){
            out << *x;
            if (std::distance(x, v.end()) > 1)
            out << ", ";
        }
        out << ']';
    }
    return out;
}    



class ParamsMap {
    public:
        typedef std::unordered_map<std::string, std::any> single_section_map_t;
        typedef std::unordered_map<std::string, single_section_map_t> params_map_t;

        // insert a param of type T. If the section does not exist, also create a new section
        template <typename T> void insert_param(std::string section, std::string name, T value, bool verbose = true);
        // // create a new empty section and return an iterator to it
        // void insert_section(std::string section);
        
        // get a parameter by section and name keys - throws an error if it does not exist
        template <typename T> T get_param(std::string section, std::string name);
        // get a reference to a section by its name - throws an error if a section does not exist
        // single_section_map_t& get_section(std::string section);

        // check if map contains a parameter
        bool has_param   (std::string section, std::string name);
        // check if map contains a section
        bool has_section (std::string section);


    private:
        params_map_t params_;

        // checks to verify if this is printable
        template <typename T, typename = void> struct has_output_operator : std::false_type {};
        template <typename T> struct has_output_operator<T, std::void_t<decltype(std::declval<std::ostream&>() << std::declval<T>())>> : std::true_type {};

};

// ----------------------------------------------------------------


template <typename T>
void ParamsMap::insert_param (std::string section, std::string name, T value, bool verbose)
{
    // try the insertion of a new section
    // if section does not exist, this will create a new section
    // otherwise, it will return an iterator to the element already found
    auto it_sec_exist = params_.insert(std::pair<std::string, single_section_map_t> (section, single_section_map_t()));
    
    // bool section_already_existed = it_sec_exist.second;
    // auto section_name = it_sec_exist.first->first;
    auto section_it   = it_sec_exist.first; // this is an iterator, i.e. a pair <key, value> (where the value is a reference1)

    // // now check if the section contains the parameter
    auto it_name = section_it->second.find(name);
    if (it_name != section_it->second.end()) // name already existed -> raise an error
        throw std::runtime_error(std::string("ParamsMap : section = " ) + section + std::string(" name = " ) + name + std::string(" already exist, cannot insert"));
    
    // screen printout
    if (verbose){
        if constexpr (has_output_operator<T>::value)
            std::cout << "... ParamsMap : inserting [" << section << "][" << name << "] --> " << value << std::endl;
        else
            std::cout << "... ParamsMap : inserting [" << section << "][" << name << "] --> " << "{not printable}" << std::endl;
    }
    section_it->second.insert(std::pair<std::string, T> (name, value));
}

template <typename T>
T ParamsMap::get_param (std::string section, std::string name)
{
    auto it_sec = params_.find(section);
    if (it_sec == params_.end())
        throw std::runtime_error(std::string("ParamsMap : section = ") + section + std::string(" does not exist, cannot get param"));
    auto it_name = it_sec->second.find(name);
    if (it_name == it_sec->second.end())
        throw std::runtime_error(std::string("ParamsMap : section = ") + section + std::string(" name = ") + name + std::string(" does not exist, cannot get param"));
    
    // if there is an error in type casting, capture it to make a more explanatory error message
    try {
        T ret = std::any_cast<T>(it_name->second);
        return ret;
    }
    catch (std::bad_any_cast& err){
        std::cout << std::string ("Type cast error when reading ParamMap section = ") + section + std::string(" name = ") + name << std::endl;
        throw err;
    }
}

#endif