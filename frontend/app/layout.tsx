import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "DarkScryC2",
  description: "DarkScryc2 managment",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;

}>) {
  return (
    <html lang="en">
      <body>
        {children}
      </body>
    </html>
  );
}
