"use client";

import { ColumnDef } from "@tanstack/react-table";

export type BasicBoxScore = {
    player: string;
    team: string;
    game_date: string | Date;
    minutes_played: number;
    fg_made: number;
    fg_attempted: number;
    fg_pct: number;
    three_pt_made: number;
    three_pt_attempted: number;
    three_pt_pct: number;
    free_throws_made: number;
    free_throws_attempted: number;
    free_throw_pct: number;
    off_rebounds: number;
    def_rebounds: number;
    total_rebounds: number;
    turnovers: number;
    personal_fouls: number;
    points: number;
    plus_minus_score: number;
    away_team: string;
};

export const columns: ColumnDef<BasicBoxScore>[] = [
    { accessorKey: "player", header: "Player" },
    { accessorKey: "team", header: "Team" },
    { accessorKey: "game_date", header: "Game Date" },
    { accessorKey: "minutes_played", header: "MP" },
    { accessorKey: "fg_made", header: "FG Made" },
    { accessorKey: "fg_attempted", header: "FG Att" },
    { accessorKey: "fg_pct", header: "FG%" },
    { accessorKey: "three_pt_made", header: "3PT Made" },
    { accessorKey: "three_pt_attempted", header: "3PT Att" },
    { accessorKey: "three_pt_pct", header: "3PT%" },
    { accessorKey: "free_throws_made", header: "FT Made" },
    { accessorKey: "free_throws_attempted", header: "FT Att" },
    { accessorKey: "free_throw_pct", header: "FT%" },
    { accessorKey: "off_rebounds", header: "OREB" },
    { accessorKey: "def_rebounds", header: "DREB" },
    { accessorKey: "total_rebounds", header: "REB" },
    { accessorKey: "turnovers", header: "TO" },
    { accessorKey: "personal_fouls", header: "PF" },
    { accessorKey: "points", header: "PTS" },
    { accessorKey: "plus_minus_score", header: "+/-" },
    { accessorKey: "away_team", header: "Away Team" },
];
