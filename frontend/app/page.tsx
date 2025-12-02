"use client";

import { useSession, signIn, signOut } from "next-auth/react";
import { useState } from "react";
import axios from "axios";

export default function Home() {
  const { data: session } = useSession();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  const search = async () => {
    if (!query) return;
    const res = await axios.post(`${process.env.NEXT_PUBLIC_AGENT_URL}/agent`, {
      action: "search",
      query,
      max_results: 5,
    });
    setResults(res.data);
  };

  if (!session) {
    return (
      <div>
        <h1>Login with Google to use MCP Agent</h1>
        <button onClick={() => signIn("google")}>Login</button>
      </div>
    );
  }

  return (
    <div>
      <h1>Welcome, {session.user?.name}</h1>
      <button onClick={() => signOut()}>Logout</button>

      <div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search YouTube"
        />
        <button onClick={search}>Search</button>
      </div>

      <div>
        {results.map((video: any) => (
          <div key={video.id}>
            <h3>{video.title}</h3>
            <p>{video.description}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
