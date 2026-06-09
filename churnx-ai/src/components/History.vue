<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { 
  BarChart2, 
  AlertCircle, 
  Search, 
  Calendar, 
  Filter, 
  Download, 
  RefreshCcw, 
  Eye,
  Plus,
  Trash2
} from 'lucide-vue-next';
import { cn } from '../lib/utils';

const historyData = ref<any[]>([]);

onMounted(() => {
  const stored = localStorage.getItem('churnx_prediction_history');
  if (stored) {
    historyData.value = JSON.parse(stored);
  }
});

const headers = ['Date & Time', 'Customer ID', 'Result', 'Confidence', 'Actions'];

const emit = defineEmits(['view-item']);

const deleteItem = (rowToDelete: any) => {
  historyData.value = historyData.value.filter(row => row !== rowToDelete);
  localStorage.setItem('churnx_prediction_history', JSON.stringify(historyData.value));
};

const totalRuns = computed(() => historyData.value.length);
const highRiskCount = computed(() => historyData.value.filter(row => row.risk === 'High').length);

const searchQuery = ref('');
const filterRisk = ref('All Risk Levels');
const filterDateRange = ref<[Date, Date] | null>(null);

const filteredData = computed(() => {
  return historyData.value.filter(row => {
    const searchMatch = row.id.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                        (row.date && row.date.toLowerCase().includes(searchQuery.value.toLowerCase()));
    const riskMatch = filterRisk.value === 'All Risk Levels' || row.risk === filterRisk.value;
    
    let dateMatch = true;
    if (filterDateRange.value && filterDateRange.value.length === 2) {
      const rowDate = new Date(row.date);
      const start = new Date(filterDateRange.value[0]);
      start.setHours(0,0,0,0);
      const end = new Date(filterDateRange.value[1]);
      end.setHours(23,59,59,999);
      dateMatch = rowDate >= start && rowDate <= end;
    }
    
    return searchMatch && riskMatch && dateMatch;
  });
});

const downloadCSV = () => {
  if (filteredData.value.length === 0) return;
  
  const headers = [
    'CustomerID', 'Churn', 'Tenure', 'PreferredLoginDevice', 'CityTier', 'WarehouseToHome', 
    'PreferredPaymentMode', 'Gender', 'HourSpendOnApp', 'NumberOfDeviceRegistered', 
    'PreferedOrderCat', 'SatisfactionScore', 'MaritalStatus', 'NumberOfAddress', 
    'Complain', 'OrderAmountHikeFromlastYear', 'CouponUsed', 'OrderCount', 
    'DaySinceLastOrder', 'CashbackAmount'
  ];

  const csvContent = [
    headers.join(','),
    ...filteredData.value.map(row => {
      const data = row.customerData || {};
      const churn = row.risk === 'High' ? 1 : 0;
      const complain = data.Complain === true || data.Complain === 1 || String(data.Complain).toLowerCase() === 'yes' ? 1 : 0;
      
      const rowValues = [
        row.id,
        churn,
        data.Tenure ?? '',
        data.PreferredLoginDevice ?? '',
        data.CityTier ?? '',
        data.WarehouseToHome ?? '',
        data.PreferredPaymentMode ?? '',
        data.Gender ?? '',
        data.HourSpendOnApp ?? '',
        data.NumberOfDeviceRegistered ?? '',
        data.PreferedOrderCat ?? '',
        data.SatisfactionScore ?? '',
        data.MaritalStatus ?? '',
        data.NumberOfAddress ?? '',
        complain,
        data.OrderAmountHikeFromlastYear ?? '',
        data.CouponUsed ?? '',
        data.OrderCount ?? '',
        data.DaySinceLastOrder ?? '',
        data.CashbackAmount ?? ''
      ];

      return rowValues.map(val => {
        const str = String(val);
        return str.includes(',') ? `"${str}"` : str;
      }).join(',');
    })
  ].join('\n');
  
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.setAttribute('href', url);
  link.setAttribute('download', `churn_retraining_data_${new Date().getTime()}.csv`);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const currentPage = ref(1);
const itemsPerPage = 10;
const totalPages = computed(() => Math.max(1, Math.ceil(filteredData.value.length / itemsPerPage)));

const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return filteredData.value.slice(start, start + itemsPerPage);
});

