import Link from "next/link";


const Navbar = (props: {
  children: React.ReactElement<any, string | React.JSXElementConstructor<any>>;
}
) => {
   return (
    <div className="absolute top-0 bg-white w-full h-16 flex items-center justify-end">
      <div className="text-black mr-16">
        {props.children}
      </div>
    </div>
   )
}

export default Navbar