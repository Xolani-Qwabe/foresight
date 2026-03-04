export const logoutService = async () => {
  return await fetch("/api/auth/logout", {
    method: "POST",
    credentials: "include",
  }).then((res) => res.json());
};