// domain/auth/signup/hook.ts
import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { signUpService } from "./service";
import { useAuth } from "../authContext";
import { SignUpDTO } from "./types";

export function useSignUp() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { setUser } = useAuth();

  return useMutation({
    mutationFn: signUpService,
    onSuccess: (data) => {
      console.log("Sign up successful:", data);
      
      // Update both the query cache and context
      if (data?.user) {
        queryClient.setQueryData(['auth', 'user'], data.user);
        setUser(data.user); // Context still updates immediately
      }

      router.push("/dashboard");
    },
    onError: (error) => {
      console.error("Sign up failed:", error);
    },
  });
}
