import React, { useEffect, useState } from "react";

interface Player {
  id: number;
  name: string;
  team: string;
  position: string;
  projection: number;
}

interface PlayerTableProps {
  positionFilter: string;
}

const PlayerTable: React.FC<PlayerTableProps> = ({ positionFilter }) => {
  const [players, setPlayers] = useState<Player[]>([]);

  // Fetch players from backend when component mounts
  useEffect(() => {
    fetch("http://127.0.0.1:5000/api/players")
      .then((res) => res.json())
      .then((data) => setPlayers(data.players))
      .catch((err) => console.error("Error fetching players:", err));
  }, []);

  const filteredPlayers = positionFilter
    ? players.filter((p) => p.position === positionFilter)
    : players;

  return (
    <table style={{ width: "100%", borderCollapse: "collapse", marginTop: "20px" }}>
      <thead style={{ backgroundColor: "#1976d2", color: "white" }}>
        <tr>
          <th style={{ padding: "10px", textAlign: "left" }}>Name</th>
          <th style={{ padding: "10px", textAlign: "left" }}>Team</th>
          <th style={{ padding: "10px", textAlign: "left" }}>Position</th>
          <th style={{ padding: "10px", textAlign: "left" }}>Projection</th>
        </tr>
      </thead>
      <tbody>
        {filteredPlayers.map((player) => (
          <tr key={player.id} style={{ borderBottom: "1px solid #ccc" }}>
            <td style={{ padding: "10px" }}>{player.name}</td>
            <td style={{ padding: "10px" }}>{player.team}</td>
            <td style={{ padding: "10px" }}>{player.position}</td>
            <td style={{ padding: "10px" }}>{player.projection}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default PlayerTable;
