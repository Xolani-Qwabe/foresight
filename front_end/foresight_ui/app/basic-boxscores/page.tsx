// app/basic-box-scores/page.tsx
"use client";

import React, { useState, useEffect } from "react";
import { BasicBoxScore, columns } from "./columns";
import { DataTable } from "@/components/data-table";

const Page = () => {
  const [data, setData] = useState<BasicBoxScore[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Dynamically import the JSON (loads on client-side)
    import("../../sampleData/basic_box_scores.json")
      .then((module) => {
        setData(module.default as BasicBoxScore[]);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Failed to load data:", error);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <section className="py-24">
        <div className="container">
          <h1 className="text-3xl font-bold">Basic Box Scores</h1>
          <div className="text-center py-8">Loading data...</div>
        </div>
      </section>
    );
  }

  return (
    <section className="flex flex-col py-24">
      <div className="w-[100%] border border-black flex flex-col item-center justify-center ">
        <h1 className="text-3xl font-bold">Basic Box Scores</h1>
        <div className="flex item-center justify-center w-[100%] border border-green">
          <DataTable columns={columns} data={data} />
        </div>
      </div>
    </section>
  );
};

export default Page;
