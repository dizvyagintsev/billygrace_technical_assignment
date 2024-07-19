import React, { useEffect, useState } from 'react';
import { DataGrid } from '@mui/x-data-grid';
import PropTypes from 'prop-types';
import { Alert } from '@mui/material';
import axios from 'axios';
import { API_BASE_URL } from '../../config-global';

export default function MetricsDataGrid({ event, dateRange }) {
  const [rows_, setRows] = useState([]);
  const [columns_, setColumns] = useState([]);
  const [fetchError, setError] = useState(null);
  const url = `${API_BASE_URL}/api/customer/23/creatives/${event}/metrics`;

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await axios.get(url, {
          params: {
            start_date: dateRange[0].format('YYYY-MM-DD'),
            end_date: dateRange[1].format('YYYY-MM-DD'),
          },
        });
        setError(null);

        const { rows, columns } = response.data;
        setRows(rows);
        setColumns(columns);
      } catch (error) {
        setError('Failed to fetch metrics data. Please try again.');
      }
    };
    fetchMetrics();
  }, [event, dateRange, url]);

  if (fetchError) {
    return <Alert severity="error">{fetchError}</Alert>;
  }

  return <DataGrid rows={rows_} columns={columns_} autoHeight />;
}

MetricsDataGrid.propTypes = {
  event: PropTypes.string.isRequired,
  dateRange: PropTypes.arrayOf(PropTypes.instanceOf(Date)).isRequired,
};
