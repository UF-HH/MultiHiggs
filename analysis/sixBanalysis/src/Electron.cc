#include "Electron.h"

#include "BuildP4.h"

void Electron::buildP4()
{
    p4_.BUILDP4(Electron, nat_);
}