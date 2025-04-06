import type { Metadata } from "next";
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";

export const metadata: Metadata = {
  title: "DarkScryC2",
  description: "DarkScryc2 managment",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
  
}>) {
  const session = await getServerSession(authOptions);
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
