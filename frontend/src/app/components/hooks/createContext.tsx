'use client'

import React from "react";

interface contextProps {
    image: [
        image: HTMLImageElement | null,
        setImage: (e: HTMLImageElement | null) => void
    ]
}

const AppContext = React.createContext<contextProps | null>(null);
export default AppContext;






