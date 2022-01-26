#ifndef BUILDP4_H
#define BUILDP4_H

/*
** class  : BuildP4.h
** author : L. Cadamuro (UF)
** date   : 30/12/2017
** brief  : a preprocessing macro to create a P4 given the name of the object used in the NanoAODTree
** note   : to be included only in implementations (.cc), NOT in headers (.h)
*/

#define BUILDP4(CLNAME, nat) SetCoordinates (				\
												nat -> CLNAME ## _pt   . At(this->getIdx()), \
												nat -> CLNAME ## _eta  . At(this->getIdx()), \
												nat -> CLNAME ## _phi  . At(this->getIdx()), \
												nat -> CLNAME ## _mass . At(this->getIdx()) \
												)

#define BUILDP4_MASS(CLNAME, nat, MASS) SetCoordinates (		\
											nat -> CLNAME ## _pt   . At(this->getIdx()), \
											nat -> CLNAME ## _eta  . At(this->getIdx()), \
											nat -> CLNAME ## _phi  . At(this->getIdx()), \
											MASS \
											)


#endif
