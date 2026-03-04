import { authRequest} from "../util";
import { LoginDTO } from "./types.js";

export function loginService(payload: LoginDTO) {
  return authRequest("/api/auth/login", payload);
}