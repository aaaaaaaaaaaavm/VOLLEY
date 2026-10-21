// Analytical plane-contact controls for the actual nine-cell payload geometry.
#include <fstream>
#include <iomanip>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include "chrono/physics/ChSystemNSC.h"
#include "chrono/physics/ChBody.h"
#include "chrono/physics/ChContactContainer.h"
#include "chrono/collision/bullet/ChCollisionSystemBullet.h"
#include "chrono/collision/ChCollisionShapeTriangleMesh.h"
#include "chrono/collision/ChCollisionShapeBox.h"
#include "chrono/geometry/ChTriangleMeshSoup.h"
using namespace chrono;
constexpr double U = 1000; // internal millimetres, kilograms, seconds; output SI

class Audit : public ChContactContainer::ReportContactCallback {
public:
  int count = 0;
  double minimum = 1;
  bool OnReportContact(const ChVector3d &, const ChVector3d &, const ChMatrix33<> &, double d,
                       double, const ChVector3d &, const ChVector3d &, ChContactable *,
                       ChContactable *, int) override {
    ++count;
    minimum = std::min(minimum, d);
    return true;
  }
};
int main(int argc, char **argv) {
  if (argc != 2)
    return 2;
  std::string dir = argv[1], line;
  std::ifstream manifest(dir + "/bodies.tsv");
  std::vector<std::string> a;
  while (std::getline(manifest, line)) {
    std::istringstream in(line);
    std::string v;
    std::vector<std::string> r;
    while (std::getline(in, v, '\t'))
      r.push_back(v);
    if (r[0] == "payload")
      a = r;
  }
  if (a.size() != 13)
    return 3;
  std::cout << "imposed_gap_m,contacts,minimum_distance_m,error_from_analytical_gap_m\n"
            << std::setprecision(15);
  for (double gap : {.0001, .00001, 0., -.00001, -.0001, -.0005, -.001}) {
    ChSystemNSC sys;
    sys.SetCollisionSystemType(ChCollisionSystem::Type::BULLET);
    ChCollisionModel::SetDefaultSuggestedEnvelope(5e-6 * U);
    ChCollisionModel::SetDefaultSuggestedMargin(0);
    auto mat = chrono_types::make_shared<ChContactMaterialNSC>();
    auto payload = chrono_types::make_shared<ChBody>();
    payload->SetMass(std::stod(a[2]));
    payload->SetInertiaXX(U * U * ChVector3d(std::stod(a[6]), std::stod(a[7]), std::stod(a[8])));
    payload->SetPos(U * ChVector3d(std::stod(a[3]), std::stod(a[4]), std::stod(a[5]) + gap));
    std::istringstream names(a[12]);
    std::string name;
    while (std::getline(names, name, ',')) {
      auto soup = ChTriangleMeshSoup::CreateFromWavefrontFile(dir + "/" + name);
      if (!soup)
        return 4;
      soup->Transform(VNULL, ChMatrix33<>(U));
      payload->AddCollisionShape(
          chrono_types::make_shared<ChCollisionShapeTriangleMesh>(mat, soup, false, true, 0.));
    }
    payload->EnableCollision(true);
    sys.Add(payload);
    auto floor = chrono_types::make_shared<ChBody>();
    floor->SetFixed(true);
    floor->SetPos(U * ChVector3d(std::stod(a[3]), std::stod(a[4]), .0126));
    floor->AddCollisionShape(chrono_types::make_shared<ChCollisionShapeBox>(
        mat, U * ChVector3d(2 * std::stod(a[3]) + .02, .12, .02)));
    floor->EnableCollision(true);
    sys.Add(floor);
    sys.Update();
    sys.ComputeCollisions();
    auto audit = chrono_types::make_shared<Audit>();
    sys.GetContactContainer()->ReportAllContacts(audit);
    std::cout << gap << ',' << audit->count << ',' << audit->minimum / U << ','
              << (audit->count ? audit->minimum / U - gap : 0) << '\n';
  }
}
