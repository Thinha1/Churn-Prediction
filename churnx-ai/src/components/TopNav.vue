<script setup lang="ts">
import { Bell, HelpCircle } from 'lucide-vue-next';

defineProps<{
  title: string;
}>();
</script>

<template>
  <header class="h-16 flex items-center justify-between px-6 bg-surface-bright border-b border-outline-variant shadow-sm sticky top-0 z-40">
    <h2 class="text-xl font-semibold text-on-surface tracking-tight">{{ title }}</h2>
    
    <div class="flex items-center gap-6">
      <div class="flex items-center gap-4">
        <button class="text-outline hover:text-primary transition-colors duration-200 relative p-1">
          <Bell class="w-5 h-5" />
          <span class="absolute top-1 right-1 w-2 h-2 bg-error rounded-full border-2 border-surface-bright"></span>
        </button>
        <button class="text-outline hover:text-primary transition-colors duration-200 p-1">
          <HelpCircle class="w-5 h-5" />
        </button>
      </div>
      
      <button v-if="title === 'Batch Upload'" class="bg-primary text-on-primary px-6 py-2 rounded-lg text-sm font-bold hover:shadow-lg transition-all active:scale-95">
        Process All
      </button>
    </div>
  </header>
</template>
