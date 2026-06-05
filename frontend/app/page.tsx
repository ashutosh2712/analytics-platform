import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      <div className="text-center">
        <h1 className="text-6xl font-bold mb-6">Analytics Platform</h1>

        <p className="text-xl text-gray-600 mb-8">
          Real-time event analytics dashboards
        </p>

        <Link
          href="/login"
          className="bg-black text-white px-8 py-4 rounded-xl text-lg"
        >
          Get Started
        </Link>
      </div>
    </div>
  );
}
