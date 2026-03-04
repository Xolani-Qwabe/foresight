import { NextRequest, NextResponse } from "next/server";

export async function POST(req: NextRequest) {
  try {
    const body = await req.json();

    const backendResponse = await fetch(
      "http://127.0.0.1:8000/api/auth/register",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      }
    );

    const data = await backendResponse.json();

    if (!backendResponse.ok) {
      return NextResponse.json(
        { error: data?.detail || "Registration failed" },
        { status: backendResponse.status }
      );
    }

    const response = NextResponse.json({
      success: true,
      user: {
        id: data.user?.id,
        username: data.user?.username,
        email: data.user?.email,
       

      },
     
    });
    // Forward cookies from FastAPI to browser
    const setCookie = backendResponse.headers.get("set-cookie");

    if (setCookie) {
      response.headers.set("set-cookie", setCookie);
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