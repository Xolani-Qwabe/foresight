import { useMutation, useQueryClient } from "@tanstack/react-query";
import { loginService } from "./service";
import { useAuth} from "../authContext";
import { useRouter } from "next/navigation";



export function useLogin() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { setUser , setI} = useAuth();
;
  return useMutation({
    mutationFn: loginService,
    onSuccess: (data) => {
      console.log("Login successful:", data);

      // Update both the query cache and context
      if (data?.user) {
        queryClient.setQueryData(["auth", "user"], data.user);
        setUser(data.user);
        setUser(data.user.isAuthenticated == true); // Context still updates immediately
      }
      
      router.push("/dashboard");
    },
    onError: (error) => {
      console.error("Login failed:", error);
    },
  });
}
