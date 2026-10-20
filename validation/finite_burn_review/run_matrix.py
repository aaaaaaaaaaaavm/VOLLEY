from target import run
import json
cases=['4_spring_10kg','4_volley_3_6_10kg','12_spring_20kg','12_volley_3_6_20kg']
results=[]
for frac in [.2,.45]:
 for name in cases: results.append(run(name,frac))
for name in cases: results.append(run(name,.35,30.))
for name in ['12_spring_20kg','12_volley_3_6_20kg']: results.append(run(name,.35,60.,100.,30.))
print('MATRIX_FINISHED',len(results))
