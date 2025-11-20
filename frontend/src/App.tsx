import React, { useState } from "react";
import PlayerTable from "./components/PlayerTable";
import FilterBar from "./components/FilterBar";

function App() {
  const [positionFilter, setPositionFilter] = useState("");

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Fantasy Sports Player Data Tracker</h1>
      <FilterBar positionFilter={positionFilter} setPositionFilter={setPositionFilter} />
      <PlayerTable positionFilter={positionFilter} />
    </div>
  );
}

export default App;
