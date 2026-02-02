import Image from "next/image";
import MyButton from "./my-components/MyButton";


import LoginForm from "@/my-components/LoginForm";
import DemoPage from "./payments/page";

export default function Home() {
  return (
    <main
      className=" 
    flex 
    flex-col 
    min-h-screen 
    items-center 
    justify-center 
    gap-4 
    bg-background-layer-0 
    "
    >
 
      {/* <SignUpForm/> */}
      {/* <LoginForm/> */}
      
      <DemoPage/>
    </main>
  );
}


