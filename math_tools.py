"""Các mô hình hình học động Chương V, hoàn toàn chạy trong trình duyệt.

Mục đích học tập: quan sát, dự đoán, kiểm chứng. Không tự cho lời giải bài đang làm.
Không dùng GeoGebra, mạng ngoài hoặc gửi dữ liệu học sinh đi đâu.
"""
from __future__ import annotations

from math import pi, sqrt

MODEL_LABELS = {
    "circle_circle": "Bài 17 · Vị trí hai đường tròn",
    "line_circle": "Bài 16 · Đường thẳng và đường tròn",
    "arc_sector": "Bài 15 · Cung tròn và hình quạt",
    "chord": "Bài 14 · Dây cung và khoảng cách đến tâm",
    "point_circle": "Bài 13 · Điểm và đường tròn",
    "thales": "Bài 13 · Tam giác vuông và trung điểm cạnh huyền",
}
LESSON_DEFAULT = {
    "b13": "thales", "b14": "chord", "b15": "arc_sector",
    "b16": "line_circle", "b17": "circle_circle",
}


def classify_two_circles(R: float, r: float, d: float) -> tuple[str, str]:
    if min(R, r) <= 0 or d < 0:
        raise ValueError("Bán kính phải dương, khoảng cách tâm không âm.")
    eps = 1e-9
    if abs(d) < eps and abs(R - r) < eps:
        return "Trùng nhau", "Vô số điểm chung"
    if abs(d) < eps:
        return "Đồng tâm, không trùng nhau", "0 điểm chung"
    if d > R + r + eps:
        return "Ngoài nhau", "0 điểm chung"
    if abs(d - (R + r)) <= eps:
        return "Tiếp xúc ngoài", "1 điểm chung"
    if d < abs(R - r) - eps:
        return "Một đường tròn nằm trong đường tròn kia", "0 điểm chung"
    if abs(d - abs(R - r)) <= eps:
        return "Tiếp xúc trong", "1 điểm chung"
    return "Cắt nhau", "2 điểm chung"


def classify_line_circle(R: float, h: float) -> str:
    if R <= 0 or h < 0:
        raise ValueError("Bán kính phải dương, khoảng cách không âm")
    return "Cắt nhau (2 điểm)" if h < R else ("Tiếp xúc (1 điểm)" if h == R else "Không giao nhau")


def chord_length(R: float, distance: float) -> float:
    if R <= 0 or not 0 <= distance <= R:
        raise ValueError("Khoảng cách từ tâm đến dây phải thuộc [0, R]")
    return 2 * sqrt(R * R - distance * distance)


def sector_measure(R: float, angle: float) -> tuple[float, float]:
    if R <= 0 or not 0 <= angle <= 360:
        raise ValueError("Góc ở tâm thuộc [0, 360]")
    return pi * R * angle / 180, pi * R * R * angle / 360


