import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: 'standalone', // Disable static export for dynamic routes
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
      {
        protocol: 'http',
        hostname: '**',
      },
    ],
  },
};

export default nextConfig;
