// Captura pública con Chrome DevTools Protocol. Sin cuentas ni cookies personales.
// Requiere Chrome temporal en --remote-debugging-port=9342 y Node 20 --experimental-websocket.
const fs = require('fs');
const path = require('path');
const root = __dirname;
const sites = [
  {id:'life',name:'Life.Church',region:'Mundo',url:'https://www.life.church/'},
  {id:'elevation',name:'Elevation Church',region:'Mundo',url:'https://www.elevationchurch.org/'},
  {id:'saddleback',name:'Saddleback Church',region:'Mundo',url:'https://saddleback.com/'},
  {id:'hillsong',name:'Hillsong Church',region:'Mundo',url:'https://hillsong.com/'},
  {id:'bethel',name:'Bethel Church',region:'Mundo',url:'https://www.bethel.com/'},
  {id:'passion',name:'Passion City Church',region:'Mundo',url:'https://passioncitychurch.com/'},
  {id:'ieb-cordoba',name:'Iglesia Evangélica Bautista de Córdoba',region:'Mundo',url:'https://iebcordoba.es/',providedURL:'https://www.iebcordoba.org/',identityNote:'Referencia confirmada por el cliente: Córdoba, España. Sustituye el portal argentino localizado provisionalmente.'},
  {id:'rey-jesus',name:'Iglesia El Rey Jesús',region:'Argentina',url:'https://iglesiaelreyjesus.com.ar/',providedURL:'https://elreyjesus.org.ar/',identityNote:'La portada identifica a Iglesia El Rey Jesús en José A. Cabrera 4656, Palermo. La denominación bautista de la lista original no se pudo confirmar.'},
  {id:'adoracion',name:'Iglesia Adoración',region:'Argentina',url:'https://iglesiaadoracion.org/'},
  {id:'centro-adoracion',name:'Centro de Adoración',region:'Argentina',url:'https://iglesiacda-2023.my.canva.site/oficial',providedURL:'https://centrodeadoracion.org/',identityNote:'Sitio de Centro de Adoración · Ministerio Altares, Villa Sarmiento. El nombre genérico de la lista original no permite asegurar que fuera la congregación inicialmente pretendida.'},
  {id:'rincon',name:'Iglesia Cristiana Evangélica Rincón',region:'Argentina',url:'https://iglesiarincon.org/'},
  {id:'missio',name:'Iglesia Cristiana Missio',region:'Argentina',url:'https://www.iglesiacristianamissio.com/',providedURL:'https://missio.com.ar/'}
];
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{
 const targets=await (await fetch(`http://127.0.0.1:${process.env.CDP_PORT||9342}/json`)).json();
 const target=targets.find(t=>t.type==='page');
 const ws=new WebSocket(target.webSocketDebuggerUrl);
 await new Promise(r=>ws.addEventListener('open',r,{once:true}));
 let next=0;const pending=new Map();let status=null;
 ws.addEventListener('message',e=>{const m=JSON.parse(e.data);if(m.id&&pending.has(m.id)){pending.get(m.id)(m);pending.delete(m.id)}if(m.method==='Network.responseReceived'&&m.params.type==='Document')status={status:m.params.response.status,url:m.params.response.url};});
 const call=(method,params={})=>new Promise(r=>{const id=++next;pending.set(id,r);ws.send(JSON.stringify({id,method,params}))});
 const run=async expression=>(await call('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true})).result?.result?.value;
 await call('Page.enable');await call('Runtime.enable');await call('Network.enable');
 const results=[];
 for(const site of sites.filter(x=>!process.env.CAPTURE_IDS||process.env.CAPTURE_IDS.split(',').includes(x.id))){
  try{
   await call('Emulation.setDeviceMetricsOverride',{width:1440,height:1000,deviceScaleFactor:1,mobile:false});
   status=null;
   const navigation=await Promise.race([call('Page.navigate',{url:site.url}),sleep(22000).then(()=>({timeout:true}))]);
   await sleep(navigation.errorText||navigation.result?.errorText?800:3800);
   const dismissal=await run(`(()=>{const button=[...document.querySelectorAll('button')].find(b=>/^(reject all|reject all cookies|decline all|rechazar todas|rechazar todo|deny|only necessary)$/i.test(b.innerText.trim()));if(button){const t=button.innerText;button.click();return t}return null})()`);
   await sleep(350);
   const observed=await run(`(()=>({title:document.title,url:location.href,text:document.body?.innerText.slice(0,22000)||'',headings:[...document.querySelectorAll('h1,h2,h3')].map(x=>x.innerText.trim()).filter(Boolean).slice(0,60),links:[...document.querySelectorAll('a[href]')].map(x=>({text:x.innerText.trim().slice(0,100),href:x.href})).filter(x=>/^https?:/.test(x.href)).slice(0,600),styles:{background:getComputedStyle(document.body).backgroundColor,font:getComputedStyle(document.body).fontFamily,headingFont:document.querySelector('h1')?getComputedStyle(document.querySelector('h1')).fontFamily:null},height:document.documentElement.scrollHeight}))()`);
   const failed=!!navigation.result?.errorText||!!navigation.timeout||!observed||observed.url.startsWith('chrome-error:')||/^(Access Denied|Just a moment|Privacy error)/i.test(observed.title)||/ERR_NAME_NOT_RESOLVED|ERR_CONNECTION|This site can.t be reached|No se puede acceder a este sitio/i.test(observed.text);
   const first=await call('Page.captureScreenshot',{format:'jpeg',quality:78,captureBeyondViewport:false});
   if(first.result?.data)fs.writeFileSync(path.join(root,'capturas',site.id+'-desktop.jpg'),Buffer.from(first.result.data,'base64'));
   if(!failed){
    await run(`new Promise(resolve=>{let y=0;const limit=Math.min(document.documentElement.scrollHeight,11000);const t=setInterval(()=>{y+=850;scrollTo(0,y);if(y>=limit){clearInterval(t);scrollTo(0,0);resolve(true)}},100)})`);
    await sleep(300);
    const metrics=await call('Page.getLayoutMetrics');
    const height=Math.min(11000,Math.ceil(metrics.result.cssContentSize.height));
    const full=await call('Page.captureScreenshot',{format:'jpeg',quality:65,captureBeyondViewport:true,clip:{x:0,y:0,width:1440,height,scale:1}});
    if(full.result?.data)fs.writeFileSync(path.join(root,'capturas',site.id+'-completa.jpg'),Buffer.from(full.result.data,'base64'));
    await call('Emulation.setDeviceMetricsOverride',{width:390,height:844,deviceScaleFactor:1,mobile:true});await sleep(450);
    await run('scrollTo(0,0)');
    const mobile=await call('Page.captureScreenshot',{format:'jpeg',quality:78,captureBeyondViewport:false});
    if(mobile.result?.data)fs.writeFileSync(path.join(root,'capturas',site.id+'-mobile.jpg'),Buffer.from(mobile.result.data,'base64'));
   }
   const record={...site,capturedAt:new Date().toISOString(),viewport:{width:1440,height:1000},available:!failed,navigationError:navigation.result?.errorText||navigation.timeout||null,response:status,dismissal,...observed};
   fs.writeFileSync(path.join(root,'datos',site.id+'.json'),JSON.stringify(record,null,2));
   results.push({id:site.id,available:record.available,title:record.title,url:record.url,status:status?.status,error:record.navigationError});
   console.log(JSON.stringify(results[results.length-1]));
  }catch(error){console.log(JSON.stringify({id:site.id,error:error.message}));}
 }
 fs.writeFileSync(path.join(root,'datos','capturas.json'),JSON.stringify(results,null,2));
 await call('Browser.close');ws.close();
})().catch(e=>{console.error(e);process.exit(1)});
