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
      <div style={{ padding: 40 }}>
        <h1>Login with Google to use MCP Agent</h1>
        <button onClick={() => signIn("google")}>Login</button>
      </div>
    );
  }

  return (
    <div style={{ padding: 20 }}>
      <h1>Welcome, {session.user?.name}</h1>
      <button onClick={() => signOut()}>Logout</button>

      <div style={{ marginTop: 20 }}>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search YouTube"
          style={{ marginRight: 10 }}
        />
        <button onClick={search}>Search</button>
      </div>

      <div style={{ marginTop: 20 }}>
        {results.map((video: any) => (
          <div key={video.id} style={{ marginBottom: 15, border: "1px solid #ccc", padding: 10 }}>
            <h3>{video.title}</h3>
            <p>{video.description}</p>
            <small>Channel: {video.channel}</small>
          </div>
        ))}
      </div>
    </div>
  );
}
