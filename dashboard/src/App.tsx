import { useState, useEffect } from "react";

type DataRow = {
  date: string;
  divergence: number;
  rolling_vol: number;
  regime: "quiet" | "normal" | "turbulent";
};

function App() {
  const [data, setData] = useState<DataRow[]>([]);

  useEffect(() => {
    fetch("/dashboard_data.json")
      .then((res) => res.json())
      .then((rows) => setData(rows));
  }, []);

  return (
    <div>
      <h1>NQ/ES Market Divergence Analyzer</h1>
      <p>Loaded {data.length} rows</p>
      <p>Latest regime: {data.at(-1)?.regime ?? "loading..."}</p>
    </div>
  );
}

export default App;