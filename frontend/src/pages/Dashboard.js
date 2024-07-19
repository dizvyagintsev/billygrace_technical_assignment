import React, { useState } from 'react';
import { Helmet } from 'react-helmet-async';
import {Box, Container, Typography} from '@mui/material';
import { useSettingsContext } from '../components/settings';
import { Event } from '../api/api';
import dayjs from 'dayjs';
import Filters from "../components/filters/Filters";
import MetricsDataGrid from "../components/metrics-data-grid/MetricsDataGrid";
import BubbleChartComponent from "../components/buble-chart/BubleChart";
import LineChartComponent from "../components/line-chart/LineChart";

export default function Dashboard() {
  const { themeStretch } = useSettingsContext();
  const [selectedEvent, setSelectedEvent] = useState(Event.ORDER_COMPLETED);
  const [dateRange, setDateRange] = useState([dayjs('2024-05-15'), dayjs('2024-07-05')]);

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

      <Container maxWidth={themeStretch ? false : 'xl'}>
        <Typography variant="h3" component="h1" paragraph>
          Dashboard
        </Typography>
        <Filters
          selectedEvent={selectedEvent}
          dateRange={dateRange}
          onEventChange={handleEventChange}
          onDateRangeChange={handleDateRangeChange}
        />
        <MetricsDataGrid event={selectedEvent} dateRange={dateRange} />
        <Typography variant="h2" component="h2" paragraph>
          Plots
        </Typography>
        <LineChartComponent />
        <BubbleChartComponent />
        {/*<Box sx={{ mt: 3 }}>*/}
        {/*  <Typography variant="h4" component="h2" paragraph>*/}
        {/*    Line Chart*/}
        {/*  </Typography>*/}
        {/*  <LineChartComponent />*/}
        {/*</Box>*/}
        {/*<Box sx={{ mt: 3 }}>*/}
        {/*  <Typography variant="h4" component="h2" paragraph>*/}
        {/*    Bubble Chart*/}
        {/*  </Typography>*/}
        {/*  <BubbleChartComponent />*/}
        {/*</Box>*/}
      </Container>
    </>
  );
}
