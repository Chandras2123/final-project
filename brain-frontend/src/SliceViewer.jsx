import { useState, useEffect } from "react"
import axios from "axios"

const API = "https://final-project-awar.onrender.com"

function SliceViewer({filePath}){

const [slices,setSlices] = useState([])
const [index,setIndex] = useState(0)

useEffect(()=>{

axios.get(API + "/slices?path=" + filePath)
.then(res => setSlices(res.data.slices))

},[])

if(!slices.length) return <p>Loading slices...</p>

return(

<div>

<h3>MRI Slice Viewer</h3>

<input
type="range"
min="0"
max={slices.length-1}
value={index}
onChange={(e)=>setIndex(e.target.value)}
/>

<pre style={{fontSize:"6px"}}>
{JSON.stringify(slices[index])}
</pre>

</div>

)

}

export default SliceViewer
