#include "SubGenJetAK8.h"

#include "BuildP4.h"

void SubGenJetAK8::buildP4()
{
  p4_.BUILDP4(SubGenJetAK8, nat_);
}
