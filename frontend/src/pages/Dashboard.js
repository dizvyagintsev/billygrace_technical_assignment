import React, { useState } from "react";
import { Helmet } from "react-helmet-async";
import { Container, Typography, Box, Grid, Card } from "@mui/material";
import { useSettingsContext } from "../components/settings";
import { Event } from "../api/api";
import dayjs from "dayjs";
import BubbleChartComponent from "../components/buble-chart/BubleChart";
import LineChartComponent from "../components/line-chart/LineChart";
import Filters from "../components/filters/Filters";
import MetricsDataGrid from "../components/metrics-data-grid/MetricsDataGrid";

export default function Dashboard() {
  const { themeStretch } = useSettingsContext();
  const [selectedEvent, setSelectedEvent] = useState(Event.ORDER_COMPLETED);
  const [dateRange, setDateRange] = useState([
    dayjs("2024-05-15"),
    dayjs("2024-07-05"),
  ]);

  const handleEventChange = (event) => {
    setSelectedEvent(event.target.value);
  };

  const handleDateRangeChange = (newValue) => {
    setDateRange(newValue);
  };

  return (
    <>
      <Helmet>
        <title>Dashboard | Minimal UI</title>
      </Helmet>

      <Container maxWidth={themeStretch ? false : "xl"}>
        <Typography variant="h3" component="h1" paragraph>
          Dashboard
        </Typography>
        <Box sx={{ mb: 3 }}>
          <Filters
            selectedEvent={selectedEvent}
            dateRange={dateRange}
            onEventChange={handleEventChange}
            onDateRangeChange={handleDateRangeChange}
          />
        </Box>
        <Card>
          <MetricsDataGrid event={selectedEvent} dateRange={dateRange} />
        </Card>
        <Box sx={{ mt: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
              <Card>
                <LineChartComponent />
              </Card>
            </Grid>
            <Grid item xs={12} md={6}>
              <Card>
                <BubbleChartComponent />
              </Card>
            </Grid>
          </Grid>
        </Box>
      </Container>
    </>
  );
}
