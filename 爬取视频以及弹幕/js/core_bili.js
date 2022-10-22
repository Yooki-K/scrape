
var rr = JSON.parse('{"nested":{"bilibili":{"nested":{"community":{"nested":{"service":{"nested":{"dm":{"nested":{"v1":{"nested":{"DmWebViewReply":{"fields":{"state":{"type":"int32","id":1},"text":{"type":"string","id":2},"textSide":{"type":"string","id":3},"dmSge":{"type":"DmSegConfig","id":4},"flag":{"type":"DanmakuFlagConfig","id":5},"specialDms":{"rule":"repeated","type":"string","id":6},"checkBox":{"type":"bool","id":7},"count":{"type":"int64","id":8},"commandDms":{"rule":"repeated","type":"CommandDm","id":9},"dmSetting":{"type":"DanmuWebPlayerConfig","id":10},"reportFilter":{"rule":"repeated","type":"string","id":11},"expressions":{"rule":"repeated","type":"Expressions","id":12},"postPanel":{"rule":"repeated","type":"PostPanel","id":13},"activityMetas":{"rule":"repeated","type":"string","id":14}}},"PostPanel":{"fields":{"start":{"type":"int64","id":1},"end":{"type":"int64","id":2},"priority":{"type":"int64","id":3},"bizId":{"type":"int64","id":4},"bizType":{"type":"PostPanelBizType","id":5},"clickButton":{"type":"ClickButton","id":6},"textInput":{"type":"TextInput","id":7},"checkBox":{"type":"CheckBox","id":8},"toast":{"type":"Toast","id":9}}},"ClickButton":{"fields":{"portraitText":{"rule":"repeated","type":"string","id":1},"landscapeText":{"rule":"repeated","type":"string","id":2},"portraitTextFocus":{"rule":"repeated","type":"string","id":3},"landscapeTextFocus":{"rule":"repeated","type":"string","id":4},"renderType":{"type":"RenderType","id":5},"show":{"type":"bool","id":6}}},"PostPanelBizType":{"values":{"PostPanelBizTypeNone":0,"PostPanelBizTypeEncourage":1,"PostPanelBizTypeFragClose":4,"PostPanelBizTypeColorDM":2}},"TextInput":{"fields":{"portraitPlaceholder":{"rule":"repeated","type":"string","id":1},"landscapePlaceholder":{"rule":"repeated","type":"string","id":2},"renderType":{"type":"RenderType","id":3},"placeholderPost":{"type":"bool","id":4},"show":{"type":"bool","id":5},"postStatus":{"type":"PostStatus","id":7}}},"PostStatus":{"values":{"PostStatusNormal":0,"PostStatusClosed":1}},"RenderType":{"values":{"RenderTypeNone":0,"RenderTypeSingle":1,"RenderTypeRotation":2}},"CheckBox":{"fields":{"text":{"type":"string","id":1},"type":{"type":"CheckboxType","id":2},"defaultValue":{"type":"bool","id":3},"show":{"type":"bool","id":4}}},"CheckboxType":{"values":{"CheckboxTypeNone":0,"CheckboxTypeEncourage":1}},"Toast":{"fields":{"text":{"type":"string","id":1},"duration":{"type":"int32","id":2},"show":{"type":"bool","id":3},"button":{"type":"Button","id":4}}},"Button":{"fields":{"text":{"type":"string","id":1},"action":{"type":"ToastFunctionType","id":2}}},"ToastFunctionType":{"values":{"ToastFunctionTypeNone":0,"ToastFunctionTypePostPanel":1}},"ToastBizType":{"values":{"ToastBizTypeNone":0,"ToastBizTypeEncourage":1}},"CommandDm":{"fields":{"oid":{"type":"int64","id":2},"mid":{"type":"int64","id":3},"command":{"type":"string","id":4},"content":{"type":"string","id":5},"progress":{"type":"int32","id":6},"ctime":{"type":"string","id":7},"mtime":{"type":"string","id":8},"extra":{"type":"string","id":9},"dmid":{"type":"string","id":10}}},"DmSegConfig":{"fields":{"pageSize":{"type":"int64","id":1},"total":{"type":"int64","id":2}}},"DanmakuFlagConfig":{"fields":{"recFlag":{"type":"int32","id":1},"recText":{"type":"string","id":2},"recSwitch":{"type":"int32","id":3}}},"DmSegMobileReply":{"fields":{"elems":{"rule":"repeated","type":"DanmakuElem","id":1}}},"DanmakuElem":{"fields":{"progress":{"type":"int32","id":2},"mode":{"type":"int32","id":3},"fontsize":{"type":"int32","id":4},"color":{"type":"uint32","id":5},"midHash":{"type":"string","id":6},"content":{"type":"string","id":7},"ctime":{"type":"int64","id":8},"weight":{"type":"int32","id":9},"action":{"type":"string","id":10},"pool":{"type":"int32","id":11},"dmid":{"type":"string","id":12},"attr":{"type":"int32","id":13},"animation":{"type":"string","id":22}}},"DanmuWebPlayerConfig":{"fields":{"dmSwitch":{"type":"bool","id":1},"aiSwitch":{"type":"bool","id":2},"aiLevel":{"type":"int32","id":3},"typeTop":{"type":"bool","id":4},"typeScroll":{"type":"bool","id":5},"typeBottom":{"type":"bool","id":6},"typeColor":{"type":"bool","id":7},"typeSpecial":{"type":"bool","id":8},"preventshade":{"type":"bool","id":9},"dmask":{"type":"bool","id":10},"opacity":{"type":"float","id":11},"dmarea":{"type":"int32","id":12},"speedplus":{"type":"float","id":13},"fontsize":{"type":"float","id":14},"fullscreensync":{"type":"bool","id":15},"speedsync":{"type":"bool","id":16},"fontfamily":{"type":"string","id":17},"bold":{"type":"bool","id":18},"fontborder":{"type":"int32","id":19},"seniorModeSwitch":{"type":"int32","id":21}}},"Expressions":{"fields":{"data":{"rule":"repeated","type":"Expression","id":1}}},"Expression":{"fields":{"keyword":{"rule":"repeated","type":"string","id":1},"url":{"type":"string","id":2},"period":{"rule":"repeated","type":"Period","id":3}}},"Period":{"fields":{"start":{"type":"int64","id":1},"end":{"type":"int64","id":2}}}}}}}}}}}}}}}')
var r = "DanmakuElem"
var et = parse("bilibili.community.service.dm.v1." + r,rr)
function parse(e,d){
    e = e.split(".")
    var dd = d
    for (var i = 0; i< e.length ;  i++) {
        var t = e[i]
        dd = dd['nested'][t];
        if (dd==null) {
            return null;
        }
    }
    return dd;
}

