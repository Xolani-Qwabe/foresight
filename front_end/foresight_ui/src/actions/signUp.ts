"use server";


import { signupSchema } from "@/app/schemas/signupSchema";
import z from "zod";

export async function createUser(unsafeData: z.infer<typeof signupSchema>) {
    const parsedData = signupSchema.parse(unsafeData);
    if (!parsedData.success) {
        throw new Error("Invalid signup data");
        // Handle db lookup and authentication here
    }
    return {success: true, message: "Signup successful"};
}