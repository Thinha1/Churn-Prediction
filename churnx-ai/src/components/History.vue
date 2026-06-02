<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { 
  BarChart2, 
  AlertCircle, 
  Search, 
  Calendar, 
  Filter, 
  Download, 
  RefreshCcw, 
  Eye,
  Plus
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
            <p class="text-xl font-bold">1,284</p>
          </div>
        </div>
        <div class="bg-surface-container-lowest border border-outline-variant p-4 rounded-xl flex items-center gap-4 shadow-sm min-w-[180px]">
          <div class="p-2.5 bg-error/10 rounded-lg">
            <AlertCircle class="w-5 h-5 text-error" />
          </div>
          <div>
            <p class="text-[10px] font-bold text-outline uppercase tracking-wider">High Risk Found</p>
            <p class="text-xl font-bold text-error">342</p>
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
              type="text" 
              placeholder="e.g. CUST-90210" 
              class="w-full pl-11 pr-4 py-2.5 bg-surface rounded-xl border border-outline-variant focus:ring-2 focus:ring-primary outline-none transition-all text-sm"
            />
          </div>
        </div>
        <div class="space-y-2">
          <label class="text-xs font-bold">Date Range</label>
          <div class="relative">
            <Calendar class="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-outline" />
            <input 
              type="text" 
              placeholder="Last 30 Days" 
              class="w-full pl-11 pr-4 py-2.5 bg-surface rounded-xl border border-outline-variant focus:ring-2 focus:ring-primary outline-none transition-all text-sm"
            />
          </div>
        </div>
        <div class="space-y-2">
          <label class="text-xs font-bold">Risk Level</label>
          <select class="w-full px-4 py-2.5 bg-surface rounded-xl border border-outline-variant focus:ring-2 focus:ring-primary outline-none text-sm appearance-none cursor-pointer">
            <option>All Risk Levels</option>
            <option>High Risk</option>
            <option>Medium Risk</option>
            <option>Low Risk</option>
          </select>
        </div>
        <div class="flex gap-3">
          <button class="flex-1 bg-primary text-white h-[42px] rounded-xl font-bold text-sm flex items-center justify-center gap-2 shadow-md hover:shadow-lg active:scale-[0.98] transition-all">
            <Filter class="w-4 h-4" />
            Apply
          </button>
          <button class="p-2.5 bg-surface-container-high text-on-surface rounded-xl border border-outline-variant hover:bg-surface-variant transition-colors group">
            <Download class="w-5 h-5 group-hover:scale-110 transition-transform" />
          </button>
          <button class="p-2.5 bg-surface-container-high text-on-surface rounded-xl border border-outline-variant hover:bg-surface-variant transition-colors">
            <RefreshCcw class="w-5 h-5" />
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
            <tr v-for="(row, idx) in historyData" :key="idx" class="hover:bg-surface-bright transition-colors group">
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
                <button class="text-primary hover:bg-primary/5 px-4 py-2 rounded-xl text-xs font-bold transition-all border border-transparent hover:border-primary/20 flex items-center gap-2 ml-auto">
                  <Eye class="w-4 h-4" />
                  View
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Footer info/stats -->
      <div class="px-6 py-4 bg-surface-container-low/30 flex items-center justify-between border-t border-outline-variant">
        <span class="text-xs text-outline font-medium">Showing 1 to 10 of 1,284 results</span>
        <div class="flex items-center gap-4">
           <button class="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-surface-container transition-colors text-xs font-bold text-outline">
             Previous
           </button>
           <div class="flex gap-1">
              <button class="w-8 h-8 rounded-lg bg-primary text-white text-xs font-bold">1</button>
              <button class="w-8 h-8 rounded-lg hover:bg-surface-container text-xs font-bold">2</button>
              <button class="w-8 h-8 rounded-lg hover:bg-surface-container text-xs font-bold">3</button>
           </div>
           <button class="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-surface-container transition-colors text-xs font-bold text-primary">
             Next
           </button>
        </div>
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
