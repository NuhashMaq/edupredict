import type { Metadata } from "next";
import { Sora, Space_Grotesk } from "next/font/google";
import "@/styles/globals.css";

import { AcademicScrollBackground } from "@/components/ui/AcademicScrollBackground";
import { Footer } from "@/components/site/Footer";

const space = Space_Grotesk({
  subsets: ["latin"],
  variable: "--font-space",
  display: "swap"
});

const logo = Sora({
  subsets: ["latin"],
  variable: "--font-logo",
  display: "swap"
});

export const metadata: Metadata = {
  title: "EduPredict — AI Student Performance Predictor",
  description: "Explainable AI risk prediction for student performance."
};

export default function RootLayout({
  children
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${space.variable} ${logo.variable}`} suppressHydrationWarning>
      <body className="min-h-screen bg-(--edp-bg) text-(--edp-ink) antialiased text-[18px] md:text-[19px] lg:text-[20px]">
        <AcademicScrollBackground />
        <div id="__edupredict" data-app-root className="relative z-10 flex min-h-screen flex-col">
          <div className="flex-1">{children}</div>
          <Footer />
        </div>
      </body>
    </html>
  );
}
