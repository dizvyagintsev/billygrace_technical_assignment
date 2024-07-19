import React from "react";
import { Grid, FormControl, InputLabel, MenuItem, Select } from "@mui/material";
import { DateRangePicker } from "@mui/x-date-pickers-pro";
import { Event } from "../../api/api";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";

export default function Filters({
  selectedEvent,
  dateRange,
  onEventChange,
  onDateRangeChange,
}) {
  return (
    <Grid container spacing={2} alignItems="center" sx={{ mb: 3 }}>
      <Grid item xs={12}>
        <FormControl fullWidth>
          <InputLabel id="event-label">Event</InputLabel>
          <Select
            labelId="event-label"
            value={selectedEvent}
            onChange={onEventChange}
            sx={{ textDecoration: "none" }}
          >
            {Object.entries(Event).map(([key, value]) => (
              <MenuItem key={key} value={value}>
                {value}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Grid>
      <Grid item xs={12}>
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <DateRangePicker
            startText="Start Date"
            endText="End Date"
            value={dateRange}
            onChange={onDateRangeChange}
          />
        </LocalizationProvider>
      </Grid>
    </Grid>
  );
}
