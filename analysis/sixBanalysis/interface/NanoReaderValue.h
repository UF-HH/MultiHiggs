#ifndef NANOREADERVALUE_H
#define NANOREADERVALUE_H

/*
** class   : NanoReaderValue
** author  : L.Cadamuro (UF)
** date    : 28/12/2017
** brief   : encapsulates a TTreeReaderValue, and handles cases where the branch is not existing
*/

#include "TTreeReader.h"
#include "TTreeReaderValue.h"
#include <memory>
#include <iostream>

// #define VERBOSE false

//XYH stuff
class NanoReaderValueBase
{
    public:
        NanoReaderValueBase(){}
        ~NanoReaderValueBase(){}
        virtual void Verify(TTree* tree) = 0;
};
//XYH stuff

template <typename T> class NanoReaderValue : public NanoReaderValueBase
{
    public:
        NanoReaderValue(TTreeReader &tr, const char *branchname);
        ~NanoReaderValue(){}
        void Verify(TTree* tree);
        bool IsValid() {return (ttrv_ ? true : false);}
        T* Get          ();
        T& operator *   () {return *Get();}
        T* operator ->  () {return Get();}
        void SetReturnDefault(bool ret_do, T ret_val = T()) {do_return_default_ = ret_do; val_return_default_ = ret_val;}
        // if ret_do = true,  will return ret_val every time the reader is invalid, instead of throwing an exception.
        // if ret_do = false, the default value passed is ignored

    private:
        TTreeReader* reader_;
        std::string branchname_;
        std::unique_ptr<TTreeReaderValue<T>> ttrv_;
        bool do_return_default_;
        T    val_return_default_;

};

template <typename T>
T* NanoReaderValue<T>::Get()
{
    if (!IsValid()){
        if (do_return_default_)
            return &val_return_default_;
        else{
            std::cerr << "** NanoReaderValue::Get() : [ERROR] reader of branch " << branchname_
                      << " is currently not valid, aborting (you can use SetReturnDefault(true, T ret_val) to set a default return value)" << std::endl;
            throw std::runtime_error ("TTreeReaderValue not configured");
        }
    }
    return ttrv_->Get();
}

template <typename T>
NanoReaderValue<T>::NanoReaderValue(TTreeReader &tr, const char *branchname) : NanoReaderValueBase()
{
    reader_ = &tr;
    branchname_ = branchname;
    do_return_default_  = false;
    val_return_default_ = T();
    this->Verify(tr.GetTree());
}

template <typename T>
void NanoReaderValue<T>::Verify(TTree* tree)
{
    // if (VERBOSE)
    //     std::cout << "NanoReaderValue :: I am verifying value : " << branchname_ << std::endl;

    if (tree->GetListOfBranches()->FindObject(branchname_.c_str())) {
        if (!ttrv_) // not yet initialized
        {   
            ttrv_ = std::unique_ptr<TTreeReaderValue<T>> (new TTreeReaderValue<T> (*reader_, branchname_.c_str()));
        }
    }

    else {
        if (ttrv_) // branch disappeared, thus disable reader
            ttrv_.release();
        std::cout<<"** Warning - Branch " << branchname_ << " does not exist!\n";
    }
}

#endif