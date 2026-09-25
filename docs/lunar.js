'use strict';
const $=id=>document.getElementById(id);
const modelCanvas=$('modelCanvas'),gl=modelCanvas.getContext('webgl',{antialias:true,preserveDrawingBuffer:true});let tilt=.45;
let program,positionLoc,colorLoc;
if(gl){
 const shader=(type,source)=>{const s=gl.createShader(type);gl.shaderSource(s,source);gl.compileShader(s);if(!gl.getShaderParameter(s,gl.COMPILE_STATUS))throw Error(gl.getShaderInfoLog(s));return s};
 program=gl.createProgram();gl.attachShader(program,shader(gl.VERTEX_SHADER,'attribute vec3 position;attribute vec3 color;varying vec3 vColor;void main(){gl_Position=vec4(position,1.0);vColor=color;}'));gl.attachShader(program,shader(gl.FRAGMENT_SHADER,'precision mediump float;varying vec3 vColor;void main(){gl_FragColor=vec4(vColor,1.0);}'));gl.linkProgram(program);if(!gl.getProgramParameter(program,gl.LINK_STATUS))throw Error(gl.getProgramInfoLog(program));gl.useProgram(program);positionLoc=gl.getAttribLocation(program,'position');colorLoc=gl.getAttribLocation(program,'color');gl.enable(gl.DEPTH_TEST);
}
const fallback=gl?null:modelCanvas.getContext('2d');
function drawModel(){
 const data=window.VOLLEY_MODELS[$('model').value];if(!data)return;
 const yaw=Number($('azimuth').value)*Math.PI/180,cy=Math.cos(yaw),sy=Math.sin(yaw),ct=Math.cos(tilt),st=Math.sin(tilt);
 const parts=data.filter(p=>$('payload').checked||p.role!=='payload');
 const project=v=>{const x=v[0]*cy-v[1]*sy,y=v[0]*sy+v[1]*cy;return [x,v[2]*ct-y*st,y*ct+v[2]*st]};
 const pp=parts.map(p=>({...p,v:p.vertices.map(project)})),all=pp.flatMap(p=>p.v);
 const lo=[0,1,2].map(i=>Math.min(...all.map(v=>v[i]))),hi=[0,1,2].map(i=>Math.max(...all.map(v=>v[i]))),scale=Math.min(980/(hi[0]-lo[0]),450/(hi[1]-lo[1]));
 const pos=[],col=[],wire=$('wire').checked;
 for(const p of pp){const color=[1,3,5].map(i=>parseInt(p.color.slice(i,i+2),16)/255);for(const ids of p.triangles){const v=ids.map(i=>p.v[i]),a=v[1].map((x,i)=>x-v[0][i]),b=v[2].map((x,i)=>x-v[0][i]),n=[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],norm=Math.hypot(...n),shade=.65+.35*Math.abs((n[0]*.25+n[1]*.65+n[2]*.72)/Math.max(norm,1e-12));for(const j of (wire?[0,1,1,2,2,0]:[0,1,2])){const q=v[j];pos.push((q[0]-(hi[0]+lo[0])/2)*scale/550,(q[1]-(hi[1]+lo[1])/2)*scale/290,-(q[2]-(hi[2]+lo[2])/2)*1.8/Math.max(hi[2]-lo[2],1));col.push(...color.map(c=>c*(wire?1:shade)))}}}
 if(!gl){
  if(!fallback)return;
  fallback.clearRect(0,0,1100,580);
  const stride=wire?6:9,faces=[];
  for(let i=0;i<pos.length;i+=stride){
   const points=[];let depth=0;
   for(let j=0;j<stride;j+=3){points.push([550+pos[i+j]*550,290-pos[i+j+1]*290]);depth+=pos[i+j+2]}
   faces.push({points,depth:depth/(stride/3),color:'rgb('+col.slice(i,i+3).map(c=>Math.round(c*255)).join(',')+')'});
  }
  // Painter ordering is a display fallback, not a clearance or interference test.
  faces.sort((a,b)=>b.depth-a.depth);
  for(const face of faces){fallback.beginPath();face.points.forEach((p,i)=>i?fallback.lineTo(...p):fallback.moveTo(...p));fallback.strokeStyle=face.color;fallback.fillStyle=face.color;if(wire)fallback.stroke();else{fallback.closePath();fallback.fill()}}
  return;
 }
 gl.viewport(0,0,1100,580);gl.clearColor(.047,.09,.13,1);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
 const upload=(location,data)=>{const buffer=gl.createBuffer();gl.bindBuffer(gl.ARRAY_BUFFER,buffer);gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(data),gl.STREAM_DRAW);gl.enableVertexAttribArray(location);gl.vertexAttribPointer(location,3,gl.FLOAT,false,0,0);return buffer};const a=upload(positionLoc,pos),b=upload(colorLoc,col);gl.drawArrays(wire?gl.LINES:gl.TRIANGLES,0,pos.length/3);gl.deleteBuffer(a);gl.deleteBuffer(b);
}
for(const id of ['model','azimuth','payload','wire'])$(id).addEventListener('input',drawModel);
$('reset').onclick=()=>{$('azimuth').value=35;tilt=.45;$('payload').checked=true;$('wire').checked=false;drawModel()};let drag=null;
modelCanvas.onpointerdown=e=>{drag={x:e.clientX,y:e.clientY,angle:Number($('azimuth').value),tilt};modelCanvas.setPointerCapture(e.pointerId)};
modelCanvas.onpointermove=e=>{if(!drag)return;$('azimuth').value=Math.max(-180,Math.min(180,drag.angle+(e.clientX-drag.x)*.45));tilt=Math.max(-1.2,Math.min(1.2,drag.tilt+(e.clientY-drag.y)*.007));drawModel()};modelCanvas.onpointerup=()=>drag=null;modelCanvas.onpointercancel=()=>drag=null;
function orbitCurve(el){let p=[];for(let i=0;i<=500;i++){const t=i/500*2*Math.PI,r=el.a_km*(1-el.e**2)/(1+el.e*Math.cos(t));p.push([r*Math.cos(t+el.omega_rad),r*Math.sin(t+el.omega_rad)])}return p}
function drawOrbit(){const D=window.VOLLEY_LUNAR,R=D.assumptions.moon_radius_km,ha=Number($('staging').value),apsis=$('apsis').value,u=Number($('speed').value);const c=D.releases.find(c=>c.staging_apo_km===ha&&c.apsis===apsis&&c.u_ms===u),base=D.releases.find(c=>c.staging_apo_km===ha&&c.apsis===apsis&&c.u_ms===0);
 const curves=[orbitCurve(base.payload),orbitCurve(c.payload),orbitCurve(c.host)],all=curves.flat(),minx=Math.min(-R,...all.map(p=>p[0])),maxx=Math.max(R,...all.map(p=>p[0])),maxy=Math.max(R,...all.map(p=>Math.abs(p[1]))),scale=Math.min(920/(maxx-minx),390/(2*maxy));const project=p=>[550+(p[0]-(minx+maxx)/2)*scale,260-p[1]*scale],ctx=$('orbitCanvas').getContext('2d');ctx.clearRect(0,0,1100,550);const moon=project([0,0]);ctx.fillStyle='#687d8c';ctx.beginPath();ctx.arc(...moon,R*scale,0,Math.PI*2);ctx.fill();const colors=['#6facdf','#f1ae52','#33d6b2'];curves.forEach((pts,i)=>{ctx.strokeStyle=colors[i];ctx.lineWidth=2;ctx.setLineDash(i===2?[3,5]:i===1?[10,5]:[]);ctx.beginPath();pts.map(project).forEach((p,j)=>j?ctx.lineTo(...p):ctx.moveTo(...p));ctx.stroke()});ctx.setLineDash([]);ctx.font='15px system-ui';['Staging','Payload','Host recoil'].forEach((s,i)=>{ctx.fillStyle=colors[i];ctx.fillText(s,35+i*145,32)});ctx.fillStyle='#b7c7d1';ctx.fillText('Moon-centered orbital plane · equal spatial scale · curves may overlap',35,520);const bar=10**Math.floor(Math.log10((maxx-minx)/5));ctx.strokeStyle='#b7c7d1';ctx.beginPath();ctx.moveTo(35,475);ctx.lineTo(35+bar*scale,475);ctx.stroke();ctx.fillText(bar.toLocaleString()+' km',35,500);
 $('orbitReadouts').innerHTML=`<div><b>${c.payload.peri_km.toFixed(2)} km</b><span>payload perilune altitude</span></div><div><b>${c.payload.apo_km.toFixed(2)} km</b><span>payload apolune altitude</span></div><div><b>${c.payload_dv_ms.toFixed(4)} m/s</b><span>payload inertial velocity increment</span></div><div><b>${c.host_dv_ms.toFixed(4)} m/s</b><span>signed host recoil along release axis</span></div>`;
}
for(const id of ['staging','apsis','speed'])$(id).addEventListener('input',drawOrbit);drawModel();drawOrbit();