var n={
    length : function(e) {
        for (var t = 0, r = 0, n = 0; n < e.length; ++n)
            (r = e.charCodeAt(n)) < 128 ? t += 1 : r < 2048 ? t += 2 : 55296 == (64512 & r) && 56320 == (64512 & e.charCodeAt(n + 1)) ? (++n,
            t += 4) : t += 3;
        return t
    }
    ,
    read : function(e, t, r) {
        if (r - t < 1)
            return "";
        for (var n, i = null, o = [], a = 0; t < r; )
            (n = e[t++]) < 128 ? o[a++] = n : n > 191 && n < 224 ? o[a++] = (31 & n) << 6 | 63 & e[t++] : n > 239 && n < 365 ? (n = ((7 & n) << 18 | (63 & e[t++]) << 12 | (63 & e[t++]) << 6 | 63 & e[t++]) - 65536,
            o[a++] = 55296 + (n >> 10),
            o[a++] = 56320 + (1023 & n)) : o[a++] = (15 & n) << 12 | (63 & e[t++]) << 6 | 63 & e[t++],
            a > 8191 && ((i || (i = [])).push(String.fromCharCode.apply(String, o)),
            a = 0);
        return i ? (a && i.push(String.fromCharCode.apply(String, o.slice(0, a))),
        i.join("")) : String.fromCharCode.apply(String, o.slice(0, a))
    }
    ,
    write : function(e, t, r) {
        for (var n, i, o = r, a = 0; a < e.length; ++a)
            (n = e.charCodeAt(a)) < 128 ? t[r++] = n : n < 2048 ? (t[r++] = n >> 6 | 192,
            t[r++] = 63 & n | 128) : 55296 == (64512 & n) && 56320 == (64512 & (i = e.charCodeAt(a + 1))) ? (n = 65536 + ((1023 & n) << 10) + (1023 & i),
            ++a,
            t[r++] = n >> 18 | 240,
            t[r++] = n >> 12 & 63 | 128,
            t[r++] = n >> 6 & 63 | 128,
            t[r++] = 63 & n | 128) : (t[r++] = n >> 12 | 224,
            t[r++] = n >> 6 & 63 | 128,
            t[r++] = 63 & n | 128);
        return r - o
    }    
}


