import { useEffect, useRef } from "react"
import * as THREE from "three"
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls"
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader"

function Viewer({brain,tumor}){

const mount=useRef()

useEffect(()=>{

const scene=new THREE.Scene()

const camera=new THREE.PerspectiveCamera(
75,
600/600,
0.1,
1000
)

const renderer=new THREE.WebGLRenderer({antialias:true})
renderer.setSize(600,600)

mount.current.appendChild(renderer.domElement)

const controls=new OrbitControls(
camera,
renderer.domElement
)

const light=new THREE.DirectionalLight(0xffffff,1)
light.position.set(10,10,10)
scene.add(light)

const loader=new OBJLoader()

loader.load(
"http://127.0.0.1:8000/"+brain,
(obj)=>{
scene.add(obj)
}
)

loader.load(
"http://127.0.0.1:8000/"+tumor,
(obj)=>{
obj.traverse(child=>{
if(child.isMesh){
child.material.color.set(0xff0000)
}
})
scene.add(obj)
}
)

camera.position.z=200

const animate=()=>{
requestAnimationFrame(animate)
renderer.render(scene,camera)
}

animate()

},[])

return <div ref={mount}></div>

}

export default Viewer