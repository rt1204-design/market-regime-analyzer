import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ReferenceLine, CartesianGrid } from "recharts";

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
        <LineChart width={600} height={300} data={data}>
        <CartesianGrid strokeDasharray="1 1" stroke="#080808" />
        <XAxis dataKey="date" tick={false} tickLine={false} axisLine={false} height={0} />
       <YAxis unit="%" tickCount={5} tick={{ fontSize: 10, fill: "#9ca3af" }} tickLine={false} axisLine={false} />
        <Tooltip 
          contentStyle={{
            background: "#ffffff",
             border: "1px solid #e5e7eb",
              borderRadius: "6px",
              fontSize: "12px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.08)",
            }}
            labelStyle={{ color: "#050505", marginBottom: "3px", textAlign: "center", }}
             formatter={(value) => [
                typeof value === "number" ? `${value.toFixed(3)}%` : "—",
                "Divergence",
              ]} 
            />
        <ReferenceLine y={0} stroke="#070707" />
        <Line
          type="monotone"
          dataKey="divergence"
          stroke="#000000"
          strokeWidth={1.0}
          dot={false}
        />
      </LineChart>
    </div>
  );
}

export default App;