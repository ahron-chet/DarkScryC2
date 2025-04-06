// pages/api/me.ts (Next.js 12 style) 
// app/api/me/route.ts
import { NextRequest, NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";

export async function GET(req: NextRequest) {
  const session = await getServerSession(authOptions);
  if (!session) {
    return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  }
  return NextResponse.json({
    email: session.user.email,
    user_id: session.user.id,
    first_name: session.user.first_name,
    last_name: session.user.last_name,
    role: session.user.role
  });
}
