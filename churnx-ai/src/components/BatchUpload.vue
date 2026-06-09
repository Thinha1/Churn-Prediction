<script setup lang="ts">
import { ref, computed } from 'vue';
import { Upload, Search, Filter, Info, CheckCircle, BrainCircuit, ChevronLeft, ChevronRight, Loader2, Eye } from 'lucide-vue-next';
import { cn } from '../lib/utils';

const isUploading = ref(false);
const previewData = ref<any[]>([]);
const totalRows = ref(0);

const currentPage = ref(1);
const itemsPerPage = 10;
const paginatedData = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  return previewData.value.slice(start, start + itemsPerPage);
});

const handleFileUpload = async (event: any) => {
  const file = event.target.files?.[0] || event.dataTransfer?.files?.[0];
  if (!file) return;

  isUploading.value = true;
  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch('http://127.0.0.1:8005/predict_batch', {
      method: 'POST',
      body: formData
    });
    const data = await res.json();
    if (data.results) {
      previewData.value = data.results;
      totalRows.value = data.total;
      currentPage.value = 1;

      const history = JSON.parse(localStorage.getItem('churnx_prediction_history') || '[]');
      const dateStr = new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
      const timeStr = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
      
      const newEntries = data.results.map((row: any) => ({
        id: row.id,
        date: dateStr,
        time: timeStr,
        customerData: row.customerData,
        risk: row.risk,
        confidence: row.confidence,
        fullPrediction: row.fullPrediction
      }));
      
      const updatedHistory = [...newEntries, ...history];
      localStorage.setItem('churnx_prediction_history', JSON.stringify(updatedHistory));
    } else {
      alert("Error: " + data.error);
    }
  } catch (error) {
    console.error('Upload failed', error);
  } finally {
    isUploading.value = false;
  }
};

const requirements = [
  'Header row must match schema', 
  'Customer ID is mandatory', 
  'Satisfaction score (1.0 to 5.0)'
];

const columns = ['Customer ID', 'Tenure', 'Complaint', 'Satisfaction Score', 'Churn Risk (Predicted)', 'Actions'];

const emit = defineEmits(['view-item']);
</script>

