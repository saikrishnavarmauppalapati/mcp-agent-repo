import { useEffect, useState } from "react";
import { signIn, signOut, useSession, getSession } from "next-auth/react";
import axios from "axios";

export default function Home() {
  const { data: session } = useSession();
  const [message, setMessage] = useState("");

  const handleSearch = async () => {
    const query = prompt("Enter search query:");
    if (!query) return;

    try {
      const token = session?.accessToken;
      const response = await axios.post(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/tools/youtube.search/invoke`,
        { input: { q: query, max: 5 }, token },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setMessage(JSON.stringify(response.data.result, null, 2));
    } catch (err: any) {
      setMessage(err.response?.data || err.message);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 p-4">
      <h1 className="text-3xl font-bold mb-4">MCP YouTube AI Agent</h1>

      {!session ? (
        <button
          onClick={() => signIn("google")}
          className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
        >
          Login with Google
        </button>
      ) : (
        <div className="flex items-center gap-4">
          <img
            src={session.user?.image || ""}
            alt="Profile"
            className="w-10 h-10 rounded-full"
          />
          <span>{session.user?.name}</span>
          <button
            onClick={() => signOut()}
            className="bg-red-500 text-white px-4 py-1 rounded-lg hover:bg-red-600"
          >
            Logout
          </button>
        </div>
      )}

      {session && (
        <button
          onClick={handleSearch}
          className="mt-6 bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700"
        >
          Search YouTube
        </button>
      )}

      {message && (
        <pre className="mt-6 w-full max-w-xl bg-gray-100 p-4 rounded-lg overflow-auto">
          {message}
        </pre>
      )}
    </div>
  );
}
