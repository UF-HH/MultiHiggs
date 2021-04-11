#include "Muon.h"

#include "BuildP4.h"

void Muon::buildP4()
{
    p4_.BUILDP4(Muon, nat_);
}