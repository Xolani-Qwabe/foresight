"use client";

import { Field } from "@/components/ui/field";
import { Mail, Lock, Chrome, Github, Facebook } from "lucide-react";
import MyButton from "./MyButton";
import Image from "next/image";
import logo from "@/public/logo.png";
import { useForm } from "react-hook-form";
import { DevTool } from "@hookform/devtools";

let renderCount = 0;

type LoginData = {
  email: string;
  password: string;
};

const LoginForm = () => {
  const form = useForm<LoginData>();
  const { register, control, handleSubmit, formState } = form;
  const { errors } = formState;

  const onSubmit = (data: LoginData) => {
    console.log("Login Data:", data);
  };

  renderCount++;

  return (
    <div className="container max-w-[450px] px-4 mx-auto my-6 bg-background-layer-1 p-6 rounded-lg shadow-raised">
      <div className="flex flex-col items-center gap-3 mb-6">
        <Image src={logo} alt="Logo" width={160} height={160} />
        {/* <h1 className="text-lg font-semibold">
          Login ({renderCount / 2})
        </h1> */}
      </div>

      <form
        className="flex flex-col gap-5"
        onSubmit={handleSubmit(onSubmit)}
        noValidate
      >
        <Field data-invalid={!!errors.email}>
          <label className="text-sm font-medium">Email</label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-foreground/50" />
            <input
              type="email"
              placeholder="email@foresight.co.za"
              {...register("email", { required: "Email is required" })}
              className="w-full pl-10 p-3 border border-foreground/50 rounded-full focus:outline-none focus:ring-2 focus:ring-primary/50 shadow-inset"
            />
          </div>
          <p className="text-red-500 text-sm mt-1">
            {errors.email?.message}
          </p>
        </Field>

        <Field data-invalid={!!errors.password}>
          <label className="text-sm font-medium">Password</label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-foreground/50" />
            <input
              type="password"
              placeholder="Password"
              {...register("password", { required: "Password is required" })}
              className="w-full pl-10 p-3 border border-foreground/50 rounded-full focus:outline-none focus:ring-2 focus:ring-primary/50 shadow-inset"
            />
          </div>
          <p className="text-red-500 text-sm mt-1">
            {errors.password?.message}
          </p>
        </Field>

        <MyButton
          name="Login"
          color="from-primary/5 to-primary/35"
          text="text-white"
          icon={null}
          rounded="rounded-full"
          type="submit"
        />

        <div className="flex items-center gap-3 my-3">
          <div className="flex-1 h-px bg-foreground/20" />
          <span className="text-foreground/50 text-sm">
            or continue with
          </span>
          <div className="flex-1 h-px bg-foreground/20" />
        </div>

        <div className="flex gap-3 justify-center">
          <MyButton
            name=""
            color="from-red-500/30 to-red-600/50"
            text="text-white"
            icon={<Chrome size={20} />}
            rounded="rounded-full"
          />
          <MyButton
            name=""
            color="from-neutral-700/40 to-neutral-900/60"
            text="text-white"
            icon={<Github size={20} />}
            rounded="rounded-full"
          />
          <MyButton
            name=""
            color="from-blue-500/30 to-blue-700/50"
            text="text-white"
            icon={<Facebook size={20} />}
            rounded="rounded-full"
          />
        </div>
      </form>

      <DevTool control={control} />
    </div>
  );
};

export default LoginForm;
