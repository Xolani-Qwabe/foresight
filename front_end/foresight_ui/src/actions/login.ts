"use server";

import { loginSchema } from "@/app/schemas/loginSchema";
import z from "zod";

export async function loginAction(unsafeData: z.infer<typeof loginSchema>) {
    const parsedData = loginSchema.parse(unsafeData);
    if (!parsedData.success) {
        throw new Error("Invalid login data");
        // Handle db lookup and authentication here
    }
    return {success: true, message: "Login successful"};
}