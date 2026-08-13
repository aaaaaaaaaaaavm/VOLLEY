"""Generate the getdp problem from magnetisation.json, so the FEM source terms cannot
diverge from the mesh they were written for.

Magnetostatic scalar potential. With no free currents, H = -grad(phi) and B = mu0*(H + M),
so div(B)=0 gives

    int grad(phi).grad(v) = int M.grad(v)          over the magnet regions only

and mu_r = 1 is used throughout, which is exactly what magpylib assumes -- the comparison
in A2 band 4 is therefore between two methods, not two material models.
"""
import json
import os

d = os.path.dirname(os.path.abspath(__file__))
cfg = json.load(open(os.path.join(d, "magnetisation.json")))
mags = cfg["mags"]
tags = sorted(int(t) for t in mags)

L = []
L.append("Group {")
L.append("  Air = Region[1000];")
for t in tags:
    L.append(f"  Mag{t} = Region[{t}];")
L.append("  Magnets = Region[{%s}];" % ", ".join(f"Mag{t}" for t in tags))
L.append("  Vol = Region[{Air, Magnets}];")
L.append("  Outer = Region[3000];")
L.append("}")
L.append("Function {")
for t in tags:
    m = mags[str(t)]["M"]
    L.append(f"  M[Mag{t}] = Vector[{m[0]:.6e}, {m[1]:.6e}, {m[2]:.6e}];")
L.append("  M[Air] = Vector[0., 0., 0.];")
L.append("  mu0 = 4.e-7 * Pi;")
L.append("}")
L.append("""
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
""")
open(os.path.join(d, "halbach3d.pro"), "w").write("\n".join(L))
print(f"wrote halbach3d.pro with {len(tags)} magnet regions")
