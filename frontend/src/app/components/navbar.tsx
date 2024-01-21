import Link from "next/link";


const Navbar = (props: {
  header: string;
  children: React.ReactElement<any, string | React.JSXElementConstructor<any>>;
}
) => {
   return (
    <div className="absolute top-0 bg-white w-full h-16 flex items-center justify-end">
      <div className="animate-fade-in mr-auto ml-10  text-slate-600 font-display">{props.header}</div>
      <div className="text-black mr-16">
        {props.children}
      </div>
    </div>
   )
}

export default Navbar