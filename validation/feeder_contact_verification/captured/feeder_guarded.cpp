// FCE09 convex-payload contact study. FM06-R1 geometry is unchanged. SI units; external application for Project Chrono10.
// Rigid meshes come from the native CAD. Only payload-mechanism contacts enabled.
// Ideal prismatic guide constraints and sampled PD control are model assumptions.
#include <algorithm>
#include <cmath>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <map>
#include <sstream>
#include <string>
#include <vector>
#include "chrono/physics/ChSystemNSC.h"
#include "chrono/collision/bullet/ChCollisionSystemBullet.h"
#include "chrono/physics/ChBody.h"
#include "chrono/physics/ChBodyEasy.h"
#include "chrono/physics/ChContactContainer.h"
#include "chrono/physics/ChLinkMotorLinearForce.h"
#include "chrono/functions/ChFunctionConst.h"
#include "chrono/collision/ChCollisionShapeTriangleMesh.h"
#include "chrono/collision/ChCollisionShapeConvexHull.h"
#include "chrono/collision/ChCollisionShapeBox.h"
#include "chrono/geometry/ChTriangleMeshConnected.h"
#include "chrono/geometry/ChTriangleMeshSoup.h"
#include "chrono/solver/ChIterativeSolver.h"
using namespace chrono;
struct Row {std::string name,role,meshes; double mass;ChVector3d pos,ix,iy;};
std::vector<std::string> split(const std::string&s,char delim){std::vector<std::string>v;std::istringstream f(s);std::string t;while(std::getline(f,t,delim))v.push_back(t);return v;}
struct Drive {std::shared_ptr<ChLinkMotorLinearForce> motor;std::shared_ptr<ChFunctionConst> force;double cap,kp,kd,force_now=0;};
Drive drive(ChSystemNSC&sys,std::shared_ptr<ChBody>a,std::shared_ptr<ChBody>b,ChVector3d axis,double cap){
 Drive d;d.motor=chrono_types::make_shared<ChLinkMotorLinearForce>();
 auto rot=QuatFromVec2Vec(VECT_Z,axis);d.motor->Initialize(a,b,ChFramed(a->GetPos(),rot));sys.Add(d.motor);
 d.force=chrono_types::make_shared<ChFunctionConst>(0);d.motor->SetForceFunction(d.force);d.cap=cap;d.kp=1600*a->GetMass();d.kd=80*a->GetMass();return d;
}
void control(Drive&d,double x,double v,double bias=0){d.force_now=std::clamp(d.kp*(x-d.motor->GetMotorPos())+d.kd*(v-d.motor->GetMotorPosDt())+bias,-d.cap,d.cap);d.force->SetConstant(d.force_now);}
std::pair<double,double> ramp(double t,double t0,double T,double a,double b){double u=std::clamp((t-t0)/T,0.,1.);double q=u*u*u*(10+u*(-15+6*u));double dq=(t>t0&&t<t0+T)?30*u*u*(1-u)*(1-u)/T:0;return{a+(b-a)*q,(b-a)*dq};}
class ContactAudit:public ChContactContainer::ReportContactCallback {
 public:double minimum_distance=1.,maximum_pair_force=0.,current_time=0.,worst_time=0.;std::string worst_a,worst_b;ChVector3d worst_pA,worst_pB,worst_n;
 bool OnReportContact(const ChVector3d&pA,const ChVector3d&pB,const ChMatrix33<>&frame,double d,double,const ChVector3d&F,const ChVector3d&,ChContactable*A,ChContactable*B,int)override{if(d<minimum_distance){minimum_distance=d;worst_time=current_time;worst_pA=pA;worst_pB=pB;worst_n=frame.GetAxisX();worst_a=A->GetPhysicsItem()->GetName();worst_b=B->GetPhysicsItem()->GetName();}maximum_pair_force=std::max(maximum_pair_force,F.Length());return true;}
};
int main(int argc,char**argv){
 if(argc!=13&&argc!=14&&argc!=15){std::cerr<<"geometry_dir output_csv mass friction restitution gravity dt drive_cap drag_N yaw_deg iterations Tfeed\n";return 2;}
 std::string dir=argv[1],out=argv[2];double pmass=std::stod(argv[3]),mu=std::stod(argv[4]),e=std::stod(argv[5]),g=std::stod(argv[6]),dt=std::stod(argv[7]),cap=std::stod(argv[8]),drag=std::stod(argv[9]),yaw=std::stod(argv[10]);int iterations=std::stoi(argv[11]);double T=std::stod(argv[12]);double guard=argc==15?std::stod(argv[14])*.001:.0001;if(guard<0||guard>.0005)return 12;
 if(dt<=0||std::abs(std::round(.001/dt)-.001/dt)>1e-8||dt>.001)return 3;
 ChCollisionModel::SetDefaultSuggestedEnvelope(5e-6);ChCollisionModel::SetDefaultSuggestedMargin(0);
 ChSystemNSC sys;ChCollisionModel::SetDefaultSuggestedEnvelope(5e-6);ChCollisionModel::SetDefaultSuggestedMargin(0);sys.SetCollisionSystemType(ChCollisionSystem::Type::BULLET);ChCollisionSystemBullet::SetContactBreakingThreshold(1e-4);sys.SetGravitationalAcceleration(ChVector3d(0,0,-g));sys.SetSolverType(ChSolver::Type::PSOR);sys.GetSolver()->AsIterative()->SetMaxIterations(iterations);sys.GetSolver()->AsIterative()->SetTolerance(1e-10);sys.SetMaxPenetrationRecoverySpeed(.01);sys.SetMinBounceSpeed(.0001);
 auto mat=chrono_types::make_shared<ChContactMaterialNSC>();mat->SetFriction(mu);mat->SetRestitution(e);
 std::ifstream manifest(dir+"/bodies.tsv");if(!manifest)return 4;
 std::map<std::string,std::shared_ptr<ChBody>> bodies;std::string line;
 while(std::getline(manifest,line)){
  auto a=split(line,'\t');if(a.size()!=13)return 5;std::cerr<<"loading "<<a[0]<<"\n";
  auto body=chrono_types::make_shared<ChBody>();body->SetName(a[0]);double mass=std::stod(a[2]);double ratio=1;if(a[1]=="payload"){ratio=pmass/mass;mass=pmass;}
  body->SetMass(mass);body->SetPos(ChVector3d(std::stod(a[3]),std::stod(a[4]),std::stod(a[5])));body->SetInertiaXX(ratio*ChVector3d(std::stod(a[6]),std::stod(a[7]),std::stod(a[8])));body->SetInertiaXY(ratio*ChVector3d(std::stod(a[9]),std::stod(a[10]),std::stod(a[11])));
  bool fixed=a[1]=="fixed"&&a[0].rfind("receiver_lock_pin_",0)!=0;body->SetFixed(fixed);
  for(auto file:split(a[12],',')){
   if(file=="NONE")continue;
   auto mesh=ChTriangleMeshConnected::CreateFromWavefrontFile(dir+"/"+file,false,false);if(!mesh)return 6;
   mesh->RepairDuplicateVertexes(1e-10);
   if(a[1]=="payload") {auto soup=ChTriangleMeshSoup::CreateFromWavefrontFile(dir+"/"+file);body->AddCollisionShape(chrono_types::make_shared<ChCollisionShapeTriangleMesh>(mat,soup,false,true,0.));}
   else {auto lo=mesh->GetCoordsVertices()[0],hi=lo;for(auto v:mesh->GetCoordsVertices()){lo=Vmin(lo,v);hi=Vmax(hi,v);}body->AddCollisionShape(chrono_types::make_shared<ChCollisionShapeBox>(mat,hi-lo),ChFramed((hi+lo)*.5,QUNIT));}
  }
  body->EnableCollision(a[12]!="NONE"&&!(argc>=14&&std::string(argv[13])=="no_contact"));if(body->GetCollisionModel()){int family=a[1]=="payload"?1:0;body->GetCollisionModel()->SetFamily(family);for(int j=0;j<15;j++)if(j!=(family==1?0:1))body->GetCollisionModel()->DisallowCollisionsWith(j);}
  if(a[1]=="payload")body->SetRot(QuatFromAngleZ(yaw*CH_PI/180.));
  if(body->GetCollisionModel())std::cerr<<"tolerances "<<a[0]<<" envelope "<<body->GetCollisionModel()->GetEnvelope()<<" margin "<<body->GetCollisionModel()->GetSafeMargin()<<"\n";sys.Add(body);bodies[a[0]]=body;
 }
 if(argc>=14&&std::string(argv[13])=="snapshot"){
  for(auto n:{"fork_body","fork_front"})bodies.at(n)->SetPos(bodies.at(n)->GetPos()+ChVector3d(0,.1,0));
  sys.DoStepDynamics(1e-8);
  std::cerr<<"SNAPSHOT contacts "<<sys.ComputeCollisions()<<"\n";
  for(auto n:{"fork_body","payload"}){auto b=bodies.at(n);auto box=b->GetCollisionModel()->GetBoundingBox();std::cerr<<n<<" AABB "<<box.min.x()<<","<<box.min.y()<<","<<box.min.z()<<" -> "<<box.max.x()<<","<<box.max.y()<<","<<box.max.z()<<" contact "<<b->GetContactForce().Length()<<"\n";}
  return 0;
 }
 if(argc>=14&&std::string(argv[13])=="jam"){
  double L=bodies.at("payload")->GetPos().x()*2;auto obstruction=chrono_types::make_shared<ChBodyEasyBox>(L,.003,.1,2700,false,true,mat);obstruction->SetName("deliberate_transfer_obstruction");obstruction->SetFixed(true);obstruction->SetPos(ChVector3d(L/2,-.05,.0726));obstruction->GetCollisionModel()->SetFamily(0);for(int j=0;j<15;j++)if(j!=1)obstruction->GetCollisionModel()->DisallowCollisionsWith(j);sys.Add(obstruction);
 }
 auto ground=chrono_types::make_shared<ChBody>();ground->SetFixed(true);sys.Add(ground);
 auto payload=bodies.at("payload"),fork=bodies.at("fork_body"),front=bodies.at("fork_front"),receiver=bodies.at("sled_entry_bar");
 auto fd=drive(sys,fork,ground,VECT_Y,cap);auto fr=drive(sys,front,fork,VECT_Z,20.);auto rd=drive(sys,receiver,ground,VECT_Z,50.);auto p0=drive(sys,bodies.at("receiver_lock_pin_0"),ground,-VECT_X,5.);auto p1=drive(sys,bodies.at("receiver_lock_pin_1"),ground,-VECT_X,5.);
 fd.kp=1600*(fork->GetMass()+front->GetMass()+pmass);fd.kd=80*(fork->GetMass()+front->GetMass()+pmass);
 if(argc>=14&&std::string(argv[13])=="stuck_pin")p0.cap=0;
 std::cerr<<"all bodies and drives initialized; mass-scaled40rad/s critically damped PD,1ms control period\n";auto initial=payload->GetPos();auto acc=fork->AddAccumulator();double last=2*T+6.5;int steps=std::lround(last/dt),control_stride=std::lround(.001/dt),write_stride=std::max(1,int(std::lround(.01/dt)));
 std::ofstream f(out);f<<std::setprecision(12)<<"time_s,fork_m,fork_v_m_s,front_lift_m,receiver_close_m,payload_x_m,payload_y_m,payload_z_m,vx_m_s,vy_m_s,vz_m_s,qw,qx,qy,qz,wx_rad_s,wy_rad_s,wz_rad_s,feed_force_N,front_force_N,receiver_force_N,contact_fx_N,contact_fy_N,contact_fz_N,contacts,pin0_withdraw_m,pin1_withdraw_m,aborted,fork_x_m,fork_y_m,fork_z_m,front_y_m,front_z_m,fork_qw,fork_qx,fork_qy,fork_qz\n";
 f.flush();bool invalid=false;bool aborted=false;bool dock_checked=false;bool receiver_checked=false;bool pin_checked=false;auto audit=chrono_types::make_shared<ContactAudit>();ChVector3d impulse(0,0,0);double max_speed=0,max_spin=0,max_contact=0,max_feed=0,positive_work=0,negative_work=0,max_fork_offaxis=0,max_fork_rotation=0;auto fork_initial=fork->GetPos();int executed=0;
 for(int k=0;k<=steps;k++){
  double t=k*dt;if(k<5||k%1000==0)std::cerr<<"step "<<k<<"\n";
  if(k%control_stride==0){
   auto target=t<T+4.5?ramp(t,0,T,0,.201):ramp(t,T+4.5,T,.201,0);
   // Smoothed dry guide drag; an assumed load on the pusher, not payload contact.
   control(fd,target.first,target.second);
   auto pt=t<T+2?ramp(t,T+.5,.5,0,.012):ramp(t,T+2,.5,.012,0);control(p0,pt.first,pt.second);control(p1,pt.first,pt.second);
   auto rt=ramp(t,T+1,1.,0,.012);control(rd,rt.first,rt.second,g*receiver->GetMass());
   auto ft=ramp(t,T+2.5,2.,0,.012);control(fr,ft.first,ft.second,g*front->GetMass());
  }
  if(t>=T+1&&!dock_checked){dock_checked=true;auto p=payload->GetPos();double L=initial.x()*2;double ymin=1.,ymax=-1.;for(int sx:{-1,1})for(int sy:{-1,1})for(int sz:{-1,1}){auto c=p+payload->GetRot().Rotate(ChVector3d(sx*L/2,sy*.05,sz*.05));ymin=std::min(ymin,c.y());ymax=std::max(ymax,c.y());}bool dock=std::abs(fd.motor->GetMotorPos()-.201)<.0005&&ymin>=-.0005+guard&&ymax<=.103-guard&&p0.motor->GetMotorPos()>.0115&&p1.motor->GetMotorPos()>.0115;if(!dock){aborted=true;std::cerr<<"abort: transfer or pin withdrawal not confirmed\n";}}
  if(t>=T+2&&!receiver_checked){receiver_checked=true;if(rd.motor->GetMotorPos()<.0115){aborted=true;std::cerr<<"abort: receiver closure not confirmed\n";}}
  if(t>=T+2.5&&!pin_checked){pin_checked=true;if(std::abs(p0.motor->GetMotorPos())>.0005||std::abs(p1.motor->GetMotorPos())>.0005){aborted=true;std::cerr<<"abort: receiver lock insertion not confirmed\n";}}
  if(aborted){fd.force->SetConstant(0);fr.force->SetConstant(0);rd.force->SetConstant(0);p0.force->SetConstant(0);p1.force->SetConstant(0);break;}
  // The pusher contact decomposition is exact only inside this X/Z region.
  auto pc=payload->GetPos();double plen=initial.x()*2;for(int sx:{-1,1})for(int sy:{-1,1})for(int sz:{-1,1}){auto corner=pc+payload->GetRot().Rotate(ChVector3d(sx*plen/2,sy*.05,sz*.05));if(corner.x()<-.012||corner.x()>plen+.012||corner.z()<.014||corner.z()>.128)invalid=true;}
  if(invalid){std::cerr<<"outside verified pusher contact domain\n";break;}
  fork->EmptyAccumulator(acc);fork->AccumulateForce(acc,ChVector3d(0,-drag*std::tanh(fd.motor->GetMotorPosDt()/.01),0),fork->GetPos(),false);
  if(k%write_stride==0||k==steps){auto p=payload->GetPos();auto v=payload->GetPosDt();auto q=payload->GetRot();auto w=payload->GetAngVelParent();auto c=payload->GetContactForce();
   f<<t<<','<<fd.motor->GetMotorPos()<<','<<fd.motor->GetMotorPosDt()<<','<<fr.motor->GetMotorPos()<<','<<rd.motor->GetMotorPos()<<','<<p.x()<<','<<p.y()<<','<<p.z()<<','<<v.x()<<','<<v.y()<<','<<v.z()<<','<<q.e0()<<','<<q.e1()<<','<<q.e2()<<','<<q.e3()<<','<<w.x()<<','<<w.y()<<','<<w.z()<<','<<fd.force_now<<','<<fr.force_now<<','<<rd.force_now<<','<<c.x()<<','<<c.y()<<','<<c.z()<<','<<sys.GetNumContacts()<<','<<p0.motor->GetMotorPos()<<','<<p1.motor->GetMotorPos()<<','<<aborted<<','<<fork->GetPos().x()<<','<<fork->GetPos().y()<<','<<fork->GetPos().z()<<','<<front->GetPos().y()<<','<<front->GetPos().z()<<','<<fork->GetRot().e0()<<','<<fork->GetRot().e1()<<','<<fork->GetRot().e2()<<','<<fork->GetRot().e3()<<'\n';if(k==0)f.flush();
   if(!std::isfinite(p.x()+p.y()+p.z())||(p-initial).Length()>1.){invalid=true;break;}
  }
  if(k<steps){sys.DoStepDynamics(dt);executed++;
   auto cf=payload->GetContactForce();impulse+=cf*dt;max_contact=std::max(max_contact,cf.Length());max_speed=std::max(max_speed,payload->GetPosDt().Length());max_spin=std::max(max_spin,payload->GetAngVelParent().Length());max_feed=std::max(max_feed,std::abs(fd.force_now));
   for(auto d:{&fd,&fr,&rd,&p0,&p1}){double work=d->force->GetConstant()*d->motor->GetMotorPosDt()*dt;if(work>=0)positive_work+=work;else negative_work+=work;}
   max_fork_offaxis=std::max(max_fork_offaxis,std::hypot(fork->GetPos().x()-fork_initial.x(),fork->GetPos().z()-fork_initial.z()));max_fork_rotation=std::max(max_fork_rotation,2*std::acos(std::clamp(std::abs(fork->GetRot().e0()),0.,1.)));audit->current_time=sys.GetChTime();sys.GetContactContainer()->ReportAllContacts(audit);
  }
 }
 auto residual=pmass*payload->GetPosDt()-impulse-ChVector3d(0,0,-pmass*g*executed*dt);
 std::ofstream m(out+".metrics.json");m<<std::setprecision(15)<<"{\n\"native_version\":\""<<CHRONO_VERSION<<"\",\n\"steps\":"<<executed<<",\n\"final_time_s\":"<<sys.GetChTime()<<",\n\"outside_domain_or_nonfinite\":"<<(invalid?"true":"false")<<",\n\"sequence_aborted\":"<<(aborted?"true":"false")<<",\n\"maximum_payload_speed_m_s\":"<<max_speed<<",\n\"maximum_payload_spin_rad_s\":"<<max_spin<<",\n\"maximum_resultant_contact_force_N\":"<<max_contact<<",\n\"maximum_pair_contact_force_N\":"<<audit->maximum_pair_force<<",\n\"minimum_reported_contact_distance_m\":"<<audit->minimum_distance<<",\n\"maximum_feed_force_N\":"<<max_feed<<",\n\"positive_mechanical_motor_work_J\":"<<positive_work<<",\n\"negative_mechanical_motor_work_J\":"<<negative_work<<",\n\"maximum_fork_off_axis_m\":"<<max_fork_offaxis<<",\n\"maximum_fork_rotation_rad\":"<<max_fork_rotation<<",\n\"payload_momentum_balance_residual_N_s\":["<<residual.x()<<","<<residual.y()<<","<<residual.z()<<"],\n\"contact_impulse_N_s\":["<<impulse.x()<<","<<impulse.y()<<","<<impulse.z()<<"]\n}\n";
 std::cerr<<"WORST_CONTACT "<<audit->worst_time<<" "<<audit->minimum_distance<<" "<<audit->worst_a<<" "<<audit->worst_b<<" pA "<<audit->worst_pA.x()<<","<<audit->worst_pA.y()<<","<<audit->worst_pA.z()<<" pB "<<audit->worst_pB.x()<<","<<audit->worst_pB.y()<<","<<audit->worst_pB.z()<<" normal "<<audit->worst_n.x()<<","<<audit->worst_n.y()<<","<<audit->worst_n.z()<<"\n";
 std::cout<<"Chrono "<<CHRONO_VERSION<<"; native dynamics finished; numerical_divergence="<<invalid<<"; aborted="<<aborted<<"; final_time="<<sys.GetChTime()<<"\n";
 return invalid?10:(aborted?11:0);
}
