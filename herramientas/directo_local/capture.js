class LexiaCapture extends AudioWorkletProcessor {
  constructor(){super();this.buffer=new Float32Array(512);this.offset=0;this.ended=false;
    this.port.onmessage=e=>{if(e.data==='flush'){
      if(this.offset){const tail=this.buffer.slice(0,this.offset);this.port.postMessage(tail,[tail.buffer]);this.offset=0;}
      this.ended=true;this.port.postMessage({flushed:true});
    }};
  }
  process(inputs,outputs){
    if(this.ended)return false;
    const channels=inputs[0];if(!channels||!channels.length)return true;
    for(let i=0;i<channels[0].length;i++){
      let value=0;for(const ch of channels)value+=ch[i];this.buffer[this.offset++]=value/channels.length;
      if(this.offset===this.buffer.length){this.port.postMessage(this.buffer,[this.buffer.buffer]);this.buffer=new Float32Array(512);this.offset=0;}
    }
    return true;
  }
}
registerProcessor('lexia-capture',LexiaCapture);
