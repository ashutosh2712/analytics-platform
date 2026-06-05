"use client";

import Link from "next/link";

import { useRouter } from "next/navigation";

import { logout } from "@/lib/auth";

const Navbar = () => {
  const router = useRouter();

  const handleLogout = () => {
    logout();

    router.push("/login");
  };

  return (
    <nav className="bg-black text-white px-8 py-4 flex justify-between items-center">
      <Link href="/dashboards" className="text-xl font-bold">
        Analytics Platform
      </Link>

      <div className="flex gap-4 items-center">
        <Link href="/settings/api-keys" className="hover:underline">
          API Keys
        </Link>

        <Link href="/ingest" className="hover:underline">
          Ingest
        </Link>

        <Link href="/dashboards" className="hover:underline">
          Dashboards
        </Link>

        <button
          onClick={handleLogout}
          className="bg-white text-black px-4 py-2 rounded-lg"
        >
          Logout
        </button>
      </div>
    </nav>
  );
};

export default Navbar;
