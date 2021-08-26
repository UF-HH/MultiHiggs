#ifndef EVENT_SHAPE_CALCULATOR_H
#define EVENT_SHAPE_CALCULATOR_H

#include "Jet.h"

#include "TMatrixDSym.h"
#include "TMatrixDSymEigen.h"

struct EventShapes {
  float sphericity = -999;
  float transverse_sphericity = -999;
  float aplanarity = -999;
};

class EventShapeCalculator{
public:
  EventShapeCalculator(const std::vector<Jet>& in_jets);
  EventShapes get_sphericity_shapes();
	
private:
  void build_momentum_tensor();

  std::vector<p4_t> jet_p4;
  std::vector<float> _eigenvalues;
};

#endif //EVENT_SHAPE_CALCULATOR_H
