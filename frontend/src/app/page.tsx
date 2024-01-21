import Image from "next/image";
import Particles from "./components/particles"
import Navbar from "./components/navbar";
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-row items-center justify-center w-screen h-screen overflow-hidden bg-gradient-to-tl from-black via-zinc-600/20 to-black">
      <Particles
        className="absolute inset-0 -z-10 animate-fade-in-instant"
        quantity={500}
        staticity={100}
      />
      <Navbar>
        <Link href='/api/auth/login'>Login</Link>
      </Navbar>
      <div>
      </div>
      <h1 className="bg-white absolute top-1/2 left-1/2 z-10 p-1 bg-clip-text text-transparent white duration-100 cursor-default font-display text-3xl md:text-5xl xl:text-7xl animate-fade-in whitespace-nowrap transform -translate-x-1/2 -translate-y-1/2">
        Ohm Snap!
      </h1>
      </div>
  );
}
