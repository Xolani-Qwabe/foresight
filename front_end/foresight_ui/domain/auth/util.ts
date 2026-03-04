export async function authRequest<T>(url: string, body: unknown): Promise<T> {
  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    credentials: "include", 
    redirect: "manual",
  });

  const data = await res.json().catch(() => null);

  if (!res.ok) {
    console.error("API Error Response:", data, "Status:", res.status);
    throw new Error(data?.error || data?.message || `Request failed (${res.status})`);
  }

  return data;
}