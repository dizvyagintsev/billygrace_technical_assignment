import React, { useEffect, useState, useCallback, useMemo } from 'react';
import { Helmet } from 'react-helmet-async';
import { Container, Typography, Box, Grid, Card, Alert, Button } from '@mui/material';
import dayjs from 'dayjs';
import axios from 'axios';
import { useSettingsContext } from '../components/settings';
import BubbleChartComponent from '../components/buble-chart/BubleChart';
import LineChartComponent from '../components/line-chart/LineChart';
import Filters from '../components/filters/Filters';
import MetricsDataGrid from '../components/metrics-data-grid/MetricsDataGrid';

export default function Dashboard() {
  const { themeStretch } = useSettingsContext();

  // Memoize initial values from localStorage and ensure they are dayjs objects
  const initialEvent = useMemo(() => localStorage.getItem('selectedEvent') || null, []);
  const initialDateRange = useMemo(() => {
    const storedDateRange = JSON.parse(localStorage.getItem('dateRange'));
    if (storedDateRange && storedDateRange.length === 2) {
      return [dayjs(storedDateRange[0]), dayjs(storedDateRange[1])];
    }
    return [dayjs(), dayjs()];
  }, []);

  const [selectedEvent, setSelectedEvent] = useState(initialEvent);
  const [dateRange, setDateRange] = useState(initialDateRange);
  const [filterOptions, setFilterOptions] = useState({
    events: [],
    date_range: { start: '', end: '' },
    default_event: '',
    default_date_range: { start: '', end: '' },
  });
  const [error, setError] = useState(null);

  // Define fetchFilterOptions with useCallback to ensure it doesn't change between renders
  const fetchFilterOptions = useCallback(
    async (resetFilters = false) => {
      try {
        const response = await axios.get(
          'http://127.0.0.1:8000/api/customer/23/creatives/filter-options'
        );
        setError(null);
        const { data } = response;
        setFilterOptions(data);

        if (resetFilters) {
          setSelectedEvent(data.default_event);
          setDateRange([dayjs(data.default_date_range.start), dayjs(data.default_date_range.end)]);
        } else {
          // Set selected event and date range from API only if not already set from localStorage
          if (!initialEvent) {
            setSelectedEvent(data.default_event);
          }
          if (
            !initialDateRange[0].isValid() ||
            !initialDateRange[1].isValid() ||
            initialDateRange[0].isSame(initialDateRange[1])
          ) {
            setDateRange([
              dayjs(data.default_date_range.start),
              dayjs(data.default_date_range.end),
            ]);
          }
        }
      } catch (err) {
        setError('Failed to get filter options. Please try again.');
      }
    },
    [initialEvent, initialDateRange]
  );

  // Call the API when the component first mounts
  useEffect(() => {
    fetchFilterOptions();
  }, [fetchFilterOptions]);

  // Save selected event to localStorage
  useEffect(() => {
    if (selectedEvent) {
      localStorage.setItem('selectedEvent', selectedEvent);
    }
  }, [selectedEvent]);

  // Save date range to localStorage
  useEffect(() => {
    if (dateRange && dateRange[0].isValid() && dateRange[1].isValid()) {
      localStorage.setItem(
        'dateRange',
        JSON.stringify(dateRange.map((date) => date.toISOString()))
      );
    }
  }, [dateRange]);

  const handleEventChange = (event) => {
    setSelectedEvent(event.target.value);
  };

  const handleRefreshData = () => {
    fetchFilterOptions(true);
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

        <Box sx={{ mb: 3 }}>
          <Filters
            selectedEvent={selectedEvent}
            dateRange={dateRange}
            onEventChange={handleEventChange}
            onDateRangeAccept={setDateRange}
            events={filterOptions.events}
          />
          <Box sx={{ mt: 2 }}>
            <Button fullWidth variant="contained" color="primary" onClick={handleRefreshData}>
              Restore Filters
            </Button>
          </Box>
        </Box>

        {error && <Alert severity="error">{error}</Alert>}

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