<template>
  <div class="p-6 space-y-8 max-w-[1440px] mx-auto animate-fade-in-up">
    <!-- Upload Drag/Drop -->
    <section>
      <div 
        @dragover.prevent 
        @drop.prevent="handleFileUpload"
        class="bg-surface-container-low border-2 border-dashed border-outline-variant rounded-2xl p-16 flex flex-col items-center justify-center text-center transition-all hover:border-primary hover:bg-surface-container group cursor-pointer relative">
        <input type="file" @change="handleFileUpload" class="absolute inset-0 w-full h-full opacity-0 cursor-pointer" accept=".csv, .xlsx, .xls" :disabled="isUploading" />
        <div class="w-16 h-16 bg-primary-fixed rounded-full flex items-center justify-center mb-6 group-hover:bg-primary transition-all duration-300">
          <Loader2 v-if="isUploading" class="w-8 h-8 text-primary group-hover:text-on-primary animate-spin" />
          <Upload v-else class="w-8 h-8 text-primary group-hover:text-on-primary" />
        </div>
        <h3 class="text-xl font-bold text-on-surface mb-2">
          {{ isUploading ? 'Processing your dataset...' : 'Drag and drop your dataset here' }}
        </h3>
        <p class="text-sm text-secondary max-w-md mb-8">Support for Excel (.xlsx) and CSV files up to 50MB. Max 10,000 rows per batch.</p>
        <button class="border border-outline px-8 py-3 rounded-xl font-bold hover:bg-surface-container-highest transition-colors" :disabled="isUploading">
          Browse Files
        </button>
      </div>
    </section>

    <!-- Data Preview -->
    <section class="bg-surface-container-lowest rounded-2xl border border-outline-variant shadow-sm overflow-hidden">
      <div class="p-6 border-b border-outline-variant flex flex-col sm:flex-row justify-between items-center bg-surface-bright gap-4">
        <h3 class="text-lg font-bold">Uploaded Data Preview</h3>
        <div class="flex items-center gap-4 w-full sm:w-auto">
          <div class="relative flex-1 sm:w-64">
            <Search class="w-4 h-4 absolute left-4 top-1/2 -translate-y-1/2 text-outline" />
            <input 
              type="text" 
              placeholder="Search preview..." 
              class="w-full pl-11 pr-4 py-2.5 bg-surface border border-outline-variant rounded-xl text-sm focus:ring-2 focus:ring-primary outline-none transition-all"
            />
          </div>
          <button class="flex items-center gap-2 px-4 py-2.5 border border-outline-variant rounded-xl text-xs font-bold text-secondary hover:bg-surface-container transition-colors">
            <Filter class="w-4 h-4" />
            Filter
          </button>
        </div>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead class="bg-surface-container-high">
            <tr>
              <th v-for="(h, idx) in columns" :key="idx" :class="cn(
                'px-6 py-4 text-[10px] font-bold text-secondary uppercase tracking-widest',
                idx === 5 && 'text-right'
              )">
                {{ h }}
              </th>
            </tr>
          </thead>
          <tbody class="divide-y divide-outline-variant">
            <tr v-if="previewData.length === 0">
              <td colspan="5" class="px-6 py-8 text-center text-secondary">No data uploaded yet. Please upload a file to see predictions.</td>
            </tr>
            <tr v-for="(row, idx) in paginatedData" :key="idx" class="hover:bg-surface-container-low transition-colors group">
              <td class="px-6 py-4 text-sm font-medium">{{ row.id }}</td>
              <td class="px-6 py-4 text-sm text-secondary">{{ row.tenure }}</td>
              <td class="px-6 py-4 text-sm text-secondary">{{ row.complaint }}</td>
              <td class="px-6 py-4 text-sm text-secondary font-bold">{{ row.score }}</td>
              <td class="px-6 py-4">
                <span :class="cn(
                  'px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider',
                  row.risk === 'Low' && 'bg-green-100 text-green-700',
                  row.risk === 'Medium' && 'bg-amber-100 text-amber-700',
                  row.risk === 'High' && 'bg-red-100 text-red-700'
                )">
                  {{ row.risk }}
                </span>
              </td>
              <td class="px-6 py-4 text-right">
                <button @click="emit('view-item', row)" class="text-primary hover:bg-primary/5 px-4 py-2 rounded-xl text-xs font-bold transition-all border border-transparent hover:border-primary/20 flex items-center gap-2 ml-auto">
                  <Eye class="w-4 h-4" />
                  View
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="p-6 bg-surface-bright flex flex-col sm:flex-row justify-between items-center border-t border-outline-variant gap-4">
        <span class="text-xs text-outline font-medium">Showing {{ previewData.length > 0 ? (currentPage - 1) * itemsPerPage + 1 : 0 }} to {{ Math.min(currentPage * itemsPerPage, previewData.length) }} of {{ totalRows }} entries</span>
        <el-pagination
          v-model:current-page="currentPage"
          :page-size="itemsPerPage"
          :total="totalRows"
          layout="prev, pager, next"
          background
        />
      </div>
    </section>

    <!-- Info Bento -->
    <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <div class="bg-surface-container-low p-8 rounded-2xl border border-outline-variant">
        <div class="flex items-center gap-3 mb-6">
          <Info class="w-5 h-5 text-primary" />
          <h4 class="font-bold">Data Requirements</h4>
        </div>
        <ul class="space-y-4 text-sm text-secondary">
          <li v-for="(text, i) in requirements" :key="i" class="flex items-center gap-3">
            <CheckCircle class="w-4 h-4 text-primary shrink-0" />
            <span class="font-medium">{{ text }}</span>
          </li>
        </ul>
      </div>
      <div class="lg:col-span-2 bg-surface-container-low p-8 rounded-2xl border border-outline-variant relative overflow-hidden group">
        <div class="relative z-10 h-full flex flex-col">
          <h4 class="font-bold mb-2">Model Version: ChurnV4.2_Enterprise</h4>
          <p class="text-sm text-secondary mb-8 max-w-xl">
            Running predictions using the latest XGBoost-based ensemble trained on historical behavior from the last 12 months. Current accuracy: <span class="text-primary font-bold">94.2%</span>.
          </p>
          <div class="mt-auto flex items-center gap-12">
            <div class="flex flex-col">
              <span class="text-[10px] font-bold text-outline uppercase tracking-widest mb-1">Latency</span>
              <span class="text-lg font-bold text-primary">~1.2s / 1k rows</span>
            </div>
            <div class="flex flex-col">
              <span class="text-[10px] font-bold text-outline uppercase tracking-widest mb-1">Queue Status</span>
              <div class="flex items-center gap-2">
                <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                <span class="text-lg font-bold text-green-600">Available</span>
              </div>
            </div>
          </div>
        </div>
        <BrainCircuit class="absolute -right-4 -bottom-4 w-48 h-48 text-primary opacity-[0.03] group-hover:opacity-[0.06] transition-all duration-700 rotate-12" />
      </div>
    </section>
  </div>
</template>

<style>
.animate-fade-in-up {
  animation: fadeInUp 0.3s ease-out forwards;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: scale(0.98);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
