/* Local browser verification; no external website or service required. */
const {chromium}=require('playwright');
const fs=require('fs');const path=require('path');const http=require('http');
const root=path.resolve(__dirname,'..');
const mime={'.html':'text/html','.css':'text/css','.js':'text/javascript','.svg':'image/svg+xml','.json':'application/json','.png':'image/png','.jpg':'image/jpeg','.mp4':'video/mp4','.webm':'video/webm','.vtt':'text/vtt'};
const server=http.createServer((req,res)=>{let name=decodeURIComponent(req.url.split('?')[0]);let f=path.resolve(root,'.'+name);if(!f.startsWith(root+path.sep)){res.writeHead(403);return res.end();}if(name.endsWith('/'))f=path.join(f,'index.html');fs.stat(f,(err,stat)=>{if(err||!stat.isFile()){res.writeHead(404);return res.end();}res.writeHead(200,{'Content-Type':mime[path.extname(f)]||'application/octet-stream','Content-Length':stat.size});fs.createReadStream(f).pipe(res);});});
(async()=>{
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const base='http://127.0.0.1:'+server.address().port;
const browser=await chromium.launch({executablePath:process.env.VOLLEY_CHROMIUM||'/workspace/volley-work/browser/chromium_headless_shell-1234/chrome-headless-shell-linux64/chrome-headless-shell',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
const evidence={viewports:[],errors:[],links:[],filmControls:[],contrast:[]};
const pages=['index.html','concept.html','evidence.html','feeder-analysis.html','orbital-analysis.html','orbit-explorer.html','films.html','docs.html','updates.html','accessibility.html',...['overview','custody','mission','methods'].flatMap(x=>[`film-${x}-transcript.html`,`film-${x}-storyboard.html`])];
for(const [width,height,label] of [[1440,1000,'desktop'],[768,1024,'tablet'],[375,812,'mobile']]){
 const context=await browser.newContext({viewport:{width,height}});const p=await context.newPage();p.on('pageerror',e=>evidence.errors.push(label+': '+e.message));
 for(const name of pages){
  await p.goto(base+'/'+name);await p.evaluate(()=>{document.querySelectorAll('img').forEach(i=>i.loading='eager')});
  await p.waitForFunction(()=>Array.from(document.images).every(i=>i.complete));
  const state=await p.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth+1,badImages:Array.from(document.images).filter(i=>!i.naturalWidth).map(i=>i.src),title:document.title,nav:document.querySelectorAll('nav a').length}));
  evidence.viewports.push({viewport:label,page:name,...state});
  if(state.overflow||state.badImages.length||state.nav!==6)throw new Error(JSON.stringify({label,name,state}));
  if(name==='index.html')await p.screenshot({path:path.join(__dirname,`site-${label}.png`),fullPage:true});
 }
 await context.close();
}
// Check every current local URL and fragment; retain archives separately.
for(const name of pages){const p=await browser.newPage();await p.goto(base+'/'+name);const urls=await p.locator('[href],[src]').evaluateAll(nodes=>nodes.map(n=>n.getAttribute('href')||n.getAttribute('src')).filter(Boolean));for(const url of urls){if(/^(https?:|mailto:|data:)/.test(url))continue;const resolved=new URL(url,base+'/'+name);const response=await fetch(resolved);if(response.status!==200)throw new Error(`${name}: ${url} returned ${response.status}`);if(resolved.hash&&resolved.pathname.endsWith('.html')){const text=await response.text();const id=decodeURIComponent(resolved.hash.slice(1));if(!text.includes(`id="${id}"`))throw new Error(`${name}: missing fragment ${url}`);}evidence.links.push({page:name,url,status:response.status});}await p.close();}
const p=await browser.newPage();await p.goto(base+'/films.html');evidence.filmControls=await p.locator('video').evaluateAll(vs=>vs.map(v=>({controls:v.controls,muted:v.muted,autoplay:v.autoplay,poster:!!v.poster,captions:v.querySelectorAll('track[kind="captions"]').length,sources:v.querySelectorAll('source').length})));if(evidence.filmControls.some(v=>!v.controls||!v.muted||v.autoplay||!v.poster||v.captions!==1||v.sources!==2))throw Error('Video controls/captions invariant failed');
await p.emulateMedia({reducedMotion:'reduce'});await p.reload();evidence.reducedMotion=await p.locator('.film').evaluateAll(f=>f.map(x=>({class:x.classList.contains('reduced'),videoHidden:getComputedStyle(x.querySelector('video')).display==='none',stillVisible:getComputedStyle(x.querySelector('.still-alternative')).display!=='none'})));if(evidence.reducedMotion.some(x=>!x.class||!x.videoHidden||!x.stillVisible))throw Error('Reduced motion invariant failed');await p.locator('.motion-override').first().click();if(await p.locator('.film').first().evaluate(f=>f.classList.contains('reduced')))throw Error('Explicit motion override failed');
// Native keyboard path and focus treatment.
await p.goto(base+'/index.html');await p.keyboard.press('Tab');evidence.firstKeyboardFocus=await p.evaluate(()=>document.activeElement.textContent);if(evidence.firstKeyboardFocus!=='Skip to content')throw Error('Skip link not first keyboard target');await p.keyboard.press('Enter');evidence.skipTarget=await p.evaluate(()=>location.hash);if(evidence.skipTarget!=='#main')throw Error('Skip target failed');
await p.goto(base+'/orbit-explorer.html');const before=await p.locator('output').textContent();await p.locator('input').fill('10');await p.locator('input').dispatchEvent('input');const after=await p.locator('output').textContent();evidence.trajectoryControlChanges=before!==after;if(!evidence.trajectoryControlChanges)throw Error('Source trajectory control failed');
// Direct playback verifies actual video decode, caption loading and metadata.
await p.goto(base+'/films.html');
for(let i=0;i<4;i++){const data=await p.locator('video').nth(i).evaluate(async v=>{v.preload='auto';v.load();await new Promise((ok,fail)=>{v.onloadedmetadata=ok;v.onerror=()=>fail(new Error('Video decode error'));});await v.play();await new Promise(ok=>setTimeout(ok,250));v.pause();return{duration:v.duration,videoWidth:v.videoWidth,videoHeight:v.videoHeight,captions:v.textTracks.length,playbackTime:v.currentTime}});evidence.filmControls[i].decoded=data;if(data.videoWidth!==1280||data.videoHeight!==720||data.playbackTime<=0)throw Error('Final video decode failed');}
function luminance(hex){return hex.match(/\w\w/g).map(x=>parseInt(x,16)/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4).reduce((s,x,i)=>s+x*[.2126,.7152,.0722][i],0)}
for(const [fg,bg] of [['f6f5f1','11161c'],['bcc3c9','11161c'],['bfe3cf','11161c'],['bcc3c9','191f26'],['f6f5f1','1b2525']]){let a=luminance(fg),b=luminance(bg);let ratio=(Math.max(a,b)+.05)/(Math.min(a,b)+.05);evidence.contrast.push({fg,bg,ratio});if(ratio<4.5)throw Error('Text contrast below 4.5');}
evidence.status='passed';evidence.currentPages=pages.length;evidence.network='Local HTTP only; all asset URLs local';fs.writeFileSync(path.join(__dirname,'SITE_QA.json'),JSON.stringify(evidence,null,2));console.log(JSON.stringify({status:'passed',pages:pages.length,viewportChecks:evidence.viewports.length,localLinks:evidence.links.length,reducedMotion:evidence.reducedMotion.length,videoDecodes:evidence.filmControls.map(v=>v.decoded)},null,2));await browser.close();server.close();
})().catch(e=>{console.error(e);server.close();process.exit(1)});
