'use client'
import AppContextProvider from "../components/hooks/context";
import Dashboard from "./dashboard";
export default function DashboardPage() {
    return(
        <AppContextProvider>
            <Dashboard />
        </AppContextProvider>
    )
};

