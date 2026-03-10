import { useState } from "react"
import axios from "axios"
import Viewer from "./Viewer"
import SliceViewer from "./SliceViewer"
import "./App.css"

const API = "https://final-project-awar.onrender.com"

function App(){

const [file,setFile] = useState(null)
const [result,setResult] = useState(null)
const [error,setError] = useState(null)
const [loading,setLoading] = useState(false)
const [showSlices,setShowSlices] = useState(false)

const upload = async () => {

if(!file){
alert("Please select an MRI file")
return
}

const form = new FormData()
form.append("file",file)

setLoading(true)

try{

const res = await axios.post(
API + "/upload",
form
)

setResult(res.data)
setError(null)

}catch(e){

setResult(null)

if(e.response){
setError(e.response.data.error || e.response.data.detail)
}else{
setError("Upload failed")
}

}finally{

setLoading(false)

}

}

return(

<div className="app">

<header className="header">
<h1>AI Brain Tumor Detection & 3D Surgical Planning</h1>
<p>Deep Learning based MRI Analysis Platform</p>
</header>

<div className="uploadSection">

<input
type="file"
id="fileUpload"
accept=".nii,.nii.gz,.jpg,.jpeg,.png"
hidden
onChange={(e)=>setFile(e.target.files[0])}
/>

<label htmlFor="fileUpload" className="uploadBtn">
Select MRI File
</label>

<button
className="analyzeBtn"
onClick={upload}
disabled={loading}

>

{loading ? (
<> <span className="spinner"></span>
Analyzing...
</>
) : (
"Analyze MRI"
)}

</button>

</div>

{error && (

<div className="errorBox">
{error}
</div>

)}

{result && (

<div className="resultPanel">

<h2>Prediction Result</h2>

<p><b>Mode:</b> {result.mode}</p>

<p><b>Tumor Type:</b> {result.tumor_type}</p>

{result.brain_mesh && (

<>

<div className="downloadSection">

<a
href={API + "/" + result.brain_mesh}
target="_blank"
rel="noreferrer"

>

Download Brain Mesh </a>

<a
href={API + "/" + result.tumor_mesh}
target="_blank"
rel="noreferrer"

>

Download Tumor Mesh </a>

</div>

<h3>3D Brain Visualization</h3>

<Viewer
brain={result.brain_mesh}
tumor={result.tumor_mesh}
/>

<div className="actionButtons">

<button
className="vrBtn"
onClick={()=>window.open("/vr.html","_blank")}

>

View Brain in VR </button>

<button
className="sliceBtn"
onClick={()=>setShowSlices(true)}

>

View MRI Slices </button>

</div>

{showSlices && (

<SliceViewer filePath={result.file_path}/>

)}

</>

)}

</div>

)}

</div>

)

}

export default App
