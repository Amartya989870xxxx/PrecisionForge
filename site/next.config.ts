import createMDX from "@next/mdx";
import type { NextConfig } from "next";
const nextConfig: NextConfig = { pageExtensions: ["ts", "tsx", "mdx"] };
export default createMDX()(nextConfig);
