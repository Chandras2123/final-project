import { useState, useEffect, useRef } from "react"
import axios from "axios"

const API = "https://final-project-awar.onrender.com"

function SliceViewer({filePath}){

const [slices,setSlices] = useState([])
const [index,setIndex] = useState(0)
const canvasRef = useRef(null)

useEffect(()=>{

axios.get(API + "/slices?path=" + filePath)
.then(res => {

setSlices(res.data.slices)

})

},[filePath])

useEffect(()=>{

if(!slices.length) return

const canvas = canvasRef.current
const ctx = canvas.getContext("2d")

const slice = slices[index]

const h = slice.length
const w = slice[0].length

canvas.width = w
canvas.height = h

const imgData = ctx.createImageData(w,h)

for(let y=0;y<h;y++){

for(let x=0;x<w;x++){

const val = Math.floor(slice[y][x] * 255)

const i = (y*w + x) * 4

imgData.data[i] = val
imgData.data[i+1] = val
imgData.data[i+2] = val
imgData.data[i+3] = 255

}

}

ctx.putImageData(imgData,0,0)

},[index,slices])

const scrollSlices = (e) => {

if(e.deltaY > 0){

setIndex(i => Math.min(i+1, slices.length-1))

}else{

setIndex(i => Math.max(i-1,0))

}

}

if(!slices.length) return <p>Loading MRI slices...</p>

return(

<div style={{marginTop:"30px"}}>

<h3>MRI Slice Viewer</h3>

<p>Slice {index+1} / {slices.length}</p>

<canvas
ref={canvasRef}
onWheel={scrollSlices}
style={{
border:"2px solid #333",
maxWidth:"500px",
cursor:"grab"
}}
/>

<br/>

<input
type="range"
min="0"
max={slices.length-1}
value={index}
onChange={(e)=>setIndex(Number(e.target.value))}
style={{width:"500px"}}
/>

</div>

)

}

export default SliceViewer
