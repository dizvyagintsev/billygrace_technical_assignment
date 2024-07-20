SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: creatives; Type: SCHEMA; Schema: -;
--

CREATE SCHEMA creatives;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: dim_combined_creative; Type: TABLE; Schema: creatives;
--

CREATE TABLE creatives.dim_combined_creative (
    channel character varying,
    ad_id character varying,
    campaign_id character varying,
    date character varying,
    customer_name character varying,
    ad_type character varying,
    link character varying,
    type character varying,
    date_column date,
    ad_copy character varying,
    media_id character varying,
    creative_id character varying,
    copy_id character varying
);

--
-- Name: pixel_event_integrated_data; Type: TABLE; Schema: creatives;
--

CREATE TABLE creatives.pixel_event_integrated_data (
    campaign_name character varying,
    medium character varying,
    source character varying,
    adset_name character varying,
    ad_name character varying,
    bg_source character varying,
    bg_source_id character varying,
    date character varying,
    sessions numeric,
    users numeric,
    new_users numeric,
    number_of_events numeric,
    shopify_revenue numeric,
    new_customer numeric,
    returning_customer numeric,
    ev character varying,
    ad_id character varying,
    impressions numeric,
    clicks numeric,
    spend numeric,
    campaign_id character varying,
    adset_id character varying,
    shopify_revenue_attr numeric,
    returning_customer_attr numeric,
    new_customer_attr numeric,
    number_of_events_attr numeric,
    customer_name character varying,
    returning_customer_revenue numeric,
    returning_customer_revenue_attr numeric,
    new_customer_revenue numeric,
    new_customer_revenue_attr numeric,
    date_column date,
    event_value numeric,
    event_value_attr numeric,
    number_of_events_attr_window_1 numeric,
    number_of_events_attr_window_7 numeric,
    number_of_events_attr_window_30 numeric,
    event_value_attr_window_1 numeric,
    event_value_attr_window_7 numeric,
    event_value_attr_window_30 numeric,
    shopify_revenue_attr_window_1 numeric,
    shopify_revenue_attr_window_7 numeric,
    shopify_revenue_attr_window_30 numeric,
    returning_customer_attr_window_1 numeric,
    returning_customer_attr_window_7 numeric,
    returning_customer_attr_window_30 numeric,
    new_customer_attr_window_1 numeric,
    new_customer_attr_window_7 numeric,
    new_customer_attr_window_30 numeric,
    returning_customer_revenue_attr_window_1 numeric,
    returning_customer_revenue_attr_window_7 numeric,
    returning_customer_revenue_attr_window_30 numeric,
    new_customer_revenue_attr_window_1 numeric,
    new_customer_revenue_attr_window_7 numeric,
    new_customer_revenue_attr_window_30 numeric,
    ad_status character varying,
    adset_status character varying,
    campaign_status character varying,
    budget_type character varying,
    budget numeric,
    cltv numeric,
    cltv_attr numeric,
    cltv_attr_window_1 numeric,
    cltv_attr_window_7 numeric,
    cltv_attr_window_30 numeric,
    pageviews numeric,
    is_integrated_channel integer,
    pre_spend_profit double precision,
    pre_spend_profit_attr double precision,
    pre_spend_profit_attr_window_1 double precision,
    pre_spend_profit_attr_window_7 double precision,
    pre_spend_profit_attr_window_30 double precision
);
