import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Semora — Research Lab Matching for Purdue Students",
  description: "Upload your resume and get matched to Purdue research labs in seconds.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
