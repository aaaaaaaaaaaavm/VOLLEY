"""Draw the front-page functional allocation; no numerical performance is implied."""
from pathlib import Path
import html
ROOT=Path(__file__).resolve().parents[1]
def text(x,y,s,size=19,color='#c6d5e0',weight='400'):
 return f'<text x="{x}" y="{y}" fill="{color}" font-family="Arial, sans-serif" font-size="{size}" font-weight="{weight}">{html.escape(s)}</text>'
s=['<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="510" viewBox="0 0 1120 510" role="img" aria-labelledby="title desc">','<title id="title">VOLLEY: allocating spacecraft departure control</title><desc id="desc">A controlled host supplies orbital state and services. A deployment system supplies relative impulse and release timing. A separated spacecraft inherits the resulting initial state. Retention, host recovery and disposal resources span the campaign.</desc>','<rect width="1120" height="510" rx="16" fill="#0c1823"/>',text(40,51,'VOLLEY / DEPARTURE CONTROL',17,'#71d5c2','700'),text(40,93,'One mission. Three responsibilities.',32,'#ffffff','700')]
for x,title,sub,lines in [(40,'ORBITAL HOST','Coarse placement',['Position + velocity','Attitude + navigation','Power + command authority']), (402,'DEPLOYMENT SYSTEM','Relative release condition',['Impulse + release timing','Retention + guidance','Reaction loads to the host']), (764,'SPACECRAFT','Initial orbital state',['Independent trajectory','Declared payload interface','Onboard mission capability'])]:
 s += [f'<rect x="{x}" y="135" width="316" height="214" rx="10" fill="#152a3a" stroke="#355365"/>',text(x+20,170,title,16,'#71d5c2','700'),text(x+20,206,sub,19,'#fff','700')]
 for i,l in enumerate(lines):s.append(text(x+20,248+29*i,l,17))
for x in [362,724]:s.append(f'<path d="M{x} 238h32m-9-7 9 7-9 7" fill="none" stroke="#71d5c2" stroke-width="2"/>')
s += ['<path d="M60 376H1060" stroke="#355365"/>',text(40,418,'CAMPAIGN ACCOUNTING',16,'#71d5c2','700'),text(40,452,'Safe retention · host recovery · remaining payloads · resource and disposal reserves',20),text(40,485,'Functional concept only. Host services and controllable release authority are not established capabilities.',15,'#9eafb9'),'</svg>']
(ROOT/'docs/assets/departure_roles.svg').write_text('\n'.join(s)+'\n')
