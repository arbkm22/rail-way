import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Indian Railways Route Finder",
  description: "Find train routes across India with interactive map visualization",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
