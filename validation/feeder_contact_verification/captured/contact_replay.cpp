// FCE09 diagnostic. Replays measured FCE08 rigid poses; does not integrate motion.
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
#include "chrono/collision/ChCollisionShapeConvexHull.h"
#include "chrono/collision/ChCollisionShapeBox.h"
#include "chrono/geometry/ChTriangleMeshConnected.h"
#include "chrono/geometry/ChTriangleMeshSoup.h"
using namespace chrono;
std::vector<std::string> fields(const std::string& s) {
    std::vector<std::string> a; std::istringstream in(s); std::string v;
    while (std::getline(in,v,'\t')) a.push_back(v); return a;
}
class Audit : public ChContactContainer::ReportContactCallback {
 public:
    int count=0; double minimum=1,maximum=-1;
    bool OnReportContact(const ChVector3d&,const ChVector3d&,const ChMatrix33<>&,
       double d,double,const ChVector3d&,const ChVector3d&,ChContactable*,ChContactable*,int) override {
        ++count; minimum=std::min(minimum,d); maximum=std::max(maximum,d);return true;
    }
};
int main(int argc,char**argv) {
    if(argc!=4) return 2;
    std::string dir=argv[1],mode=argv[3],line;
    std::ifstream poses(argv[2]);
    std::cout<<"time_s,representation,contact_count,min_distance_m,max_distance_m\n"<<std::setprecision(15);
    while(std::getline(poses,line)) {
        auto p=fields(line); if(p.size()!=15)return 3;
        ChSystemNSC sys;
        ChCollisionModel::SetDefaultSuggestedEnvelope(mode=="volumes"?5e-6:1e-4);
        ChCollisionModel::SetDefaultSuggestedMargin(mode=="volumes"?0:1e-5);
        sys.SetCollisionSystemType(ChCollisionSystem::Type::BULLET);
        ChCollisionSystemBullet::SetContactBreakingThreshold(1e-4);
        auto mat=chrono_types::make_shared<ChContactMaterialNSC>();
        std::ifstream manifest(dir+"/bodies.tsv");
        std::string row;
        while(std::getline(manifest,row)) {
            auto a=fields(row); if(a.size()!=13)return 4;
            bool payload=a[0]=="payload"; if(!payload&&a[0]!="fork_body")continue;
            auto b=chrono_types::make_shared<ChBody>(); b->SetName(a[0]);
            b->SetMass(std::stod(a[2]));b->SetInertiaXX(ChVector3d(std::stod(a[6]),std::stod(a[7]),std::stod(a[8])));
            b->SetInertiaXY(ChVector3d(std::stod(a[9]),std::stod(a[10]),std::stod(a[11])));
            b->SetPos(ChVector3d(std::stod(p[payload?1:8]),std::stod(p[payload?2:9]),std::stod(p[payload?3:10])));
            b->SetRot(ChQuaternion<>(std::stod(p[payload?4:11]),std::stod(p[payload?5:12]),std::stod(p[payload?6:13]),std::stod(p[payload?7:14])));
            std::istringstream files(a[12]);std::string file;
            while(std::getline(files,file,',')) {
                auto mesh=ChTriangleMeshConnected::CreateFromWavefrontFile(dir+"/"+file,false,false);
                if(!mesh)return 5; mesh->RepairDuplicateVertexes(1e-10);
                if(mode=="volumes"&&payload) {
                    auto soup=ChTriangleMeshSoup::CreateFromWavefrontFile(dir+"/"+file);
                    b->AddCollisionShape(chrono_types::make_shared<ChCollisionShapeTriangleMesh>(mat,soup,false,true,0.));
                } else if(mode=="volumes") {
                    auto lo=mesh->GetCoordsVertices()[0],hi=lo;
                    for(auto v:mesh->GetCoordsVertices()){lo=Vmin(lo,v);hi=Vmax(hi,v);}
                    b->AddCollisionShape(chrono_types::make_shared<ChCollisionShapeBox>(mat,hi-lo),ChFramed((hi+lo)*.5,QUNIT));
                } else if(payload&&mode!="mesh")
                    b->AddCollisionShape(chrono_types::make_shared<ChCollisionShapeConvexHull>(mat,mesh->GetCoordsVertices()));
                else b->AddCollisionShape(chrono_types::make_shared<ChCollisionShapeTriangleMesh>(mat,mesh,false,false,1e-5));
            }
            b->EnableCollision(true);b->GetCollisionModel()->SetFamily(payload?1:0);
            b->GetCollisionModel()->DisallowCollisionsWith(payload?1:0);sys.Add(b);
        }
        sys.Update();sys.ComputeCollisions();auto audit=chrono_types::make_shared<Audit>();sys.GetContactContainer()->ReportAllContacts(audit);
        std::cout<<p[0]<<','<<mode<<','<<audit->count<<','<<audit->minimum<<','<<audit->maximum<<'\n';
    }
}
