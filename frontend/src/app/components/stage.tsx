'use client'
import { useContext, useEffect, useState } from "react";
import AppContext from "./hooks/createContext";
import ReactDOM from 'react-dom';

const Stage = () => {
    const {
        image: [image]
    } = useContext(AppContext)!;

  
    const imageClasses = "";
    const maskImageClasses = `absolute opacity-40 pointer-events-none`;
    return (
        <div className="flex items-center justify-center w-1/2 h-1/2 bg-white">
            <div className="flex items-center justify-center w-[90%] h-[90%]"></div>
                <div>
            </div>
        </div>
    );
}

export default Stage;