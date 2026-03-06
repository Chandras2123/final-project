import { Canvas } from "@react-three/fiber"
import { OrbitControls } from "@react-three/drei"
import { OBJLoader } from "three/examples/jsm/loaders/OBJLoader"
import { useLoader } from "@react-three/fiber"

function Brain({ url }) {

  const obj = useLoader(OBJLoader, url)

  return <primitive object={obj} scale={1} />

}

export default function VRViewer({ brain }) {

  return (

    <Canvas>

      <ambientLight intensity={0.5} />
      <directionalLight position={[10,10,10]} />

      <Brain url={"http://127.0.0.1:8000/"+brain} />

      <OrbitControls />

    </Canvas>

  )

}