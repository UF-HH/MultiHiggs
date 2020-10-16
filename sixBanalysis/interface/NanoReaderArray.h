#ifndef NANOREADERARRAY_H
#define NANOREADERARRAY_H

/*
** class   : NanoReaderArray
** author  : L.Cadamuro (UF)
** date    : 31/01/2017
** brief   : encapsulates a TTreeReaderArray, and handles cases where the branch is not existing
*/

#include "TTreeReader.h"
#include "TTreeReaderArray.h"
#include <memory>
#include <iostream>

template <typename T>
class NanoReaderArray {
    public:
        NanoReaderArray (TTreeReader &tr, const char *branchname);
        ~NanoReaderArray(){}
        void Verify(TTree* tree);
        bool IsValid() {return (ttra_ ? true : false);}
        
        // just forwarding the TTreeReaderArray functions - the underlying unique_ptr will throw if not initialized
        // getting a default value does not make much sense for arrays
        T& At (size_t idx) {return ttra_->At(idx);}
        T& operator[] (size_t idx){return (*ttra_)[idx];} 
        auto  begin () {return ttra_->begin();}
        auto  end () const {return ttra_->end();}
        size_t GetSize() const { return ttra_->GetSize();}
    private:
        TTreeReader* reader_;
        std::string branchname_;
        std::unique_ptr<TTreeReaderArray<T>> ttra_;
};

template <typename T>
NanoReaderArray<T>::NanoReaderArray (TTreeReader &tr, const char *branchname)
{
    reader_ = &tr;
    branchname_ = branchname;
    this->Verify(tr.GetTree());
}

template <typename T>
void NanoReaderArray<T>::Verify(TTree* tree)
{
    // if (VERBOSE)
    //     std::cout << "NanoReaderArray :: I am verifying value : " << branchname_ << std::endl;

    if (tree->GetListOfBranches()->FindObject(branchname_.c_str())) {
        if (!ttra_) // not yet initialized
        {   
            ttra_ = std::unique_ptr<TTreeReaderArray<T>> (new TTreeReaderArray<T> (*reader_, branchname_.c_str()));
        }
    }

    else {
        if (ttra_) // branch disappeared, thus disable reader
            ttra_.release();
    }
}

#endif