function u(e) {
    this.buf = e,
    this.pos = 0,
    this.len = e.length
}
var l;
u.prototype._slice = Uint8Array.prototype.subarray || Uint8Array.prototype.slice,
u.prototype.uint32 = (l = 4294967295,
u.prototype.int32 = function() {
    return 0 | this.uint32()
}
,
function() {
    if (l = (127 & this.buf[this.pos]) >>> 0,
    this.buf[this.pos++] < 128)
        return l;
    if (l = (l | (127 & this.buf[this.pos]) << 7) >>> 0,
    this.buf[this.pos++] < 128)
        return l;
    if (l = (l | (127 & this.buf[this.pos]) << 14) >>> 0,
    this.buf[this.pos++] < 128)
        return l;
    if (l = (l | (127 & this.buf[this.pos]) << 21) >>> 0,
    this.buf[this.pos++] < 128)
        return l;
    if (l = (l | (15 & this.buf[this.pos]) << 28) >>> 0,
    this.buf[this.pos++] < 128)
        return l;
    if ((this.pos += 5) > this.len)
        throw this.pos = this.len,
        s(this, 10);
    return l
}
),
u.prototype.bytes = function() {
    var e = this.uint32()
      , t = this.pos
      , r = this.pos + e;
    if (r > this.len)
        throw s(this, e);
    return this.pos += e,
    Array.isArray(this.buf) ? this.buf.slice(t, r) : t === r ? new this.buf.constructor(0) : this._slice.call(this.buf, t, r)
}
,
u.prototype.string = function() {
    var e = this.bytes();
    return n.read(e, 0, e.length)
},
u.prototype.skip = function(e) {
    if ("number" == typeof e) {
        if (this.pos + e > this.len)
            throw s(this, e);
        this.pos += e
    } else
        do {
            if (this.pos >= this.len)
                throw s(this)
        } while (128 & this.buf[this.pos++]);
    return this
}
,
u.prototype.skipType = function(e) {
    switch (e) {
    case 0:
        this.skip();
        break;
    case 1:
        this.skip(8);
        break;
    case 2:
        this.skip(this.uint32());
        break;
    case 3:
        for (; 4 != (e = 7 & this.uint32()); )
            this.skipType(e);
        break;
    case 5:
        this.skip(4);
        break;
    default:
        throw Error("invalid wire type " + e + " at offset " + this.pos)
    }
    return this
}

function DanmakuElem(p){
    p = p.fields;
    if(p)
    for(var ks=Object.keys(p),i=0;i<ks.length;++i)if(p[ks[i]]!=null)
        if(p[ks[i]]['type']=='string'){
            this[ks[i]]='';
        }else{
            this[ks[i]]=0;
        }
        
}

function DanmakuElemDecode(Reader,r,l){
  if(!(r instanceof Reader))
  r=new Reader(r)
  var c=l===undefined?r.len:r.pos+l,m=new DanmakuElem(et)
  while(r.pos<c){
  var t=r.uint32()
  switch(t>>>3){
      case 2:
      m.progress=r.int32()
      break
      case 3:
      m.mode=r.int32()
      break
      case 4:
      m.fontsize=r.int32()
      break
      case 5:
      m.color=r.uint32()
      break
      case 6:
      m.midHash=r.string()
      break
      case 7:
      m.content=r.string()
      break
      case 8:
      m.ctime=r.int32()
      break
      case 9:
      m.weight=r.int32()
      break
      case 10:
      m.action=r.string()
      break
      case 11:
      m.pool=r.int32()
      break
      case 12:
      m.dmid=r.string()
      break
      case 13:
      m.attr=r.int32()
      break
      case 22:
      m.animation=r.string()
      break
      default:
      r.skipType(t&7)
      break
      }
  }
  return m
}

function DmSegView(p){
  this.elems=[]
  if(p)for(var ks=Object.keys(p),i=0;i<ks.length;++i)if(p[ks[i]]!=null)
  this[ks[i]]=p[ks[i]]
}
function DmSegMobileReply(Reader,r,l){
    if(!(r instanceof Reader))
    r=new Reader(r)
    var c=l===undefined?r.len:r.pos+l,m=new DmSegView;
    while(r.pos<c){
    var t=r.uint32()
    switch(t>>>3){
    case 1:
    if(!(m.elems&&m.elems.length))
    m.elems=[]
    m.elems.push(DanmakuElemDecode(Reader,r,r.uint32()))
    break
    default:
    r.skipType(t&7)
    break
    }
    }
    return m
}
var app = {
    run: function(data){
        return DmSegMobileReply(u, new Uint8Array(data))
    }
}
module.exports = app;