import { NextRequest, NextResponse } from "next/server";

export async function GET(req: NextRequest) {
  try {
    const backendResponse = await fetch(
      "http://127.0.0.1:8000/api/auth/session",
      {
        headers: {
          Cookie: req.headers.get("cookie") || "",
        },
      }
    );

    if (!backendResponse.ok) {
      return NextResponse.json({ user: null });
    }

    const data = await backendResponse.json();


    return NextResponse.json({
      user: {
        id: data.id,
        username: data.username,
        email: data.email,
      },
    });

  } catch (error) {
    console.error("Error checking session:", error);
    return NextResponse.json({ user: null });
  }
}