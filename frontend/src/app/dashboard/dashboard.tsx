
'use client'
import Navbar from "../components/navbar";
import Link from "next/link";
import Stage from "../components/stage";
import { FormEvent, useContext, useEffect } from "react";
import React from "react";
import { handleImageScale } from "../components/helpers/scaleHelper";
import AppContext from "../components/hooks/createContext";
import MousePositionComponent from "./mousepos";

import { useUser } from '@auth0/nextjs-auth0/client';

export default function Dashboard() {
    const [resultImage, setResultImage] = React.useState<string>('/public/Untitled.jpeg');
    const [image, setImage] = React.useState<string | null>('/public/Untitled.jpeg');
    const [file, setFile] = React.useState<File>()
    const [coords, setCoords] = React.useState<[number, number]>([0, 0]);
    const updateCoordinates = (x: number, y: number) => { setCoords([x, y]) }
    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e && e.target && e.target.files) {
            console.log(e.target.files[0]);
            setFile(e.target.files[0]);
            setImage(URL.createObjectURL(e.target.files[0]));
        } else {
            console.log('error')
        }
    }
    const apiUrl = 'http://127.0.0.1:5000/mask';

    const submitForm = (e: React.SyntheticEvent): Promise<void> => {
        e.preventDefault();
        const str = JSON.stringify({ "coordinates": { "x": coords[0], "y": coords[1] } })
        const data = new FormData();
        if (file) {
            data.append('image', file)
            data.append('data', new Blob([str], { type: "application/json" }))
        }

            // Access-Control-Allow-Origin: https://example.com
        const requestOptions: RequestInit = {
            method: 'POST',
            body: data,
            headers: {'Access-Control-Allow-Origin': 'http://127.0.0.1:5000/mask'},
        };
        return fetch(apiUrl, requestOptions)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Failed to submit form: ${response.statusText}`);
                }
                return response.blob()
            })
            .then((blob) => setResultImage(URL.createObjectURL(blob)))
    }

    const {user, error, isLoading} = useUser();

    return (
        <div className="flex flex-col items-center justify-center w-screen h-screen overflow-hidden bg-gradient-to-tl from-black via-zinc-600/20 to-black">
            <Navbar header={user ? `Welcome ${user?.name}`: ''}>
                <Link href='/api/auth/login?redirectTo=/'>Logout</Link>
            </Navbar>
            <div className="bg-orange-100 h-1/2 w-1/2">
                <MousePositionComponent imageSrc={image} setCoords={updateCoordinates} />
            </div>
            <form className="py-10" onSubmit={(e: FormEvent<HTMLFormElement>) => {
                submitForm(e)
            }}>
                <input className="border-2 rounded-md p-1 px-2 m-2" type="file" onChange={handleChange} name="image" />
                <input className="border-2 rounded-md p-1 px-2 m-2" type="submit" />
            </form>
            <img className="bg-white" src={resultImage} />
            {/* <div className="mt-20 p-2 flex flex-col justify-center items-center border-solid border-2 rounded-md border-white h-[90%] w-[90%]">

                <div className="h-1/2 w-1/2 flex item-center justify-content">
                <img className="border-2 rounded-md" src={image}/>
                </div> */}
            {/* </div> */}
        </div>
    );
}