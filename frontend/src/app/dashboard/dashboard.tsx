
'use client'
import Navbar from "../components/navbar";
import Link from "next/link";
import Stage from "../components/stage";
import { useContext, useEffect } from "react";
import React from "react";
import { handleImageScale } from "../components/helpers/scaleHelper";
import AppContext from "../components/hooks/createContext";
import MousePositionComponent from "./mousepos";


export default function Dashboard() {
    const [image, setImage] = React.useState<string | null>('/public/Untitled.jpeg');
    const [coords, setCoords] = React.useState<[number, number]>([0, 0]);
    const updateCoordinates = (x: number, y : number) => {setCoords([x, y])}
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e && e.target && e.target.files) {
            console.log(e.target.files[0])
            console.log(URL.createObjectURL(e.target.files[0]))
            setImage(URL.createObjectURL(e.target.files[0]));
        } else {
            console.log('error')
        }
    }

    return (
            <div className="flex flex-col items-center justify-center w-screen h-screen overflow-hidden bg-gradient-to-tl from-black via-zinc-600/20 to-black">
                <Navbar>
                    <Link href='/api/auth/login'>Logout</Link>
                </Navbar>
                <div className="bg-orange-100 h-1/2 w-1/2">
                <MousePositionComponent imageSrc={image} setCoords={updateCoordinates}/>
                </div>
                <form className="pb-10">
                    <input className="border-2 rounded-md p-1 px-2 m-2" type="file" onChange={handleChange} name="image" />
                    <input className="border-2 rounded-md p-1 px-2 m-2" type="submit" />
                </form>
                {/* <div className="mt-20 p-2 flex flex-col justify-center items-center border-solid border-2 rounded-md border-white h-[90%] w-[90%]">

                <div className="h-1/2 w-1/2 flex item-center justify-content">
                <img className="border-2 rounded-md" src={image}/>
                </div> */}
                {/* </div> */}
            </div>
    );
}