#include "GenJet.h"

#include "BuildP4.h"

void GenJet::buildP4()
{
    p4_.BUILDP4(GenJet, nat_);
}
