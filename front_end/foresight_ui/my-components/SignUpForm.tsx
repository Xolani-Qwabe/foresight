"use client";

import { Controller, useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import { signupSchema } from "@/app/schemas/signupSchema";
import { createUser } from "@/src/actions/signUp";
import { toast } from "react-hot-toast";

import {
  FieldGroup,
  Field,
  FieldError,
  FieldLabel,
  FieldSeparator,
} from "../../components/ui/field";

import { Input } from "@base-ui/react";
import { User, Mail, Phone, Lock, Chrome, Github, Facebook } from "lucide-react";
import MyButton from "./MyButton";

const SignUpForm = () => {
  const form = useForm<z.infer<typeof signupSchema>>({
    resolver: zodResolver(signupSchema),
    defaultValues: {
      username: "",
      email: "",
      phone: "",
      password: "",
      provider: undefined,
    },
  });

  async function onSubmit(data: z.infer<typeof signupSchema>) {
    const res = await createUser(data);

    if (res.success) {
      form.reset();
      toast.success("Signup successful");
    } else {
      toast.error(`Signup failed: ${res.message}`);
    }
  }

  const handleSocialSignup = (provider: "google" | "github" | "facebook") => {
    form.setValue("provider", provider);
    form.handleSubmit(onSubmit)();
  };

  return (
    <div className="container max-w-[450px] px-4 mx-auto my-6 bg-background-layer-1 p-4 rounded-lg shadow-raised">
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FieldGroup>

          {/* Username */}
          <Controller
            control={form.control}
            name="username"
            render={({ field, fieldState }) => (
              <Field data-invalid={fieldState.invalid}>
                <FieldLabel>Username</FieldLabel>
                <div className="relative">
                  <User className="absolute left-3 top-1/2 -translate-y-1/2 text-foreground/50" />
                  <Input {...field} className="w-full pl-10 p-3 border border-foreground/50 rounded-full focus:outline-none focus:ring-2 focus:ring-primary/50 shadow-inset" />
                </div>
                <FieldError errors={[fieldState.error]} />
              </Field>
            )}
          />

          {/* Email */}
          <Controller
            control={form.control}
            name="email"
            render={({ field, fieldState }) => (
              <Field data-invalid={fieldState.invalid}>
                <FieldLabel>Email</FieldLabel>
                <div className="relative">
                  <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-foreground/50" />
                  <Input {...field} className="w-full pl-10 p-3 border border-foreground/50 rounded-full focus:outline-none focus:ring-2 focus:ring-primary/50 shadow-inset" />
                </div>
                <FieldError errors={[fieldState.error]} />
              </Field>
            )}
          />

          {/* Phone */}
          <Controller
            control={form.control}
            name="phone"
            render={({ field, fieldState }) => (
              <Field data-invalid={fieldState.invalid}>
                <FieldLabel>Phone</FieldLabel>
                <div className="relative">
                  <Phone className="absolute left-3 top-1/2 -translate-y-1/2 text-foreground/50" />
                  <Input {...field} className="w-full pl-10 p-3 border border-foreground/50 rounded-full focus:outline-none focus:ring-2 focus:ring-primary/50 shadow-inset" />
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
                    className="w-full pl-10 p-3 border border-foreground/50 rounded-full focus:outline-none focus:ring-2 focus:ring-primary/50 shadow-inset"
                  />
                </div>
                <FieldError errors={[fieldState.error]} />
              </Field>
            )}
          />

          {/* Primary Submit */}
          <MyButton
            name="Create Account"
            color="from-primary/5 to-primary/35"
            text="text-white"
            icon={null}
            rounded="rounded-full"
            type="submit"
          />

          {/* Field Separator */}
          <FieldSeparator>
            <span className="text-foreground/50 text-sm px-2">or continue with</span>
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
              onClick={() => handleSocialSignup("google")}
            />

            <MyButton
              name=""
              color="from-neutral-700/40 to-neutral-900/60"
              text="text-white"
              icon={<Github size={20} />}
              rounded="rounded-full"
              type="button"
              onClick={() => handleSocialSignup("github")}
            />

            <MyButton
              name=""
              color="from-blue-500/30 to-blue-700/50"
              text="text-white"
              icon={<Facebook size={20} />}
              rounded="rounded-full"
              type="button"
              onClick={() => handleSocialSignup("facebook")}
            />
          </div>

        </FieldGroup>
      </form>
    </div>
  );
};

export default SignUpForm;