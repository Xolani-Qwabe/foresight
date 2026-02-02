import { z } from "zod";

export const signupSchema = z.object({
  provider: z.enum(["google", "github", "facebook"]).optional(),

  username: z
    .string()
    .min(1, { message: "Username is required" }),

  email: z
    .string()
    .email({ message: "Invalid email address" }),

  phone: z
    .string()
    .min(10, { message: "Phone number is required" }),

  password: z
    .string()
    .min(6, { message: "Password must be at least 6 characters long" }),
});

export type SignupInput = z.infer<typeof signupSchema>;
