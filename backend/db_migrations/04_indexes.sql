CREATE INDEX idx_pixel_event_integrated_data_filter ON creatives.pixel_event_integrated_data (customer_name, ev, date_column);
CREATE INDEX idx_pixel_event_integrated_data_ad_id ON creatives.pixel_event_integrated_data (ad_id);
CREATE INDEX idx_dim_combined_creative_ad_id ON creatives.dim_combined_creative (ad_id);
