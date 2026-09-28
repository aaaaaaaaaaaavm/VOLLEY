"""Independent physical limits for the local cartridge and finite-burn studies."""
import json,math,sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import mission_cartridges as mc
import finite_burn_departure as fb

class ContinuationTests(unittest.TestCase):
    def test_mass_and_speed_from_independent_momentum(self):
        r=mc.size(2,.08)['nominal'];A=4.25;B=300
        kinetic=r['work_J'];v=math.sqrt(2*kinetic*(1/A+1/B))
        payload=B/(A+B)*v;host=-A/(A+B)*v
        retained=(B*host+.25*payload)/(B+.25)
        self.assertAlmostEqual(payload-retained,2,places=10)
        self.assertAlmostEqual(4*payload+(B+.25)*retained,0,places=10)
    def test_contact_and_original_latch_limits_are_effective(self):
        self.assertIn('CONTACT_NOT_POSITIVE_AT_EXIT',mc.evaluate(100,.02,.025,f=100)['rejections'])
        self.assertIn('REFERENCE_LATCH_LOAD',mc.size(5,.24)['nominal']['rejections'])
    def test_low_cartridge_cannot_inherit_twenty_mm_catcher(self):
        self.assertFalse(mc.size(.5,.02)['nominal']['catcher_model_valid'])
        self.assertTrue(mc.size(2,.08)['nominal']['catcher_model_valid'])
    def test_integrated_rocket_burn(self):
        z=np.array([1e7,0,0,0,314.]);r=fb.propagate(z,30,10,0,True,mu=0)
        mf=314-300/fb.VE
        self.assertAlmostEqual(r[4],mf,places=9)
        self.assertAlmostEqual(r[2],fb.VE*math.log(314/mf),places=8)
    def test_slew_uses_short_arc_and_acceleration(self):
        self.assertAlmostEqual(fb.slew(math.pi-.001,-math.pi+.001),2*math.sqrt(.002/fb.ACCEL),places=9)
        self.assertGreater(fb.slew(0,.1),.1/fb.RATE)
    def test_invalid_duration_rejected(self):
        with self.assertRaises(ValueError):fb.propagate(np.r_[fb.tt.initial(),314],-1)
    def test_fuel_consumption_and_release_momentum(self):
        d=json.loads(fb.OUT.read_text())
        for case in d['cases']:
            s=case['selected'];self.assertAlmostEqual(s['fuel_used_kg'],case['thrust_N']*(s['first_burn_s']+s['second_burn_s'])/fb.VE,places=7)
            self.assertLess(s['momentum_residual_kg_m_s'],1e-8)
            if s['accepted']:
                self.assertGreaterEqual(s['fuel_remaining_kg'],2)
                self.assertGreaterEqual(s['first_to_second_available_s'],s['first_to_second_required_s'])
    def test_no_silent_acceptance_of_low_thrust_misses(self):
        d=json.loads(fb.OUT.read_text())
        for c in d['cases']:
            if c['thrust_N']==1:self.assertFalse(c['selected']['accepted'])

if __name__=='__main__':unittest.main()