def geometry_html(initial: str = "circle_circle") -> str:
    """HTML độc lập dùng trong st.components.v1.html (iframe), không kết nối internet."""
    if initial not in MODEL_LABELS:
        initial = "circle_circle"
    opts = "".join(
        f'<option value="{key}" {"selected" if key == initial else ""}>{label}</option>'
        for key, label in MODEL_LABELS.items()
    )
    template = r'''<!doctype html><html lang="vi"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<style>
:root{font-family:system-ui,-apple-system,sans-serif;color:#1b3658}*{box-sizing:border-box}
body{margin:0;padding:12px;background:#f7fbff}.shell{background:white;border:1px solid #dce6f3;border-radius:15px;padding:13px}
label{font-weight:600;font-size:13px}select{width:100%;border:1px solid #bdcfe1;border-radius:9px;padding:9px;background:white;color:#214e79}
.controls{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;margin:10px 0}.one{min-width:0;background:#f3f7ff;border-radius:9px;padding:8px}
.one input{width:100%;accent-color:#1875bb}.one .value{font-weight:bold;color:#095f99}.plot{width:100%;border:1px solid #edf2f8;border-radius:11px;background:#fbfdff;overflow:hidden}
svg{width:100%;height:255px}svg text{font-size:13px;fill:#263b52}#question{margin-top:9px;font-size:13px;line-height:1.5;color:#375a7c}
.result{padding:8px 10px;border-radius:9px;background:#eef8f5;color:#0d5d56;margin-top:7px;font-size:13px;min-height:35px}
.tog{display:flex;align-items:center;gap:8px;margin-top:10px;font-size:13px;font-weight:500}.tog input{accent-color:#1785b3}
small{font-size:12px;color:#657b91}
@media(max-width:570px){.controls{grid-template-columns:repeat(2,minmax(0,1fr))}svg{height:210px}body{padding:6px}.shell{padding:9px}}
</style></head><body><div class="shell"><label for="model">🔍 Chọn mô hình hình học</label>
<select id="model">__OPTIONS__</select><div class="controls" id="controls"></div>
<div class="plot"><svg id="drawing" viewBox="0 0 700 285" role="img" aria-label="Mô hình hình học thay đổi khi di chuyển thanh trượt"></svg></div>
<div id="question"></div>
<label class="tog"><input type="checkbox" id="reveal"/> Em đã dự đoán — hiển thị nhận xét để kiểm chứng</label>
<div class="result" id="result" aria-live="polite">Hãy quan sát và tự dự đoán trước khi mở nhận xét.</div>
<small>Đây là hình minh họa động cho kiến thức nền, không thay cho hình vẽ của đề riêng.</small>
</div>
<script>
const $=id=>document.getElementById(id);
const conf={
 circle_circle:[['R','Bán kính R',1,7,5],['r','Bán kính r',1,7,3],['d','Khoảng cách d',0,14,2]],
 line_circle:[['R','Bán kính R',1,7,5],['h','Khoảng cách h',0,10,5]],
 arc_sector:[['R','Bán kính R',1,7,4],['a','Góc ở tâm (°)',10,350,90]],
 chord:[['R','Bán kính R',1,7,5],['h','Khoảng cách OH',0,7,3]],
 point_circle:[['R','Bán kính R',1,7,5],['d','Khoảng cách OM',0,10,5]],
 thales:[['a','Vị trí điểm A (độ)',25,155,65]]};
const colors={blue:'#2377c2',teal:'#0a9b9a',orange:'#ef9b33'};
const fmt=x=>Number(x).toFixed(2).replace(/\.00$/,'').replace(/0$/,'').replace(/\.$/,'');
function circle(x,y,r,col,fill='none'){return `<circle cx="${x}" cy="${y}" r="${r}" stroke="${col}" stroke-width="3" fill="${fill}"/>`}
function dot(x,y,name){return `<circle cx="${x}" cy="${y}" r="4" fill="#183653"/><text x="${x+7}" y="${y-7}">${name}</text>`}
function line(x1,y1,x2,y2,col=colors.blue,stroke=2){return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="${stroke}"/>`}
function controls(){const key=$('model').value;$('controls').innerHTML='';conf[key].forEach(([id,label,min,max,value])=>{
 const wrap=document.createElement('div');wrap.className='one';wrap.innerHTML=`<label for="s_${id}">${label}: <span class="value" id="v_${id}">${value}</span></label><input id="s_${id}" type="range" min="${min}" max="${max}" step="1" value="${value}"/>`;
 $('controls').appendChild(wrap);$('s_'+id).addEventListener('input',render)});$('reveal').checked=false;render();}
function val(id){return Number($('s_'+id).value)}
function render(){const key=$('model').value;conf[key].forEach(c=>{$('v_'+c[0]).innerText=val(c[0])});
 let art='',result='',q='';
 if(key==='circle_circle'){
 const R=val('R'),r=val('r'),d=val('d'),low=Math.min(-R,d-r),high=Math.max(R,d+r);
 const scale=Math.min(26,560/Math.max(1,high-low),115/Math.max(R,r));const ox=350-scale*(low+high)/2,oy=142,ex=ox+d*scale;
 art+=line(50,oy,650,oy,'#d5dfe9',1)+circle(ox,oy,R*scale,colors.blue)+circle(ex,oy,r*scale,colors.teal)+dot(ox,oy,'O')+dot(ex,oy,d===0?'O′/O':'O′');
 if(d>0)art+=line(ox,oy,ex,oy,colors.orange,2);
 if(d===0 && R===r)result='Hai đường tròn trùng nhau: vô số điểm chung.';
 else if(d===0)result='Đồng tâm nhưng bán kính khác nhau: 0 điểm chung.';
 else if(d>R+r)result='Hai đường tròn ngoài nhau: 0 điểm chung.';
 else if(d===R+r)result='Hai đường tròn tiếp xúc ngoài: 1 điểm chung.';
 else if(d<Math.abs(R-r))result='Một đường tròn nằm trong đường tròn kia và không chạm: 0 điểm chung.';
 else if(d===Math.abs(R-r))result='Hai đường tròn tiếp xúc trong: 1 điểm chung.';
 else result='Hai đường tròn cắt nhau: 2 điểm chung.';
 q=`Em hãy dự đoán: khi d = ${d}, còn R = ${R}, r = ${r}, hai đường tròn có bao nhiêu điểm chung? So sánh d với |R−r| và R+r.`;
 }else if(key==='line_circle'){
 const R=val('R'),h=val('h'),sc=Math.min(25,110/Math.max(R,h,1)),x=350,y=116,ly=y+h*sc;
 art+=circle(x,y,R*sc,colors.blue)+line(45,ly,655,ly,colors.teal,3)+dot(x,y,'O')+dot(x,ly,'H')+line(x,y,x,ly,colors.orange,3);
 result=h<R?'Đường thẳng cắt đường tròn ở 2 điểm.':h===R?'Đường thẳng tiếp xúc với đường tròn ở 1 điểm.':'Đường thẳng không có điểm chung với đường tròn.';
 q=`Hãy quan sát khoảng cách OH = ${h} và bán kính R = ${R}. Em dự đoán có bao nhiêu điểm chung?`;
 }else if(key==='arc_sector'){
 const R=val('R'),a=val('a'),cx=350,cy=172,rad=108;
 const a0=0,a1=a*Math.PI/180,x1=cx+rad*Math.cos(a1),y1=cy-rad*Math.sin(a1);
 const large=a>180?1:0;
 art+=`<path d="M${cx} ${cy} L${cx+rad} ${cy} A${rad} ${rad} 0 ${large} 0 ${x1} ${y1} Z" fill="#d7eef6" stroke="${colors.teal}" stroke-width="2"/>`;
 art+=circle(cx,cy,rad,colors.blue)+line(cx,cy,cx+rad,cy,colors.orange)+line(cx,cy,x1,y1,colors.orange)+dot(cx,cy,'O');
 result=`Độ dài cung là πRα/180 = ${fmt(Math.PI*R*a/180)}; diện tích quạt là πR²α/360 = ${fmt(Math.PI*R*R*a/360)} (đơn vị tương ứng).`;
 q=`Em dự đoán độ dài cung và diện tích hình quạt thay đổi thế nào khi góc ở tâm tăng từ 10° đến ${a}°?`;
 }else if(key==='chord'){
 const R=val('R'),h=Math.min(val('h'),R),cx=350,cy=138,rad=113,y=cy+(h/R)*rad,xOff=Math.sqrt(Math.max(0,rad*rad-(y-cy)*(y-cy)));
 art+=circle(cx,cy,rad,colors.blue)+line(cx-xOff,y,cx+xOff,y,colors.teal,4)+line(cx,cy,cx,y,colors.orange,2)+dot(cx,cy,'O')+dot(cx,y,'H');
 result=`Độ dài dây là 2√(R²−OH²) = ${fmt(2*Math.sqrt(Math.max(0,R*R-h*h)))} (cùng đơn vị với R).`;
 q=`Khi OH tăng từ 0 đến ${h} mà bán kính vẫn là ${R}, dây cung dài hơn hay ngắn đi?`;
 }else if(key==='thales'){
 const a=val('a')*Math.PI/180,mx=350,my=171,rad=110,Ax=mx+rad*Math.cos(a),Ay=my-rad*Math.sin(a),Bx=mx-rad,Cx=mx+rad;
 art+=circle(mx,my,rad,colors.blue)+line(Bx,my,Cx,my,colors.orange,3);
 art+=line(Bx,my,Ax,Ay,colors.teal,3)+line(Cx,my,Ax,Ay,colors.teal,3)+line(mx,my,Ax,Ay,'#7b63c8',2);
 art+=dot(Bx,my,'B')+dot(Cx,my,'C')+dot(mx,my,'M')+dot(Ax,Ay,'A');
 result='Với A thuộc đường tròn đường kính BC, góc BAC = 90°. M là trung điểm BC, nên MA = MB = MC = BC/2.';
 q='Em hãy dự đoán: M là trung điểm đoạn nào? Khi A chạy trên nửa đường tròn, góc BAC có thay đổi không?';
 }else{
 const R=val('R'),d=val('d'),cx=345,cy=145,rad=R*17,mx=cx+d*17;
 art+=circle(cx,cy,rad,colors.blue)+line(cx,cy,mx,cy,colors.orange,2)+dot(cx,cy,'O')+dot(mx,cy,'M');
 result=d<R?'M nằm bên trong đường tròn (OM < R).':d===R?'M thuộc đường tròn (OM = R).':'M nằm ngoài đường tròn (OM > R).';
 q=`Với OM = ${d} và R = ${R}, điểm M ở trong, trên hay ngoài đường tròn?`;
 }
 $('drawing').innerHTML=art;$('question').textContent=q;
 $('result').textContent=$('reveal').checked?result:'Hãy quan sát và tự dự đoán trước khi mở nhận xét.';
}
$('model').addEventListener('change',controls);$('reveal').addEventListener('change',render);controls();
</script></body></html>'''
    return template.replace("__OPTIONS__", opts)
