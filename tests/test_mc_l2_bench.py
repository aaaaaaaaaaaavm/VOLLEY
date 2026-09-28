"""Synthetic evaluator regression cases; no experimental measurements."""
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
from bench_acceptance import evaluate

class BenchEvidence(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        (self.root/'synthetic.txt').write_text('SYNTHETIC UNIT TEST FIXTURE; NOT MEASURED DATA')
        digest=hashlib.sha256((self.root/'synthetic.txt').read_bytes()).hexdigest()
        self.run_data=dict(article_serial='SYNTHETIC',source_commit='synthetic',drawing_revision='synthetic',
            configuration_id='SYNTHETIC',calibration_record='synthetic.txt',reviewer_release_record='synthetic.txt',
            shots=[dict(shot_id=i+1,measured_speed_m_s=1.99,predicted_speed_m_s=1.9876,
                expanded_uncertainty_m_s=.007,captured=True,configuration_id='SYNTHETIC',
                raw_file='synthetic.txt',raw_sha256=digest) for i in range(20)])
    def test_complete_synthetic_speed_record(self):
        self.assertTrue(evaluate(self.run_data,self.root)['speed_characterization_pass'])
    def test_missing_calibration_blocks(self):
        self.run_data['calibration_record']='missing'
        self.assertFalse(evaluate(self.run_data,self.root)['speed_characterization_pass'])
    def test_bad_uncertainty_or_capture_or_hash_blocks(self):
        for key,value in [('expanded_uncertainty_m_s',.014),('captured',False),('raw_sha256','wrong')]:
            old=self.run_data['shots'][0][key];self.run_data['shots'][0][key]=value
            self.assertFalse(evaluate(self.run_data,self.root)['speed_characterization_pass'])
            self.run_data['shots'][0][key]=old
    def test_nonfinite_and_duplicate_rejected(self):
        self.run_data['shots'][0]['measured_speed_m_s']=float('nan')
        self.assertFalse(evaluate(self.run_data,self.root)['speed_characterization_pass'])
        self.run_data['shots'][0]['measured_speed_m_s']=1.99
        self.run_data['shots'][1]['shot_id']=1
        self.assertFalse(evaluate(self.run_data,self.root)['speed_characterization_pass'])
    def test_outlier_not_discarded(self):
        self.run_data['shots'][19]['measured_speed_m_s']=2.5
        self.assertFalse(evaluate(self.run_data,self.root)['speed_characterization_pass'])
    def test_blank_and_malformed_rejected(self):
        self.assertFalse(evaluate({},self.root)['speed_characterization_pass'])
        self.run_data['shots'][0]=None
        self.assertFalse(evaluate(self.run_data,self.root)['speed_characterization_pass'])

if __name__=='__main__': unittest.main()
