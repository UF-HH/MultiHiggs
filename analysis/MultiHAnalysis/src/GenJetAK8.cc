#include "GenJetAK8.h"

#include "BuildP4.h"

void GenJetAK8::buildP4()
{
  p4_.BUILDP4(GenJetAK8, nat_);
}
