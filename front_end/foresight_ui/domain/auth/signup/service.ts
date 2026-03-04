import { authRequest } from "../util";
import { SignUpDTO } from "./types.js";

export function signUpService(payload: SignUpDTO) {
  return authRequest("/api/auth/register", payload);
}