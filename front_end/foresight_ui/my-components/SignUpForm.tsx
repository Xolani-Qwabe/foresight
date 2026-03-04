"use client";

import { Field } from "@/components/ui/field";
import {
  User,
  Mail,
  Lock,
  Chrome,
  Github,
  Facebook,
  Eye,
  EyeOff,
} from "lucide-react";
import { useState } from "react";
import MyButton from "./MyButton";
import Image from "next/image";
import logo from "@/public/logo.png";
import { useForm } from "react-hook-form";
import { DevTool } from "@hookform/devtools";

import { useSignUp } from "@/domain/auth/signup/hook";
import { SignUpSchema } from "@/domain/auth/signup/schema";
import { SignUpDTO } from "@/domain/auth/signup/types";

const SignUpForm = () => {
  const [showPassword, setShowPassword] = useState(false);
  const form = useForm<SignUpDTO>();
  const { register, control, handleSubmit, formState } = form;
  const { errors } = formState;

  const mutation = useSignUp();

  const onSubmit = (data: SignUpDTO) => {
    const parsed = SignUpSchema.safeParse(data);

    if (!parsed.success) {
      console.error("Validation errors:", parsed.error.format());
      return;
    }

    mutation.mutate(parsed.data, {
      onSuccess: (response) => {
        console.log("Sign up successful:", response);
      },
      onError: (error) => {
        console.error("Sign up failed:", error);
      },
    });
  };

  return (
    <div className="container max-w-[450px] px-4 mx-auto my-6 bg-background-layer-1 p-6 rounded-lg shadow-raised">
      <div className="flex flex-col items-center gap-3 mb-6">
        <Image src={logo} alt="Logo" width={160} height={160} />
        {/* <h1 className="text-lg font-semibold">
          Register ({renderCount / 2})
        </h1> */}
      </div>

      <form
        className="flex flex-col gap-5"
        onSubmit={handleSubmit(onSubmit)}
        noValidate
      >
        {/* Username */}
        <Field data-invalid={!!errors.username}>
          <label className="text-sm font-medium">Username</label>
          <div className="relative">
            <User className="absolute left-3 top-1/2 -translate-y-1/2 text-foreground/50" />
            <input
              type="text"
              placeholder="Username"
              {...register("username", {
                required: "Username is required",
              })}
              className="w-full pl-10 p-3 border border-foreground/50 rounded-full focus:outline-none focus:ring-2 focus:ring-primary/50 shadow-inset"
            />
          </div>
          <p className="text-red-500 text-sm mt-1">
            {errors.username?.message}
          </p>
        </Field>

        {/* Email */}
        <Field data-invalid={!!errors.email}>
          <label className="text-sm font-medium">Email</label>
          <div className="relative">
            <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-foreground/50" />
            <input
              type="email"
              placeholder="email@foresight.co.za"
              {...register("email", {
                required: "Email is required",
                pattern: {
                  value:
                    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$/,
                  message: "Please enter a valid email address",
                },
              })}
              className="w-full pl-10 p-3 border border-foreground/50 rounded-full focus:outline-none focus:ring-2 focus:ring-primary/50 shadow-inset"
            />
          </div>
          <p className="text-red-500 text-sm mt-1">{errors.email?.message}</p>
        </Field>

        {/* Password */}
        {/* Password */}
        <Field data-invalid={!!errors.password}>
          <label className="text-sm font-medium">Password</label>
          <div className="relative">
            <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-foreground/50" />
            <input
              type={showPassword ? "text" : "password"}
              placeholder="Password"
              {...register("password", {
                required: "Password is required",
              })}
              className="w-full pl-10 pr-10 p-3 border border-foreground/50 rounded-full focus:outline-none focus:ring-2 focus:ring-primary/50 shadow-inset"
            />
            <button
              type="button"
              onClick={() => setShowPassword((prev) => !prev)}
              className="absolute right-3 top-1/2 -translate-y-1/2 text-foreground/50 hover:text-foreground transition"
              tabIndex={-1}
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          </div>
          <p className="text-red-500 text-sm mt-1">
            {errors.password?.message}
          </p>
        </Field>

        <MyButton
          name={mutation.isPending ? "Creating..." : "Create Account"}
          color="from-primary/5 to-primary/35"
          text="text-white"
          icon={null}
          rounded="rounded-full"
          type="submit"
        />

        {/* Divider */}
        <div className="flex items-center gap-3 my-3">
          <div className="flex-1 h-px bg-foreground/20" />
          <span className="text-foreground/50 text-sm">or continue with</span>
          <div className="flex-1 h-px bg-foreground/20" />
        </div>

        {/* Social */}
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

export default SignUpForm;
