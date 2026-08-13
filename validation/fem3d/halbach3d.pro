Group {
  Air = Region[1000];
  Mag2000 = Region[2000];
  Mag2001 = Region[2001];
  Mag2002 = Region[2002];
  Mag2003 = Region[2003];
  Mag2004 = Region[2004];
  Mag2005 = Region[2005];
  Mag2006 = Region[2006];
  Mag2007 = Region[2007];
  Mag2008 = Region[2008];
  Mag2009 = Region[2009];
  Mag2010 = Region[2010];
  Mag2011 = Region[2011];
  Mag2012 = Region[2012];
  Mag2013 = Region[2013];
  Mag2014 = Region[2014];
  Mag2015 = Region[2015];
  Mag2016 = Region[2016];
  Mag2017 = Region[2017];
  Mag2018 = Region[2018];
  Mag2019 = Region[2019];
  Mag2020 = Region[2020];
  Mag2021 = Region[2021];
  Mag2022 = Region[2022];
  Mag2023 = Region[2023];
  Magnets = Region[{Mag2000, Mag2001, Mag2002, Mag2003, Mag2004, Mag2005, Mag2006, Mag2007, Mag2008, Mag2009, Mag2010, Mag2011, Mag2012, Mag2013, Mag2014, Mag2015, Mag2016, Mag2017, Mag2018, Mag2019, Mag2020, Mag2021, Mag2022, Mag2023}];
  Vol = Region[{Air, Magnets}];
  Outer = Region[3000];
}
Function {
  M[Mag2000] = Vector[6.431984e-11, 1.050423e+06, 0.000000e+00];
  M[Mag2001] = Vector[6.431984e-11, 1.050423e+06, 0.000000e+00];
  M[Mag2002] = Vector[-1.050423e+06, 1.286397e-10, 0.000000e+00];
  M[Mag2003] = Vector[1.050423e+06, 0.000000e+00, 0.000000e+00];
  M[Mag2004] = Vector[-1.929595e-10, -1.050423e+06, 0.000000e+00];
  M[Mag2005] = Vector[-1.929595e-10, -1.050423e+06, 0.000000e+00];
  M[Mag2006] = Vector[1.050423e+06, 0.000000e+00, 0.000000e+00];
  M[Mag2007] = Vector[-1.050423e+06, 1.286397e-10, 0.000000e+00];
  M[Mag2008] = Vector[6.431984e-11, 1.050423e+06, 0.000000e+00];
  M[Mag2009] = Vector[6.431984e-11, 1.050423e+06, 0.000000e+00];
  M[Mag2010] = Vector[-1.050423e+06, 1.286397e-10, 0.000000e+00];
  M[Mag2011] = Vector[1.050423e+06, 0.000000e+00, 0.000000e+00];
  M[Mag2012] = Vector[-1.929595e-10, -1.050423e+06, 0.000000e+00];
  M[Mag2013] = Vector[-1.929595e-10, -1.050423e+06, 0.000000e+00];
  M[Mag2014] = Vector[1.050423e+06, 0.000000e+00, 0.000000e+00];
  M[Mag2015] = Vector[-1.050423e+06, 1.286397e-10, 0.000000e+00];
  M[Mag2016] = Vector[6.431984e-11, 1.050423e+06, 0.000000e+00];
  M[Mag2017] = Vector[6.431984e-11, 1.050423e+06, 0.000000e+00];
  M[Mag2018] = Vector[-1.050423e+06, 1.286397e-10, 0.000000e+00];
  M[Mag2019] = Vector[1.050423e+06, 0.000000e+00, 0.000000e+00];
  M[Mag2020] = Vector[-1.929595e-10, -1.050423e+06, 0.000000e+00];
  M[Mag2021] = Vector[-1.929595e-10, -1.050423e+06, 0.000000e+00];
  M[Mag2022] = Vector[1.050423e+06, 0.000000e+00, 0.000000e+00];
  M[Mag2023] = Vector[-1.050423e+06, 1.286397e-10, 0.000000e+00];
  M[Air] = Vector[0., 0., 0.];
  mu0 = 4.e-7 * Pi;
}

Jacobian { { Name Vol; Case { { Region All; Jacobian Vol; } } } }
Integration { { Name I1; Case { { Type Gauss; Case {
  { GeoElement Tetrahedron; NumberOfPoints 4; }
  { GeoElement Triangle;    NumberOfPoints 3; } } } } } }

Constraint { { Name phiZero; Type Assign;
  Case { { Region Outer; Value 0.; } } } }

FunctionSpace {
  { Name Hphi; Type Form0;
    BasisFunction { { Name sn; NameOfCoef un; Function BF_Node;
                      Support Vol; Entity NodesOf[All]; } }
    Constraint { { NameOfCoef un; EntityType NodesOf; NameOfConstraint phiZero; } } }
}

Formulation {
  { Name Mag; Type FemEquation;
    Quantity { { Name phi; Type Local; NameOfSpace Hphi; } }
    Equation {
      Galerkin { [ Dof{d phi} , {d phi} ]; In Vol;
                 Jacobian Vol; Integration I1; }
      Galerkin { [ -M[] , {d phi} ]; In Magnets;
                 Jacobian Vol; Integration I1; }
    }
  }
}

Resolution {
  { Name Sol;
    System { { Name A; NameOfFormulation Mag; } }
    Operation { Generate[A]; Solve[A]; SaveSolution[A]; }
  }
}

PostProcessing {
  { Name Post; NameOfFormulation Mag;
    Quantity {
      { Name b; Value { Local { [ -mu0 * {d phi} + mu0 * M[] ]; In Vol;
                                Jacobian Vol; } } }
    }
  }
}

PostOperation {
  { Name Line; NameOfPostProcessing Post;
     Operation {
       Print[ b, OnLine { { -0.024000000, 0., 0. } { 0.024000000, 0., 0. } } {240},
              Format SimpleTable, File "b_midgap.txt" ];
     } }
}
