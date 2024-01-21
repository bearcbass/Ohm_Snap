'use client'
import AppContext from "./createContext";
import React from "react";

const AppContextProvider = (props: {
    children: React.ReactElement<any, string | React.JSXElementConstructor<any>>;
}) => {
    const [image, setImage] = React.useState<HTMLImageElement | null>(null);

    return(
        <AppContext.Provider value={{image: [image, setImage]}}>
            {props.children}
        </AppContext.Provider>
    );
}

export default AppContextProvider;