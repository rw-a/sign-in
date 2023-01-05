  var QRCode;!function(){function t(t){this.mode=e.MODE_8BIT_BYTE,this.data=t,this.parsedData=[];for(var _=0,r=this.data.length;_<r;_++){var i=[],o=this.data.charCodeAt(_);o>65536?(i[0]=240|(1835008&o)>>>18,i[1]=128|(258048&o)>>>12,i[2]=128|(4032&o)>>>6,i[3]=128|63&o):o>2048?(i[0]=224|(61440&o)>>>12,i[1]=128|(4032&o)>>>6,i[2]=128|63&o):o>128?(i[0]=192|(1984&o)>>>6,i[1]=128|63&o):i[0]=o,this.parsedData.push(i)}this.parsedData=Array.prototype.concat.apply([],this.parsedData),this.parsedData.length!=this.data.length&&(this.parsedData.unshift(191),this.parsedData.unshift(187),this.parsedData.unshift(239))}function _(t,_){this.typeNumber=t,this.errorCorrectLevel=_,this.modules=null,this.moduleCount=0,this.dataCache=null,this.dataList=[]}t.prototype={getLength:function(t){return this.parsedData.length},write:function(t){for(var _=0,e=this.parsedData.length;_<e;_++)t.put(this.parsedData[_],8)}},_.prototype={addData:function(_){var e=new t(_);this.dataList.push(e),this.dataCache=null},isDark:function(t,_){if(t<0||this.moduleCount<=t||_<0||this.moduleCount<=_)throw Error(t+","+_);return this.modules[t][_]},getModuleCount:function(){return this.moduleCount},make:function(){this.makeImpl(!1,this.getBestMaskPattern())},makeImpl:function(t,e){this.moduleCount=4*this.typeNumber+17,this.modules=Array(this.moduleCount);for(var r=0;r<this.moduleCount;r++){this.modules[r]=Array(this.moduleCount);for(var i=0;i<this.moduleCount;i++)this.modules[r][i]=null}this.setupPositionProbePattern(0,0),this.setupPositionProbePattern(this.moduleCount-7,0),this.setupPositionProbePattern(0,this.moduleCount-7),this.setupPositionAdjustPattern(),this.setupTimingPattern(),this.setupTypeInfo(t,e),this.typeNumber>=7&&this.setupTypeNumber(t),null==this.dataCache&&(this.dataCache=_.createData(this.typeNumber,this.errorCorrectLevel,this.dataList)),this.mapData(this.dataCache,e)},setupPositionProbePattern:function(t,_){for(var e=-1;e<=7;e++)if(!(t+e<=-1)&&!(this.moduleCount<=t+e))for(var r=-1;r<=7;r++)_+r<=-1||this.moduleCount<=_+r||(0<=e&&e<=6&&(0==r||6==r)||0<=r&&r<=6&&(0==e||6==e)||2<=e&&e<=4&&2<=r&&r<=4?this.modules[t+e][_+r]=!0:this.modules[t+e][_+r]=!1)},getBestMaskPattern:function(){for(var t=0,_=0,e=0;e<8;e++){this.makeImpl(!0,e);var r=o.getLostPoint(this);(0==e||t>r)&&(t=r,_=e)}return _},createMovieClip:function(t,_,e){var r=t.createEmptyMovieClip(_,e);this.make();for(var i=0;i<this.modules.length;i++)for(var o=1*i,n=0;n<this.modules[i].length;n++){var a=1*n;this.modules[i][n]&&(r.beginFill(0,100),r.moveTo(a,o),r.lineTo(a+1,o),r.lineTo(a+1,o+1),r.lineTo(a,o+1),r.endFill())}return r},setupTimingPattern:function(){for(var t=8;t<this.moduleCount-8;t++)null==this.modules[t][6]&&(this.modules[t][6]=t%2==0);for(var _=8;_<this.moduleCount-8;_++)null==this.modules[6][_]&&(this.modules[6][_]=_%2==0)},setupPositionAdjustPattern:function(){for(var t=o.getPatternPosition(this.typeNumber),_=0;_<t.length;_++)for(var e=0;e<t.length;e++){var r=t[_],i=t[e];if(null==this.modules[r][i])for(var n=-2;n<=2;n++)for(var a=-2;a<=2;a++)-2==n||2==n||-2==a||2==a||0==n&&0==a?this.modules[r+n][i+a]=!0:this.modules[r+n][i+a]=!1}},setupTypeNumber:function(t){for(var _=o.getBCHTypeNumber(this.typeNumber),e=0;e<18;e++){var r=!t&&(_>>e&1)==1;this.modules[Math.floor(e/3)][e%3+this.moduleCount-8-3]=r}for(var e=0;e<18;e++){var r=!t&&(_>>e&1)==1;this.modules[e%3+this.moduleCount-8-3][Math.floor(e/3)]=r}},setupTypeInfo:function(t,_){for(var e=this.errorCorrectLevel<<3|_,r=o.getBCHTypeInfo(e),i=0;i<15;i++){var n=!t&&(r>>i&1)==1;i<6?this.modules[i][8]=n:i<8?this.modules[i+1][8]=n:this.modules[this.moduleCount-15+i][8]=n}for(var i=0;i<15;i++){var n=!t&&(r>>i&1)==1;i<8?this.modules[8][this.moduleCount-i-1]=n:i<9?this.modules[8][15-i-1+1]=n:this.modules[8][15-i-1]=n}this.modules[this.moduleCount-8][8]=!t},mapData:function(t,_){for(var e=-1,r=this.moduleCount-1,i=7,n=0,a=this.moduleCount-1;a>0;a-=2)for(6==a&&a--;;){for(var s=0;s<2;s++)if(null==this.modules[r][a-s]){var $=!1;n<t.length&&($=(t[n]>>>i&1)==1),o.getMask(_,r,a-s)&&($=!$),this.modules[r][a-s]=$,-1==--i&&(n++,i=7)}if((r+=e)<0||this.moduleCount<=r){r-=e,e=-e;break}}}},_.PAD0=236,_.PAD1=17,_.createData=function(t,e,r){for(var i=$.getRSBlocks(t,e),n=new h,a=0;a<r.length;a++){var s=r[a];n.put(s.mode,4),n.put(s.getLength(),o.getLengthInBits(s.mode,t)),s.write(n)}for(var l=0,a=0;a<i.length;a++)l+=i[a].dataCount;if(n.getLengthInBits()>8*l)throw Error("code length overflow. ("+n.getLengthInBits()+">"+8*l+")");for(n.getLengthInBits()+4<=8*l&&n.put(0,4);n.getLengthInBits()%8!=0;)n.putBit(!1);for(;!(n.getLengthInBits()>=8*l)&&(n.put(_.PAD0,8),!(n.getLengthInBits()>=8*l));){n.put(_.PAD1,8)}return _.createBytes(n,i)},_.createBytes=function(t,_){for(var e=0,r=0,i=0,n=Array(_.length),a=Array(_.length),$=0;$<_.length;$++){var h=_[$].dataCount,l=_[$].totalCount-h;r=Math.max(r,h),i=Math.max(i,l),n[$]=Array(h);for(var u=0;u<n[$].length;u++)n[$][u]=255&t.buffer[u+e];e+=h;var f=o.getErrorCorrectPolynomial(l),g=new s(n[$],f.getLength()-1).mod(f);a[$]=Array(f.getLength()-1);for(var u=0;u<a[$].length;u++){var d=u+g.getLength()-a[$].length;a[$][u]=d>=0?g.get(d):0}}for(var c=0,u=0;u<_.length;u++)c+=_[u].totalCount;for(var p=Array(c),m=0,u=0;u<r;u++)for(var $=0;$<_.length;$++)u<n[$].length&&(p[m++]=n[$][u]);for(var u=0;u<i;u++)for(var $=0;$<_.length;$++)u<a[$].length&&(p[m++]=a[$][u]);return p};for(var e={MODE_NUMBER:1,MODE_ALPHA_NUM:2,MODE_8BIT_BYTE:4,MODE_KANJI:8},r={L:1,M:0,Q:3,H:2},i={PATTERN000:0,PATTERN001:1,PATTERN010:2,PATTERN011:3,PATTERN100:4,PATTERN101:5,PATTERN110:6,PATTERN111:7},o={PATTERN_POSITION_TABLE:[[],[6,18],[6,22],[6,26],[6,30],[6,34],[6,22,38],[6,24,42],[6,26,46],[6,28,50],[6,30,54],[6,32,58],[6,34,62],[6,26,46,66],[6,26,48,70],[6,26,50,74],[6,30,54,78],[6,30,56,82],[6,30,58,86],[6,34,62,90],[6,28,50,72,94],[6,26,50,74,98],[6,30,54,78,102],[6,28,54,80,106],[6,32,58,84,110],[6,30,58,86,114],[6,34,62,90,118],[6,26,50,74,98,122],[6,30,54,78,102,126],[6,26,52,78,104,130],[6,30,56,82,108,134],[6,34,60,86,112,138],[6,30,58,86,114,142],[6,34,62,90,118,146],[6,30,54,78,102,126,150],[6,24,50,76,102,128,154],[6,28,54,80,106,132,158],[6,32,58,84,110,136,162],[6,26,54,82,110,138,166],[6,30,58,86,114,142,170]],G15:1335,G18:7973,G15_MASK:21522,getBCHTypeInfo:function(t){for(var _=t<<10;o.getBCHDigit(_)-o.getBCHDigit(o.G15)>=0;)_^=o.G15<<o.getBCHDigit(_)-o.getBCHDigit(o.G15);return(t<<10|_)^o.G15_MASK},getBCHTypeNumber:function(t){for(var _=t<<12;o.getBCHDigit(_)-o.getBCHDigit(o.G18)>=0;)_^=o.G18<<o.getBCHDigit(_)-o.getBCHDigit(o.G18);return t<<12|_},getBCHDigit:function(t){for(var _=0;0!=t;)_++,t>>>=1;return _},getPatternPosition:function(t){return o.PATTERN_POSITION_TABLE[t-1]},getMask:function(t,_,e){switch(t){case i.PATTERN000:return(_+e)%2==0;case i.PATTERN001:return _%2==0;case i.PATTERN010:return e%3==0;case i.PATTERN011:return(_+e)%3==0;case i.PATTERN100:return(Math.floor(_/2)+Math.floor(e/3))%2==0;case i.PATTERN101:return _*e%2+_*e%3==0;case i.PATTERN110:return(_*e%2+_*e%3)%2==0;case i.PATTERN111:return(_*e%3+(_+e)%2)%2==0;default:throw Error("bad maskPattern:"+t)}},getErrorCorrectPolynomial:function(t){for(var _=new s([1],0),e=0;e<t;e++)_=_.multiply(new s([1,n.gexp(e)],0));return _},getLengthInBits:function(t,_){if(1<=_&&_<10)switch(t){case e.MODE_NUMBER:return 10;case e.MODE_ALPHA_NUM:return 9;case e.MODE_8BIT_BYTE:case e.MODE_KANJI:return 8;default:throw Error("mode:"+t)}else if(_<27)switch(t){case e.MODE_NUMBER:return 12;case e.MODE_ALPHA_NUM:return 11;case e.MODE_8BIT_BYTE:return 16;case e.MODE_KANJI:return 10;default:throw Error("mode:"+t)}else if(_<41)switch(t){case e.MODE_NUMBER:return 14;case e.MODE_ALPHA_NUM:return 13;case e.MODE_8BIT_BYTE:return 16;case e.MODE_KANJI:return 12;default:throw Error("mode:"+t)}else throw Error("type:"+_)},getLostPoint:function(t){for(var _=t.getModuleCount(),e=0,r=0;r<_;r++)for(var i=0;i<_;i++){for(var o=0,n=t.isDark(r,i),a=-1;a<=1;a++)if(!(r+a<0)&&!(_<=r+a))for(var s=-1;s<=1;s++)!(i+s<0)&&!(_<=i+s)&&(0!=a||0!=s)&&n==t.isDark(r+a,i+s)&&o++;o>5&&(e+=3+o-5)}for(var r=0;r<_-1;r++)for(var i=0;i<_-1;i++){var $=0;t.isDark(r,i)&&$++,t.isDark(r+1,i)&&$++,t.isDark(r,i+1)&&$++,t.isDark(r+1,i+1)&&$++,(0==$||4==$)&&(e+=3)}for(var r=0;r<_;r++)for(var i=0;i<_-6;i++)t.isDark(r,i)&&!t.isDark(r,i+1)&&t.isDark(r,i+2)&&t.isDark(r,i+3)&&t.isDark(r,i+4)&&!t.isDark(r,i+5)&&t.isDark(r,i+6)&&(e+=40);for(var i=0;i<_;i++)for(var r=0;r<_-6;r++)t.isDark(r,i)&&!t.isDark(r+1,i)&&t.isDark(r+2,i)&&t.isDark(r+3,i)&&t.isDark(r+4,i)&&!t.isDark(r+5,i)&&t.isDark(r+6,i)&&(e+=40);for(var h=0,i=0;i<_;i++)for(var r=0;r<_;r++)t.isDark(r,i)&&h++;return e+10*(Math.abs(100*h/_/_-50)/5)}},n={glog:function(t){if(t<1)throw Error("glog("+t+")");return n.LOG_TABLE[t]},gexp:function(t){for(;t<0;)t+=255;for(;t>=256;)t-=255;return n.EXP_TABLE[t]},EXP_TABLE:Array(256),LOG_TABLE:Array(256)},a=0;a<8;a++)n.EXP_TABLE[a]=1<<a;for(var a=8;a<256;a++)n.EXP_TABLE[a]=n.EXP_TABLE[a-4]^n.EXP_TABLE[a-5]^n.EXP_TABLE[a-6]^n.EXP_TABLE[a-8];for(var a=0;a<255;a++)n.LOG_TABLE[n.EXP_TABLE[a]]=a;function s(t,_){if(void 0==t.length)throw Error(t.length+"/"+_);for(var e=0;e<t.length&&0==t[e];)e++;this.num=Array(t.length-e+_);for(var r=0;r<t.length-e;r++)this.num[r]=t[r+e]}function $(t,_){this.totalCount=t,this.dataCount=_}function h(){this.buffer=[],this.length=0}s.prototype={get:function(t){return this.num[t]},getLength:function(){return this.num.length},multiply:function(t){for(var _=Array(this.getLength()+t.getLength()-1),e=0;e<this.getLength();e++)for(var r=0;r<t.getLength();r++)_[e+r]^=n.gexp(n.glog(this.get(e))+n.glog(t.get(r)));return new s(_,0)},mod:function(t){if(this.getLength()-t.getLength()<0)return this;for(var _=n.glog(this.get(0))-n.glog(t.get(0)),e=Array(this.getLength()),r=0;r<this.getLength();r++)e[r]=this.get(r);for(var r=0;r<t.getLength();r++)e[r]^=n.gexp(n.glog(t.get(r))+_);return new s(e,0).mod(t)}},$.RS_BLOCK_TABLE=[[1,26,19],[1,26,16],[1,26,13],[1,26,9],[1,44,34],[1,44,28],[1,44,22],[1,44,16],[1,70,55],[1,70,44],[2,35,17],[2,35,13],[1,100,80],[2,50,32],[2,50,24],[4,25,9],[1,134,108],[2,67,43],[2,33,15,2,34,16],[2,33,11,2,34,12],[2,86,68],[4,43,27],[4,43,19],[4,43,15],[2,98,78],[4,49,31],[2,32,14,4,33,15],[4,39,13,1,40,14],[2,121,97],[2,60,38,2,61,39],[4,40,18,2,41,19],[4,40,14,2,41,15],[2,146,116],[3,58,36,2,59,37],[4,36,16,4,37,17],[4,36,12,4,37,13],[2,86,68,2,87,69],[4,69,43,1,70,44],[6,43,19,2,44,20],[6,43,15,2,44,16],[4,101,81],[1,80,50,4,81,51],[4,50,22,4,51,23],[3,36,12,8,37,13],[2,116,92,2,117,93],[6,58,36,2,59,37],[4,46,20,6,47,21],[7,42,14,4,43,15],[4,133,107],[8,59,37,1,60,38],[8,44,20,4,45,21],[12,33,11,4,34,12],[3,145,115,1,146,116],[4,64,40,5,65,41],[11,36,16,5,37,17],[11,36,12,5,37,13],[5,109,87,1,110,88],[5,65,41,5,66,42],[5,54,24,7,55,25],[11,36,12],[5,122,98,1,123,99],[7,73,45,3,74,46],[15,43,19,2,44,20],[3,45,15,13,46,16],[1,135,107,5,136,108],[10,74,46,1,75,47],[1,50,22,15,51,23],[2,42,14,17,43,15],[5,150,120,1,151,121],[9,69,43,4,70,44],[17,50,22,1,51,23],[2,42,14,19,43,15],[3,141,113,4,142,114],[3,70,44,11,71,45],[17,47,21,4,48,22],[9,39,13,16,40,14],[3,135,107,5,136,108],[3,67,41,13,68,42],[15,54,24,5,55,25],[15,43,15,10,44,16],[4,144,116,4,145,117],[17,68,42],[17,50,22,6,51,23],[19,46,16,6,47,17],[2,139,111,7,140,112],[17,74,46],[7,54,24,16,55,25],[34,37,13],[4,151,121,5,152,122],[4,75,47,14,76,48],[11,54,24,14,55,25],[16,45,15,14,46,16],[6,147,117,4,148,118],[6,73,45,14,74,46],[11,54,24,16,55,25],[30,46,16,2,47,17],[8,132,106,4,133,107],[8,75,47,13,76,48],[7,54,24,22,55,25],[22,45,15,13,46,16],[10,142,114,2,143,115],[19,74,46,4,75,47],[28,50,22,6,51,23],[33,46,16,4,47,17],[8,152,122,4,153,123],[22,73,45,3,74,46],[8,53,23,26,54,24],[12,45,15,28,46,16],[3,147,117,10,148,118],[3,73,45,23,74,46],[4,54,24,31,55,25],[11,45,15,31,46,16],[7,146,116,7,147,117],[21,73,45,7,74,46],[1,53,23,37,54,24],[19,45,15,26,46,16],[5,145,115,10,146,116],[19,75,47,10,76,48],[15,54,24,25,55,25],[23,45,15,25,46,16],[13,145,115,3,146,116],[2,74,46,29,75,47],[42,54,24,1,55,25],[23,45,15,28,46,16],[17,145,115],[10,74,46,23,75,47],[10,54,24,35,55,25],[19,45,15,35,46,16],[17,145,115,1,146,116],[14,74,46,21,75,47],[29,54,24,19,55,25],[11,45,15,46,46,16],[13,145,115,6,146,116],[14,74,46,23,75,47],[44,54,24,7,55,25],[59,46,16,1,47,17],[12,151,121,7,152,122],[12,75,47,26,76,48],[39,54,24,14,55,25],[22,45,15,41,46,16],[6,151,121,14,152,122],[6,75,47,34,76,48],[46,54,24,10,55,25],[2,45,15,64,46,16],[17,152,122,4,153,123],[29,74,46,14,75,47],[49,54,24,10,55,25],[24,45,15,46,46,16],[4,152,122,18,153,123],[13,74,46,32,75,47],[48,54,24,14,55,25],[42,45,15,32,46,16],[20,147,117,4,148,118],[40,75,47,7,76,48],[43,54,24,22,55,25],[10,45,15,67,46,16],[19,148,118,6,149,119],[18,75,47,31,76,48],[34,54,24,34,55,25],[20,45,15,61,46,16]],$.getRSBlocks=function(t,_){var e=$.getRsBlockTable(t,_);if(void 0==e)throw Error("bad rs block @ typeNumber:"+t+"/errorCorrectLevel:"+_);for(var r=e.length/3,i=[],o=0;o<r;o++)for(var n=e[3*o+0],a=e[3*o+1],s=e[3*o+2],h=0;h<n;h++)i.push(new $(a,s));return i},$.getRsBlockTable=function(t,_){switch(_){case r.L:return $.RS_BLOCK_TABLE[(t-1)*4+0];case r.M:return $.RS_BLOCK_TABLE[(t-1)*4+1];case r.Q:return $.RS_BLOCK_TABLE[(t-1)*4+2];case r.H:return $.RS_BLOCK_TABLE[(t-1)*4+3];default:return}},h.prototype={get:function(t){var _=Math.floor(t/8);return(this.buffer[_]>>>7-t%8&1)==1},put:function(t,_){for(var e=0;e<_;e++)this.putBit((t>>>_-e-1&1)==1)},getLengthInBits:function(){return this.length},putBit:function(t){var _=Math.floor(this.length/8);this.buffer.length<=_&&this.buffer.push(0),t&&(this.buffer[_]|=128>>>this.length%8),this.length++}};var l=[[17,14,11,7],[32,26,20,14],[53,42,32,24],[78,62,46,34],[106,84,60,44],[134,106,74,58],[154,122,86,64],[192,152,108,84],[230,180,130,98],[271,213,151,119],[321,251,177,137],[367,287,203,155],[425,331,241,177],[458,362,258,194],[520,412,292,220],[586,450,322,250],[644,504,364,280],[718,560,394,310],[792,624,442,338],[858,666,482,382],[929,711,509,403],[1003,779,565,439],[1091,857,611,461],[1171,911,661,511],[1273,997,715,535],[1367,1059,751,593],[1465,1125,805,625],[1528,1190,868,658],[1628,1264,908,698],[1732,1370,982,742],[1840,1452,1030,790],[1952,1538,1112,842],[2068,1628,1168,898],[2188,1722,1228,958],[2303,1809,1283,983],[2431,1911,1351,1051],[2563,1989,1423,1093],[2699,2099,1499,1139],[2809,2213,1579,1219],[2953,2331,1663,1273]];function u(){var t=!1,_=navigator.userAgent;if(/android/i.test(_)){t=!0;var e=_.toString().match(/android ([0-9]\.[0-9])/i);e&&e[1]&&(t=parseFloat(e[1]))}return t}var f,g,d=((f=function(t,_){this._el=t,this._htOption=_}).prototype.draw=function(t){var _=this._htOption,e=this._el,r=t.getModuleCount();function i(t,_){var e=document.createElementNS("http://www.w3.org/2000/svg",t);for(var r in _)_.hasOwnProperty(r)&&e.setAttribute(r,_[r]);return e}_.width,_.height,this.clear();var o=i("svg",{viewBox:"0 0 "+String(r)+" "+String(r),width:"100%",height:"100%",fill:_.colorLight});o.setAttributeNS("http://www.w3.org/2000/xmlns/","xmlns:xlink","http://www.w3.org/1999/xlink"),e.appendChild(o),o.appendChild(i("rect",{fill:_.colorLight,width:"100%",height:"100%"})),o.appendChild(i("rect",{fill:_.colorDark,width:"1",height:"1",id:"template"}));for(var n=0;n<r;n++)for(var a=0;a<r;a++)if(t.isDark(n,a)){var s=i("use",{x:String(a),y:String(n)});s.setAttributeNS("http://www.w3.org/1999/xlink","href","#template"),o.appendChild(s)}},f.prototype.clear=function(){for(;this._el.hasChildNodes();)this._el.removeChild(this._el.lastChild)},f),c="svg"===document.documentElement.tagName.toLowerCase()?d:"undefined"!=typeof CanvasRenderingContext2D?function(){function t(){this._elImage.src=this._elCanvas.toDataURL("image/png"),this._elImage.style.display="block",this._elCanvas.style.display="none"}if(this._android&&this._android<=2.1){var _=1/window.devicePixelRatio,e=CanvasRenderingContext2D.prototype.drawImage;CanvasRenderingContext2D.prototype.drawImage=function(t,r,i,o,n,a,s,$,h){if("nodeName"in t&&/img/i.test(t.nodeName))for(var l=arguments.length-1;l>=1;l--)arguments[l]=arguments[l]*_;else void 0===$&&(arguments[1]*=_,arguments[2]*=_,arguments[3]*=_,arguments[4]*=_);e.apply(this,arguments)}}function r(t,_){var e=this;if(e._fFail=_,e._fSuccess=t,null===e._bSupportDataURI){var r=document.createElement("img"),i=function(){e._bSupportDataURI=!1,e._fFail&&e._fFail.call(e)},o=function(){e._bSupportDataURI=!0,e._fSuccess&&e._fSuccess.call(e)};r.onabort=i,r.onerror=i,r.onload=o,r.src="data:image/gif;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNbyblAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5ErkJggg==";return}!0===e._bSupportDataURI&&e._fSuccess?e._fSuccess.call(e):!1===e._bSupportDataURI&&e._fFail&&e._fFail.call(e)}var i=function(t,_){this._bIsPainted=!1,this._android=u(),this._htOption=_,this._elCanvas=document.createElement("canvas"),this._elCanvas.width=_.width,this._elCanvas.height=_.height,t.appendChild(this._elCanvas),this._el=t,this._oContext=this._elCanvas.getContext("2d"),this._bIsPainted=!1,this._elImage=document.createElement("img"),this._elImage.alt="Scan me!",this._elImage.style.display="none",this._el.appendChild(this._elImage),this._bSupportDataURI=null};return i.prototype.draw=function(t){var _=this._elImage,e=this._oContext,r=this._htOption,i=t.getModuleCount(),o=r.width/i,n=r.height/i,a=Math.round(o),s=Math.round(n);_.style.display="none",this.clear();for(var $=0;$<i;$++)for(var h=0;h<i;h++){var l=t.isDark($,h),u=h*o,f=$*n;e.strokeStyle=l?r.colorDark:r.colorLight,e.lineWidth=1,e.fillStyle=l?r.colorDark:r.colorLight,e.fillRect(u,f,o,n),e.strokeRect(Math.floor(u)+.5,Math.floor(f)+.5,a,s),e.strokeRect(Math.ceil(u)-.5,Math.ceil(f)-.5,a,s)}this._bIsPainted=!0},i.prototype.makeImage=function(){this._bIsPainted&&r.call(this,t)},i.prototype.isPainted=function(){return this._bIsPainted},i.prototype.clear=function(){this._oContext.clearRect(0,0,this._elCanvas.width,this._elCanvas.height),this._bIsPainted=!1},i.prototype.round=function(t){return t?Math.floor(1e3*t)/1e3:t},i}():((g=function(t,_){this._el=t,this._htOption=_}).prototype.draw=function(t){for(var _=this._htOption,e=this._el,r=t.getModuleCount(),i=Math.floor(_.width/r),o=Math.floor(_.height/r),n=['<table style="border:0;border-collapse:collapse;">'],a=0;a<r;a++){n.push("<tr>");for(var s=0;s<r;s++)n.push('<td style="border:0;border-collapse:collapse;padding:0;margin:0;width:'+i+"px;height:"+o+"px;background-color:"+(t.isDark(a,s)?_.colorDark:_.colorLight)+';"></td>');n.push("</tr>")}n.push("</table>"),e.innerHTML=n.join("");var $=e.childNodes[0],h=(_.width-$.offsetWidth)/2,l=(_.height-$.offsetHeight)/2;h>0&&l>0&&($.style.margin=l+"px "+h+"px")},g.prototype.clear=function(){this._el.innerHTML=""},g);(QRCode=function(t,_){if(this._htOption={width:256,height:256,typeNumber:4,colorDark:"#000000",colorLight:"#ffffff",correctLevel:r.H},"string"==typeof _&&(_={text:_}),_)for(var e in _)this._htOption[e]=_[e];"string"==typeof t&&(t=document.getElementById(t)),this._htOption.useSVG&&(c=d),this._android=u(),this._el=t,this._oQRCode=null,this._oDrawing=new c(this._el,this._htOption),this._htOption.text&&this.makeCode(this._htOption.text)}).prototype.makeCode=function(t){this._oQRCode=new _(function t(_,e){for(var i,o,n=1,a=(i=_,o=encodeURI(i).toString().replace(/\%[0-9a-fA-F]{2}/g,"a"),o.length+(o.length!=i?3:0)),s=0,$=l.length;s<=$;s++){var h=0;switch(e){case r.L:h=l[s][0];break;case r.M:h=l[s][1];break;case r.Q:h=l[s][2];break;case r.H:h=l[s][3]}if(a<=h)break;n++}if(n>l.length)throw Error("Too long data");return n}(t,this._htOption.correctLevel),this._htOption.correctLevel),this._oQRCode.addData(t),this._oQRCode.make(),this._el.title=t,this._oDrawing.draw(this._oQRCode),this.makeImage()},QRCode.prototype.makeImage=function(){"function"==typeof this._oDrawing.makeImage&&(!this._android||this._android>=3)&&this._oDrawing.makeImage()},QRCode.prototype.clear=function(){this._oDrawing.clear()},QRCode.CorrectLevel=r}();