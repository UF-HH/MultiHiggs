#include "EventShapeCalculator.h"
#include "Math/VectorUtil.h"
#include "TMatrixDSym.h"
#include "TMatrixDSymEigen.h"
#include "TVectorD.h"

#include <iostream>
#include <tuple>

EventShapeCalculator::EventShapeCalculator(const std::vector<Jet>& in_jets)
{
  jet_p4.clear();
  for (const Jet& j : in_jets) jet_p4.push_back( j.P4Regressed() );
}

void EventShapeCalculator::build_momentum_tensor()
{
  /*
    Calculate the momentum tensor for the jet collection passed at initialization

    Eigenvalues are sorted smallest to largest and are normalized so

    sum( w_i ) = 1
  */

  double a,b,c,d,e,f;
  a = b = c = d = e = f = 0;

  for (p4_t p4 : jet_p4)
    {
      float px = p4.px();
      float py = p4.py();
      float pz = p4.pz();
		
      a += px*px;
      b += py*py;
      c += pz*pz;

      d += px*py;
      e += px*pz;
      f += py*pz;
    }

  double m[9] = {
    a,d,e,
    d,b,f,
    e,f,c
  };

  TMatrixDSym tensor(3,m);
  TMatrixDSymEigen eigen(tensor);

  TVectorD eigenvalues = eigen.GetEigenValues();
  double trace = eigenvalues.Norm1();
	
  _eigenvalues.clear();
  for (int iw = 0; iw < 3; iw++) _eigenvalues.push_back( eigenvalues[iw]/trace );
  std::sort(_eigenvalues.begin(),_eigenvalues.end());
}

EventShapes EventShapeCalculator::get_sphericity_shapes()
{
  build_momentum_tensor();

  EventShapes shapes;
  shapes.sphericity = 1.5 * ( _eigenvalues[1] + _eigenvalues[0] );
  shapes.transverse_sphericity = 2 * _eigenvalues[1] / (_eigenvalues[2] + _eigenvalues[1]);
  shapes.aplanarity = 1.5 * _eigenvalues[0];

  return shapes;
}
