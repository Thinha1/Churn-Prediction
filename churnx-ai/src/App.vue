<script setup lang="ts">
import { ref, computed } from 'vue';
import Sidebar from './components/Sidebar.vue';
import TopNav from './components/TopNav.vue';
import Dashboard from './components/Dashboard.vue';
import BatchUpload from './components/BatchUpload.vue';
import History from './components/History.vue';

const activeTab = ref('dashboard');

const pageTitle = computed(() => {
  switch (activeTab.value) {
    case 'dashboard': return 'Customer Churn Prediction';
    case 'batch': return 'Batch Upload';
    case 'history': return 'Prediction History';
    case 'settings': return 'System Settings';
    default: return 'ChurnX AI';
  }
});
</script>

<template>
  <div class="flex min-h-screen bg-background text-on-surface select-none">
    <Sidebar v-model:activeTab="activeTab" />
    
    <div class="flex-1 ml-[260px] flex flex-col min-h-screen">
      <TopNav :title="pageTitle" />
      
      <main class="flex-1 overflow-x-hidden">
        <transition name="fade-slide" mode="out-in">
          <Dashboard v-if="activeTab === 'dashboard'" />
          <BatchUpload v-else-if="activeTab === 'batch'" />
          <History v-else-if="activeTab === 'history'" />
          <div v-else-if="activeTab === 'settings'" class="p-12 text-center">
            <h3 class="text-2xl font-bold text-outline">Settings Module</h3>
            <p class="text-secondary mt-2">Enterprise configuration and API management coming soon.</p>
          </div>
        </transition>
      </main>
    </div>
  </div>
</template>

<style>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateX(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateX(-10px);
}
</style>
