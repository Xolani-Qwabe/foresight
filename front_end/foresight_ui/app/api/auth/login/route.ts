
import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    // Call backend
    const backendResponse = await fetch("http://127.0.0.1:8000/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
      credentials: "include"
    });

 
    const data = await backendResponse.json().catch(() => null);


    if (!backendResponse.ok) {
      return NextResponse.json(
        { error: data?.detail || "Login failed" },
        { status: backendResponse.status }
      );
    }


    const response = NextResponse.json(data);

 
    const setCookieHeaders = backendResponse.headers.get("set-cookie");
    if (setCookieHeaders) {
      
      const cookies = setCookieHeaders.split(/,(?=\s*\w+=)/);
      cookies.forEach((cookie) => response.headers.append("set-cookie", cookie));
    }

    return response;

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (error: any) {
    return NextResponse.json(
      { error: error.message || "Something went wrong" },
      { status: 500 }
    );
  }
}