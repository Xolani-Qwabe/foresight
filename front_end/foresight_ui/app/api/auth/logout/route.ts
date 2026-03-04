import { NextResponse } from "next/server";

export async function POST() {
  try {
    const backendResponse = await fetch(
      "http://127.0.0.1:8000/api/auth/logout",
      {
        method: "POST",
        credentials: "include",
      }
    );

    const response = NextResponse.json({ success: true });

    // Forward any cookies (including cleared cookies)
    const setCookieHeaders = backendResponse.headers.get("set-cookie");
    if (setCookieHeaders) {
      const cookies = setCookieHeaders.split(/,(?=\s*\w+=)/);
      cookies.forEach((cookie) =>
        response.headers.append("set-cookie", cookie)
      );
    }

    return response;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || "Logout failed" },
      { status: 500 }
    );
  }
}