const displayedPages = computed(() => {
  const pages = [];
  let start = Math.max(1, currentPage.value - 2);
  let end = Math.min(totalPages.value, start + 4);
  if (end - start < 4) {
    start = Math.max(1, end - 4);
  }
  for (let i = start; i <= end; i++) {
    pages.push(i);
  }
  return pages;
});

const nextPage = () => {
  if (currentPage.value < totalPages.value) currentPage.value++;
};
const prevPage = () => {
  if (currentPage.value > 1) currentPage.value--;
};
</script>

<template>
  <div class="p-6 space-y-8 max-w-[1440px] mx-auto animate-fade-in">
    <!-- Header & Stats -->
    <div class="flex flex-col lg:flex-row lg:items-end justify-between gap-6">
      <div>
        <h3 class="text-2xl font-bold tracking-tight mb-2">Prediction History</h3>
        <p class="text-sm text-outline font-medium">Review and audit all AI-generated churn analysis reports across the enterprise.</p>
      </div>
      <div class="flex gap-4">
        <div class="bg-surface-container-lowest border border-outline-variant p-4 rounded-xl flex items-center gap-4 shadow-sm min-w-[180px]">
          <div class="p-2.5 bg-primary/10 rounded-lg">
            <BarChart2 class="w-5 h-5 text-primary" />
          </div>
          <div>
            <p class="text-[10px] font-bold text-outline uppercase tracking-wider">Total Runs</p>
            <p class="text-xl font-bold">{{ totalRuns }}</p>
          </div>
        </div>
        <div class="bg-surface-container-lowest border border-outline-variant p-4 rounded-xl flex items-center gap-4 shadow-sm min-w-[180px]">
          <div class="p-2.5 bg-error/10 rounded-lg">
            <AlertCircle class="w-5 h-5 text-error" />
          </div>
          <div>
            <p class="text-[10px] font-bold text-outline uppercase tracking-wider">High Risk Found</p>
            <p class="text-xl font-bold text-error">{{ highRiskCount }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filter Bar -->
    <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-6 shadow-sm">
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 items-end">
        <div class="space-y-2">
          <label class="text-xs font-bold">Search Customer ID</label>
          <div class="relative">
            <Search class="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-outline" />
            <input 
              v-model="searchQuery"
              type="text" 
              placeholder="e.g. CUST-90210" 
              class="w-full pl-11 pr-4 py-2.5 bg-surface rounded-xl border border-outline-variant focus:ring-2 focus:ring-primary outline-none transition-all text-sm"
            />
          </div>
        </div>
        <div class="space-y-2 col-span-1 md:col-span-2 lg:col-span-1">
          <label class="text-xs font-bold">Date Range</label>
          <div class="w-full h-[42px] relative overflow-hidden rounded-xl border border-outline-variant focus-within:ring-2 focus-within:ring-primary transition-all">
            <el-date-picker
              v-model="filterDateRange"
              type="daterange"
              range-separator="-"
              start-placeholder="Start date"
              end-placeholder="End date"
              format="MMM D, YYYY"
              class="!w-full !h-full !border-0 !bg-surface"
              style="--el-input-bg-color: transparent; --el-input-border-color: transparent; width: 100%; height: 100%; box-shadow: none;"
            />
          </div>
        </div>
        <div class="space-y-2">
          <label class="text-xs font-bold">Risk Level</label>
          <select 
            v-model="filterRisk"
            class="w-full px-4 py-2.5 bg-surface rounded-xl border border-outline-variant focus:ring-2 focus:ring-primary outline-none text-sm appearance-none cursor-pointer">
            <option value="All Risk Levels">All Risk Levels</option>
            <option value="High">High Risk</option>
            <option value="Medium">Medium Risk</option>
            <option value="Low">Low Risk</option>
          </select>
        </div>
        <div class="flex gap-3">
          <button @click="downloadCSV" class="flex-1 bg-primary text-white h-[42px] rounded-xl font-bold text-sm flex items-center justify-center gap-2 shadow-md hover:shadow-lg active:scale-[0.98] transition-all">
            <Download class="w-4 h-4" />
            Export CSV
          </button>
          <button class="p-2.5 bg-surface-container-high text-on-surface rounded-xl border border-outline-variant hover:bg-surface-variant transition-colors group" title="Refresh">
            <RefreshCcw class="w-5 h-5 group-hover:rotate-180 transition-transform duration-500" />
          </button>
        </div>
      </div>
    </div>

    <!-- Table -->
    <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl shadow-sm overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-surface-container-low/50 border-b border-outline-variant">
              <th v-for="(h, i) in headers" :key="i" :class="cn(
                'px-6 py-4 text-[10px] font-bold uppercase text-outline tracking-widest',
                i === 4 && 'text-right'
              )">
                {{ h }}
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-outline-variant">
            <tr v-for="(row, idx) in paginatedData" :key="idx" class="hover:bg-surface-bright transition-colors group">
              <td class="px-6 py-6">
                <div class="flex flex-col">
                  <span class="text-sm font-bold text-on-surface">{{ row.date }}</span>
                  <span class="text-xs text-outline">{{ row.time }}</span>
                </div>
              </td>
              <td class="px-6 py-6">
                <div class="flex items-center gap-3">
                  <img 
                    :src="`https://picsum.photos/seed/cust-${idx}/40/40`" 
                    alt="" 
                    class="w-8 h-8 rounded bg-surface-variant object-cover" 
                    referrerpolicy="no-referrer"
                  />
                  <span class="text-sm font-bold">{{ row.id }}</span>
                </div>
              </td>
              <td class="px-6 py-6">
                <span :class="cn(
                  'px-3 py-1 rounded-lg text-[10px] font-bold uppercase tracking-wider border flex items-center gap-2 w-max',
                  row.risk === 'High' && 'bg-red-50 text-error border-error/10',
                  row.risk === 'Medium' && 'bg-amber-50 text-amber-700 border-amber-200',
                  row.risk === 'Low' && 'bg-green-50 text-green-700 border-green-200'
                )">
                  <span :class="cn(
                    'w-1.5 h-1.5 rounded-full',
                    row.risk === 'High' && 'bg-error',
                    row.risk === 'Medium' && 'bg-amber-600',
                    row.risk === 'Low' && 'bg-green-600'
                  )"></span>
                  {{ row.risk === 'High' ? 'Churn Likely' : row.risk === 'Medium' ? 'Potential Risk' : 'No Churn' }}
                </span>
              </td>
              <td class="px-6 py-6 font-bold">
                <div class="flex items-center gap-3 w-40">
                  <div class="h-2 flex-grow bg-surface-container rounded-full overflow-hidden">
                    <div 
                      :class="cn(
                        'h-full transition-all duration-1000',
                        row.risk === 'High' ? 'bg-error' : row.risk === 'Medium' ? 'bg-amber-500' : 'bg-green-500'
                      )" 
                      :style="{ width: `${row.confidence}%` }"
                    ></div>
                  </div>
                  <span class="text-xs w-8">{{ row.confidence }}%</span>
                </div>
              </td>
              <td class="px-6 py-6 text-right">
                <div class="flex items-center justify-end gap-2">
                  <button @click="emit('view-item', row)" class="text-primary hover:bg-primary/5 px-4 py-2 rounded-xl text-xs font-bold transition-all border border-transparent hover:border-primary/20 flex items-center gap-2">
                    <Eye class="w-4 h-4" />
                    View
                  </button>
                  <button @click="deleteItem(row)" class="text-error hover:bg-error/5 p-2 rounded-xl transition-all border border-transparent hover:border-error/20 flex items-center justify-center" title="Delete">
                    <Trash2 class="w-4 h-4" />
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Footer info/stats -->
      <div class="px-6 py-4 bg-surface-container-low/30 flex items-center justify-between border-t border-outline-variant">
        <span class="text-xs text-outline font-medium">Showing {{ filteredData.length > 0 ? (currentPage - 1) * itemsPerPage + 1 : 0 }} to {{ Math.min(currentPage * itemsPerPage, filteredData.length) }} of {{ filteredData.length }} results</span>
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="itemsPerPage"
          :total="filteredData.length"
          layout="prev, pager, next"
          background
        />
      </div>
    </div>

    <!-- FAB -->
    <button class="fixed bottom-8 right-8 w-14 h-14 bg-primary text-white rounded-full shadow-2xl flex items-center justify-center hover:scale-110 active:scale-95 transition-all z-50">
      <Plus class="w-7 h-7" />
    </button>
  </div>
</template>

<style>
.animate-fade-in {
  animation: fadeIn 0.3s ease-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>
