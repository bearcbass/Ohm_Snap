import Link from "next/link";


const Navbar = (props: {
  header: string;
  children: React.ReactElement<any, string | React.JSXElementConstructor<any>>;
}
) => {
   return (
    <div className="absolute top-0 bg-white w-full h-16 flex items-center justify-end">
      <div className="mr-auto flex flex-row items-center">
        <a href="/" className="ml-8 flex items-center justify-center">
          <img src="/logo.png" className="black rounded-md border-2 h-10 w-10 rotate-90"/>
        </a>
      <div className="animate-fade-in ml-4 text-slate-600 font-display">{props.header}</div>

      </div>
      <div className="text-black mr-16">
        {props.children}
      </div>
    </div>
   )
}

export default Navbar