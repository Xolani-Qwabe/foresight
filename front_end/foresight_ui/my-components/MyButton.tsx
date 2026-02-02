// MyButton.tsx - Simplified version
import { Button } from "@base-ui/react/button";
import { ReactNode } from "react";

type MyButtonProps = {
  name: string;
  color: string;
  text: string;
  icon: ReactNode;
  rounded: string;
  type?: "button" | "submit" | "reset"; 
};

const MyButton = ({ name, color, text, icon, rounded, type = "button" }: MyButtonProps) => {
  return (
    <Button
      type={type}
      className={`
        inline-flex
        gap-2
        items-center
        justify-center
        ${text}
        font-medium
        hover:opacity-80
        focus-visible:ring-foreground
        focus-visible:ring-offset-2
        focus-visible:outline-none
        border-3
        border-background
        shadow-raised
        bg-linear-to-right
        px-4
        py-2
        ${rounded}
        cursor-pointer
        bg-gradient-to-br
        ${color}
        `}
    >
      {icon}
      {name}
    </Button>
  );
};

export default MyButton;