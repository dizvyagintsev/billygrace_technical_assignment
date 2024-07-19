import React, { useEffect, useState } from "react";
import { DataGrid } from "@mui/x-data-grid";
import { useAuthContext } from "../../auth/useAuthContext";
import { getMetrics } from "../../api/api";

export default function MetricsDataGrid({ event, dateRange }) {
  const [rows, setRows] = useState([]);
  const { user } = useAuthContext();

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const data = await getMetrics(
          user?.customerId,
          event,
          dateRange[0].format("YYYY-MM-DD"),
          dateRange[1].format("YYYY-MM-DD")
        );
        const formattedData = data.map((item, index) => ({
          id: index + 1,
          ad_copy: item.ad_copy,
          spend: item.spend,
          clicks: item.clicks,
          impressions: item.impressions,
          sessions: item.sessions,
          roas: item.roas,
        }));
        setRows(formattedData);
      } catch (error) {
        console.error("There was an error fetching the data!", error);
      }
    };
    void fetchMetrics();
  }, [event, dateRange, user?.customerId]);

  const columns = [
    {
      field: "ad_copy",
      headerName: "Ad Copy",
      flex: 3,
      headerAlign: "center",
      align: "center",
    },
    {
      field: "spend",
      headerName: "Spend",
      flex: 1,
      headerAlign: "center",
      align: "center",
    },
    {
      field: "clicks",
      headerName: "Clicks",
      flex: 1,
      headerAlign: "center",
      align: "center",
    },
    {
      field: "impressions",
      headerName: "Impressions",
      flex: 1,
      headerAlign: "center",
      align: "center",
    },
    {
      field: "sessions",
      headerName: "Sessions",
      flex: 1,
      headerAlign: "center",
      align: "center",
    },
    {
      field: "roas",
      headerName: "ROAS",
      flex: 1,
      headerAlign: "center",
      align: "center",
    },
  ];

  return <DataGrid rows={rows} columns={columns} autoHeight />;
}
