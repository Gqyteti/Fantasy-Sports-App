import React from "react";

interface FilterBarProps {
  positionFilter: string;
  setPositionFilter: (position: string) => void;
}

const FilterBar: React.FC<FilterBarProps> = ({ positionFilter, setPositionFilter }) => {
  return (
    <div style={{ marginBottom: "20px" }}>
      <label htmlFor="position" style={{ marginRight: "10px", fontWeight: "bold" }}>
        Filter by Position:
      </label>
      <select
        id="position"
        value={positionFilter}
        onChange={(e) => setPositionFilter(e.target.value)}
        style={{
          padding: "8px",
          borderRadius: "5px",
          border: "1px solid #ccc",
          minWidth: "120px",
        }}
      >
        <option value="">All</option>
        <option value="QB">QB</option>
        <option value="RB">RB</option>
        <option value="WR">WR</option>
        <option value="TE">TE</option>
      </select>
    </div>
  );
};

export default FilterBar;
