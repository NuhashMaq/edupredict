import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      // Enables utilities like h-130 / w-130 (Tailwind spacing scale), used by aceternity-style components.
      spacing: {
        90: "22.5rem", // 360px
        110: "27.5rem", // 440px
        120: "30rem", // 480px
        128: "32rem", // 512px
        130: "32.5rem", // 520px
        136: "34rem", // 544px
        180: "45rem", // 720px
        220: "55rem" // 880px
      }
    }
  },
  plugins: []
};

export default config;
