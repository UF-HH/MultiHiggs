#include "SubJet.h"
#include <iostream>
#include "BuildP4.h"

void SubJet::buildP4()
{
  p4_.BUILDP4(SubJet, nat_);
}
