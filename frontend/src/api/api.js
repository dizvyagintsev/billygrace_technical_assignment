import axios from 'axios';
import { API_BASE_URL } from '../config-global';

export const Event = Object.freeze({
  AD_CALLS: 'ad_calls',
  ADD_TO_CART: 'add_to_cart',
  BEL_AFSPRAAK: 'bel_afspraak',
  CHECK_STOCK: 'check_stock',
  LANDINGPAGE_VISIT: 'landingpage_visit',
  ORDER_COMPLETED: 'order_completed',
  ORDER_COMPLETED_CV: 'order_completed_cv',
  PRODUCT_VIEW: 'product_view',
  SOLLICITATIE_VERZONDEN: 'sollicitatie_verzonden',
  SUBSCRIBE: 'subscribe',
  WINKEL_AFSPRAAK: 'winkel_afspraak',
});

export const getMetrics = async (customerId, event, startDate, endDate) => {
  const response = await axios.get(
    `${API_BASE_URL}/api/customer/${customerId}/creatives/${event}/metrics`,
    {
      params: {
        start_date: startDate,
        end_date: endDate,
      },
    }
  );
  return response.data;
};
