"use client";

import { Controller, useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { loginSchema } from "@/app/schemas/loginSchema";
import { toast } from "react-hot-toast";
import { useEffect, useState } from "react";

import {
  FieldGroup,
  Field,
  FieldError,
  FieldLabel,
  FieldSeparator,
} from "../../components/ui/field";

import { Input } from "@base-ui/react";
import { User, Lock, Chrome, Github, Facebook } from "lucide-react";
import MyButton from "./MyButton";

const LoginForm = () => {
  const [isClient, setIsClient] = useState(false);
  
  const form = useForm<z.infer<typeof loginSchema>>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      username: "",
      password: "",
    },
  });

  useEffect(() => {
    setIsClient(true);
  }, []);

  async function onSubmit(data: z.infer<typeof loginSchema>) {
    console.log("Login Data:", data);
    toast.success("Login successful!");
    form.reset();
  }

  const handleSocialLogin = (provider: "google" | "github" | "facebook") => {
    console.log(`Social login with ${provider}`);
    toast.success(`Logging in with ${provider}`);
  };

  if (!isClient) {
    return (
      <div className="container max-w-[450px] px-4 mx-auto my-6 bg-background-layer-1 p-4 rounded-lg shadow-raised">
        <div className="h-[400px] animate-pulse" />
      </div>
    );
  }

  return (
    <div className="container max-w-[450px] px-4 mx-auto my-6 bg-background-layer-1 p-4 rounded-lg shadow-raised">
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FieldGroup>

          {/* Username/Email */}
          <Controller
            control={form.control}
            name="username"
            render={({ field, fieldState }) => (
              <Field data-invalid={fieldState.invalid}>
                <FieldLabel>Username or Email</FieldLabel>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 text-foreground/50" />
                  <Input 
                    {...field} 
                    suppressHydrationWarning
                    className="w-full pl-10 p-3 border border-foreground/50 rounded-full focus:outline-none focus:ring-2 focus:ring-primary/50 shadow-inset" 
                    placeholder="Enter username or email"
                  />
                </div>
                <FieldError errors={[fieldState.error]} />
              </Field>
            )}
          />

          {/* Password */}
          <Controller
            control={form.control}
            name="password"
            render={({ field, fieldState }) => (
              <Field data-invalid={fieldState.invalid}>
                <FieldLabel>Password</FieldLabel>
                <div className="relative">
                  <Lock className="absolute left-3 top-1/2 -translate-y-1/2 text-foreground/50" />
                  <Input
                    type="password"
                    {...field}
                    suppressHydrationWarning
                    className="w-full pl-10 p-3 border border-foreground/50 rounded-full focus:outline-none focus:ring-2 focus:ring-primary/50 shadow-inset"
                    placeholder="Enter your password"
                  />
                </div>
                <FieldError errors={[fieldState.error]} />
              </Field>
            )}
          />

          {/* Remember me & Forgot password */}
          <div className="flex items-center justify-between mb-4">
            <label className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                className="w-4 h-4 text-primary border border-foreground/50 rounded-full focus:outline-none focus:ring-2 focus:ring-primary/50 shadow-inset"
                suppressHydrationWarning
              />
              <span className="text-sm text-foreground/70">Remember me</span>
            </label>
            <a 
              href="#" 
              className="text-sm text-primary hover:text-primary/80 transition-colors"
              onClick={(e) => {
                e.preventDefault();
                toast.success("Forgot password link clicked!");
              }}
              suppressHydrationWarning
            >
              Forgot password?
            </a>
          </div>

          {/* Login Submit Button */}
          <MyButton
            name="Sign In"
            color="from-primary/5 to-primary/35"
            text="text-white"
            icon={null}
            rounded="rounded-full"
            type="submit"
          />

          {/* Field Separator */}
          <FieldSeparator>
            <span className="text-foreground/50 text-sm px-4 rounded-full">or continue with</span>
          </FieldSeparator>

          {/* Social Buttons */}
          <div className="flex gap-2 justify-center">
            <MyButton
              name=""
              color="from-red-500/30 to-red-600/50"
              text="text-white"
              icon={<Chrome size={20} />}
              rounded="rounded-full"
              type="button"
              onClick={() => handleSocialLogin("google")}
            />

            <MyButton
              name=""
              color="from-neutral-700/40 to-neutral-900/60"
              text="text-white"
              icon={<Github size={20} />}
              rounded="rounded-full"
              type="button"
              onClick={() => handleSocialLogin("github")}
            />

            <MyButton
              name=""
              color="from-blue-500/30 to-blue-700/50"
              text="text-white"
              icon={<Facebook size={20} />}
              rounded="rounded-full"
              type="button"
              onClick={() => handleSocialLogin("facebook")}
            />
          </div>

          {/* Sign up link */}
          <div className="text-center mt-4 pt-4 border-t border-foreground/10">
            <p className="text-sm text-foreground/70">
              Don't have an account?{" "}
              <a 
                href="#" 
                className="text-primary hover:text-primary/80 font-medium transition-colors"
                onClick={(e) => {
                  e.preventDefault();
                  toast.success("Redirect to sign up page!");
                }}
                suppressHydrationWarning
              >
                Sign up
              </a>
            </p>
          </div>

        </FieldGroup>
      </form>
    </div>
  );
};

export default LoginForm;