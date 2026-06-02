<script setup lang="ts">
import { LayoutDashboard, FileUp, History, Settings } from 'lucide-vue-next';
import { cn } from '../lib/utils';

const props = defineProps<{
  activeTab: string;
}>();

const emit = defineEmits<{
  (e: 'update:activeTab', tab: string): void
}>();

const navItems = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'batch', label: 'Batch Upload', icon: FileUp },
  { id: 'history', label: 'History', icon: History },
  { id: 'settings', label: 'Settings', icon: Settings },
];
</script>

<template>
  <aside class="fixed left-0 top-0 h-full w-[260px] bg-surface border-r border-outline-variant flex flex-col py-6 px-4 z-50">
    <div class="mb-8 px-2">
      <h1 class="text-xl font-bold text-primary tracking-tight">ChurnX AI</h1>
      <p class="text-xs text-secondary font-medium">Enterprise Analytics</p>
    </div>

    <nav class="flex-1 space-y-1">
      <button
        v-for="item in navItems"
        :key="item.id"
        @click="emit('update:activeTab', item.id)"
        :class="cn(
          'w-full flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-200 group',
          activeTab === item.id
            ? 'bg-secondary-container text-primary font-bold shadow-sm'
            : 'text-secondary hover:bg-surface-container hover:text-on-surface'
        )"
      >
        <component 
          :is="item.icon" 
          :class="cn(
            'w-5 h-5 transition-colors',
            activeTab === item.id ? 'text-primary' : 'text-outline group-hover:text-secondary'
          )" 
        />
        <span class="text-sm font-medium">{{ item.label }}</span>
      </button>
    </nav>

    <div class="mt-auto p-2 border-t border-outline-variant pt-6">
      <div class="flex items-center gap-3">
        <img
          src="https://picsum.photos/seed/executive/80/80"
          alt="User avatar"
          class="w-10 h-10 rounded-full border border-outline-variant object-cover"
          referrerpolicy="no-referrer"
        />
        <div class="flex flex-col min-w-0">
          <span class="text-sm font-bold truncate">Executive User</span>
          <span class="text-xs text-outline truncate">Organization Admin</span>
        </div>
      </div>
    </div>
  </aside>
</template>
