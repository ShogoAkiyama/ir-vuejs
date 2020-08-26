import Vue from 'vue'
import App from './App'
import store from './store';

import Highcharts from 'highcharts';
import Stock from 'highcharts/modules/stock';
import HighchartsVue from 'highcharts-vue';

Stock(Highcharts);
Vue.use(HighchartsVue);

Vue.config.productionTip = false

new Vue({
  store: store,
  render: h => h(App),
}).$mount('#app')
