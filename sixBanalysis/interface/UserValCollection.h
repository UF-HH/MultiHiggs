#ifndef USERVALCOLLECTION_H
#define USERVALCOLLECTION_H

/**
** class  : UserValCollection
** author : L. Cadamuro (UF)
** date   : 29/01/2018
** brief  : a class to store and index values of a type T to be used to create user branches in a outputTree
**/

#include <string>
#include <vector>
#include <memory>
#include <iostream>
#include <unordered_map>

template <class T>
class UserValCollection {

    public:
        UserValCollection(){};
        ~UserValCollection(){};

        // returns false if the value cannot be added, else true
        bool addVal (std::string name, T defaultVal);
        // throws a std::runtime_error exception if cannot access the value (e.g, not declared)
        T&   getVal    (std::string name);
        T*   getValPtr (std::string name);

        bool hasVal (std::string name) {return (names_vals_.find(name) != names_vals_.end());}

        // sets all the stored values to their default
        void resetAll();

    private:
        // the stored values - note: using shared ptr to be sure the allocated memory space doesn't change when copied
        std::vector<std::shared_ptr<T>>   stored_vals_;
        // the default values at clear()
        std::vector<T>   default_vals_;
        // the map that converts a name into the index of the previous vectors
        std::unordered_map<std::string, int> names_vals_;

};

template <class T>
bool UserValCollection<T>::addVal (std::string name, T defaultVal)
{
    // check if the branch exists
    if (names_vals_.find(name) != names_vals_.end()){
        // std::cout << "[WARNING] UserValCollection : addVal : value " << name << " was already defined, cannot create it again" << std::endl;
        return false;
    }

    std::shared_ptr<T> pp = std::make_shared<T> (defaultVal);
    stored_vals_.push_back(pp);
    default_vals_.push_back(defaultVal);
    names_vals_ [name] = stored_vals_.size() -1;
    return true;
}

template <class T>
T& UserValCollection<T>::getVal (std::string name)
{
    return *getValPtr(name);
}

template <class T>
T* UserValCollection<T>::getValPtr (std::string name)
{
    auto val = names_vals_.find(name);
    if (val == names_vals_.end())
        throw std::runtime_error("user value " + name + " not found");
    return (stored_vals_.at(val->second).get());
}

template <class T>
void UserValCollection<T>::resetAll()
{
    for (unsigned int i = 0; i < stored_vals_.size(); ++i)
        (*stored_vals_.at(i)) = default_vals_.at(i);
}


#endif