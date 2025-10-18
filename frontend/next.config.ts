import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "im.runware.ai",
      },
      {
        protocol: "https",
        hostname: "vm.runware.ai",
      },
    ],
  },
};

export default nextConfig;
