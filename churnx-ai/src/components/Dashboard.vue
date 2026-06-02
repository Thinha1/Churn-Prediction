<script setup lang="ts">
import { ref } from 'vue';
import { Info, AlertTriangle, Sparkles, LineChart, ChevronRight } from 'lucide-vue-next';
import { cn } from '../lib/utils';

const form = ref({
  Tenure: null as number | null,
  CityTier: 1,
  WarehouseToHome: null as number | null,
  HourSpendOnApp: null as number | null,
  NumberOfDeviceRegistered: null as number | null,
  SatisfactionScore: 4,
  NumberOfAddress: null as number | null,
  Complain: false,
  OrderAmountHikeFromlastYear: null as number | null,
  CouponUsed: null as number | null,
  OrderCount: null as number | null,
  DaySinceLastOrder: null as number | null,
  CashbackAmount: null as number | null,
  PreferredLoginDevice: 'Mobile Phone',
  PreferredPaymentMode: 'Debit Card',
  Gender: 'Male',
  PreferedOrderCat: 'Laptop & Accessory',
  MaritalStatus: 'Single'
});

const isPredicting = ref(false);
const predictionResult = ref<any>(null);

const predictChurn = async () => {
  isPredicting.value = true;
  try {
    const response = await fetch('http://127.0.0.1:8000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        Tenure: form.value.Tenure || 0,
        CityTier: form.value.CityTier,
        WarehouseToHome: form.value.WarehouseToHome || 0,
        HourSpendOnApp: form.value.HourSpendOnApp || 0,
        NumberOfDeviceRegistered: form.value.NumberOfDeviceRegistered || 0,
        SatisfactionScore: form.value.SatisfactionScore,
        NumberOfAddress: form.value.NumberOfAddress || 0,
        Complain: form.value.Complain,
        OrderAmountHikeFromlastYear: form.value.OrderAmountHikeFromlastYear || 0,
        CouponUsed: form.value.CouponUsed || 0,
        OrderCount: form.value.OrderCount || 0,
        DaySinceLastOrder: form.value.DaySinceLastOrder || 0,
        CashbackAmount: form.value.CashbackAmount || 0,
        PreferredLoginDevice: form.value.PreferredLoginDevice,
        PreferredPaymentMode: form.value.PreferredPaymentMode,
        Gender: form.value.Gender,
        PreferedOrderCat: form.value.PreferedOrderCat,
        MaritalStatus: form.value.MaritalStatus
      })
    });
    
    if (response.ok) {
      predictionResult.value = await response.json();
      
      const history = JSON.parse(localStorage.getItem('churnx_prediction_history') || '[]');
      const newEntry = {
        id: `CUST-${Math.floor(Math.random() * 90000) + 10000}`,
        date: new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }),
        time: new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        customerData: { ...form.value },
        risk: predictionResult.value.risk_level,
        confidence: predictionResult.value.confidence
      };
      history.unshift(newEntry);
      localStorage.setItem('churnx_prediction_history', JSON.stringify(history));
    }
  } catch (error) {
    console.error("Prediction error:", error);
  } finally {
    isPredicting.value = false;
  }
};
</script>

<template>
  <div class="grid grid-cols-12 gap-6 p-6 max-w-[1440px] mx-auto">
    <!-- Prediction FormSection -->
    <section class="col-span-12 lg:col-span-7">
      <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-8 shadow-sm h-full">
        <div class="flex items-center justify-between mb-8">
          <h3 class="text-lg font-bold text-on-surface">Single Prediction Form</h3>
          <span class="px-3 py-1 bg-primary-container text-on-primary-container rounded-full text-xs font-bold tracking-tight">NEW ENTRY</span>
        </div>

        <form @submit.prevent="predictChurn" class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-2">
            <label class="text-sm font-bold text-on-surface">Thời gian sử dụng (Tenure)</label>
            <input v-model="form.Tenure" type="number" placeholder="e.g. 12" class="w-full bg-surface border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:outline-none transition-all" required />
          </div>
          <div class="space-y-2">
            <label class="text-sm font-bold text-on-surface">Khoảng cách từ kho (Warehouse to Home)</label>
            <input v-model="form.WarehouseToHome" type="number" placeholder="e.g. 5" class="w-full bg-surface border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:outline-none transition-all" required />
          </div>
          <div class="space-y-2">
            <label class="text-sm font-bold text-on-surface">Phân cấp thành phố (City Tier)</label>
            <select v-model="form.CityTier" class="w-full bg-surface border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:outline-none appearance-none transition-all">
              <option :value="1">Tier 1</option>
              <option :value="2">Tier 2</option>
              <option :value="3">Tier 3</option>
            </select>
          </div>
          <div class="space-y-2">
            <label class="text-sm font-bold text-on-surface">Giờ dùng App (Hour Spend On App)</label>
            <input v-model="form.HourSpendOnApp" type="number" step="0.5" placeholder="e.g. 3" class="w-full bg-surface border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:outline-none transition-all" required />
          </div>
          <div class="space-y-2">
            <label class="text-sm font-bold text-on-surface">Thiết bị đăng nhập (Login Device)</label>
            <select v-model="form.PreferredLoginDevice" class="w-full bg-surface border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:outline-none appearance-none transition-all">
              <option value="Mobile Phone">Mobile Phone</option>
              <option value="Computer">Computer</option>
            </select>
          </div>
          <div class="space-y-2">
            <label class="text-sm font-bold text-on-surface">Số thiết bị đăng ký (Devices Registered)</label>
            <input v-model="form.NumberOfDeviceRegistered" type="number" placeholder="e.g. 3" class="w-full bg-surface border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:outline-none transition-all" required />
          </div>
          <div class="space-y-2">
            <label class="text-sm font-bold text-on-surface">Giới tính (Gender)</label>
            <select v-model="form.Gender" class="w-full bg-surface border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:outline-none appearance-none transition-all">
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
          </div>
          <div class="space-y-2">
            <label class="text-sm font-bold text-on-surface">Tình trạng hôn nhân (Marital Status)</label>
            <select v-model="form.MaritalStatus" class="w-full bg-surface border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:outline-none appearance-none transition-all">
              <option value="Single">Single</option>
              <option value="Married">Married</option>
              <option value="Divorced">Divorced</option>
            </select>
          </div>

          <div class="md:col-span-2 bg-surface-container p-6 rounded-xl space-y-4">
            <div class="flex justify-between items-center">
              <label class="text-sm font-bold text-on-surface">Điểm hài lòng (Satisfaction Score)</label>
              <span class="text-lg font-bold text-primary">{{ form.SatisfactionScore }}</span>
            </div>
            <input type="range" min="1" max="5" v-model.number="form.SatisfactionScore" class="w-full h-2 bg-outline-variant rounded-full appearance-none cursor-pointer accent-primary" />
            <div class="flex justify-between text-[11px] text-outline font-medium">
              <span>1 - Kém (Poor)</span>
              <span>5 - Xuất sắc (Excellent)</span>
            </div>
          </div>

          <div class="space-y-2">
            <label class="text-sm font-bold text-on-surface">Phương thức thanh toán (Payment Mode)</label>
            <select v-model="form.PreferredPaymentMode" class="w-full bg-surface border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:outline-none appearance-none transition-all">
              <option value="Debit Card">Debit Card</option>
              <option value="Credit Card">Credit Card</option>
              <option value="E wallet">E wallet</option>
              <option value="UPI">UPI</option>
              <option value="Cash on Delivery">Cash on Delivery</option>
            </select>
          </div>
          <div class="space-y-2">
            <label class="text-sm font-bold text-on-surface">Danh mục ưa thích (Preferred Order Cat)</label>
            <select v-model="form.PreferedOrderCat" class="w-full bg-surface border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:outline-none appearance-none transition-all">
              <option value="Laptop & Accessory">Laptop & Accessory</option>
              <option value="Mobile Phone">Mobile Phone</option>
              <option value="Fashion">Fashion</option>
              <option value="Grocery">Grocery</option>
              <option value="Others">Others</option>
            </select>
          </div>
          <div class="space-y-2">
            <label class="text-sm font-bold text-on-surface">Số lượng đơn hàng (Order Count)</label>
            <input v-model="form.OrderCount" type="number" placeholder="e.g. 2" class="w-full bg-surface border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:outline-none transition-all" required />
          </div>
          <div class="space-y-2">
            <label class="text-sm font-bold text-on-surface">Mã giảm giá đã dùng (Coupon Used)</label>
            <input v-model="form.CouponUsed" type="number" placeholder="e.g. 1" class="w-full bg-surface border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:outline-none transition-all" required />
          </div>
          <div class="space-y-2">
            <label class="text-sm font-bold text-on-surface">% Tăng giá trị đơn so với năm trước (Order Amount Hike %)</label>
            <input v-model="form.OrderAmountHikeFromlastYear" type="number" placeholder="e.g. 15" class="w-full bg-surface border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:outline-none transition-all" required />
          </div>
          <div class="space-y-2">
            <label class="text-sm font-bold text-on-surface">Tổng số địa chỉ (Number of Address)</label>
            <input v-model="form.NumberOfAddress" type="number" placeholder="e.g. 2" class="w-full bg-surface border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:outline-none transition-all" required />
          </div>
          <div class="space-y-2">
            <label class="text-sm font-bold text-on-surface">Ngày từ lần mua cuối (Days Since Last Order)</label>
            <input v-model="form.DaySinceLastOrder" type="number" placeholder="e.g. 5" class="w-full bg-surface border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:outline-none transition-all" required />
          </div>
          <div class="space-y-2">
            <label class="text-sm font-bold text-on-surface">Tiền hoàn lại (Cashback Amount $)</label>
            <input v-model="form.CashbackAmount" type="number" step="0.01" placeholder="e.g. 150.50" class="w-full bg-surface border border-outline-variant rounded-xl px-4 py-3 focus:ring-2 focus:ring-primary focus:outline-none transition-all" required />
          </div>

          <div class="flex items-center justify-between p-4 border border-outline-variant rounded-xl bg-surface md:col-span-2">
            <div class="flex flex-col">
              <label class="text-sm font-bold text-on-surface">Đã từng khiếu nại (Registered Complaint)</label>
              <span class="text-xs text-outline">Active complaint file</span>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="form.Complain" class="sr-only peer" />
              <div class="w-11 h-6 bg-outline-variant peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
            </label>
          </div>

          <div class="md:col-span-2 pt-6 border-t border-outline-variant flex justify-end">
            <button type="submit" :disabled="isPredicting" class="bg-primary text-on-primary px-8 py-3.5 rounded-xl font-bold flex items-center gap-3 hover:shadow-xl transition-all active:scale-95 disabled:opacity-50">
              <LineChart v-if="!isPredicting" class="w-5 h-5" />
              <span v-else class="w-5 h-5 border-2 border-white/20 border-t-white rounded-full animate-spin"></span>
              {{ isPredicting ? 'Predicting...' : 'Dự đoán rủi ro (Predict Churn Risk)' }}
            </button>
          </div>
        </form>
      </div>
    </section>

    <!-- Analysis Results -->
    <section class="col-span-12 lg:col-span-5 space-y-6">
      
      <template v-if="predictionResult">
        <!-- Churn Probability Gauge -->
        <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-8 shadow-sm text-center">
          <h3 class="text-base font-bold text-on-surface mb-8 text-left">Churn Probability</h3>
          
          <div class="relative w-44 h-44 mx-auto flex items-center justify-center">
            <svg class="absolute w-full h-full transform -rotate-90">
              <circle class="text-surface-container" cx="88" cy="88" r="80" fill="transparent" stroke="currentColor" stroke-width="12" />
              <circle 
                :class="predictionResult.risk_level === 'High' ? 'text-error' : (predictionResult.risk_level === 'Medium' ? 'text-orange-500' : 'text-green-500')" 
                cx="88" 
                cy="88" 
                r="80" 
                fill="transparent" 
                stroke="currentColor" 
                stroke-width="12" 
                stroke-dasharray="502.6" 
                :stroke-dashoffset="502.6 * (1 - (predictionResult.confidence / 100))" 
                stroke-linecap="round"
              />
            </svg>
            <div class="relative z-10 -mt-2">
              <span :class="['text-4xl font-bold block leading-none', predictionResult.risk_level === 'High' ? 'text-error' : (predictionResult.risk_level === 'Medium' ? 'text-orange-500' : 'text-green-500')]">
                {{ predictionResult.confidence }}%
              </span>
              <span class="text-[10px] font-bold text-outline uppercase tracking-widest mt-2 block">{{ predictionResult.risk_level }} Risk</span>
            </div>
          </div>

          <div :class="['mt-8 p-4 rounded-xl flex items-start gap-4 text-left border', 
            predictionResult.risk_level === 'High' ? 'bg-error-container/40 border-error/10 text-on-error-container' : 
            (predictionResult.risk_level === 'Medium' ? 'bg-orange-500/10 border-orange-500/20 text-orange-900' : 
            'bg-green-500/10 border-green-500/20 text-green-900')
          ]">
            <AlertTriangle v-if="predictionResult.risk_level === 'High' || predictionResult.risk_level === 'Medium'" :class="['w-5 h-5 shrink-0 mt-0.5', predictionResult.risk_level === 'High' ? 'text-error' : 'text-orange-500']" />
            <Info v-else class="w-5 h-5 text-green-500 shrink-0 mt-0.5" />
            <p class="text-xs leading-relaxed">
              {{ predictionResult.risk_level === 'High' ? 'Customer shows significant patterns associated with attrition. Immediate intervention is recommended.' : 
                 (predictionResult.risk_level === 'Medium' ? 'Customer shows some signs of potential churn. Consider a follow-up to ensure satisfaction.' : 
                 'Customer appears highly loyal and satisfied with minimal risk of churn.') }}
            </p>
          </div>
        </div>

        <!-- Feature Importance (XAI) -->
        <div class="bg-surface-container-lowest border border-outline-variant rounded-2xl p-8 shadow-sm">
          <div class="flex items-center gap-2 mb-8">
            <h3 class="text-base font-bold text-on-surface">Feature Importance (XAI)</h3>
            <Info class="w-4 h-4 text-outline" />
          </div>

          <div class="space-y-6">
            <div v-for="(feature, idx) in predictionResult.top_features" :key="idx" class="space-y-2">
              <div class="flex justify-between text-xs font-bold">
                <span class="text-on-surface">{{ feature.name }}</span>
                <span :class="feature.type === 'increase' ? 'text-error' : 'text-tertiary'">
                  {{ feature.type === 'increase' ? '+' : '-' }}{{ feature.value }}%
                </span>
              </div>
              <div class="w-full bg-surface-container h-2 rounded-full overflow-hidden">
                <div 
                  :class="cn(
                    'h-full rounded-full transition-all duration-1000',
                    feature.type === 'increase' ? 'bg-error' : 'bg-tertiary'
                  )"
                  :style="{ 
                    width: `${feature.value * 2}%`,
                    marginLeft: feature.type === 'decrease' ? 'auto' : '0' 
                  }"
                />
              </div>
            </div>
          </div>

          <div class="mt-8 flex justify-between gap-4 border-t border-outline-variant pt-6">
            <div class="flex items-center gap-2">
              <div class="w-3 h-3 bg-error rounded-sm"></div>
              <span class="text-[10px] font-bold text-outline uppercase tracking-wider">Increases Risk</span>
            </div>
            <div class="flex items-center gap-2">
              <div class="w-3 h-3 bg-tertiary rounded-sm"></div>
              <span class="text-[10px] font-bold text-outline uppercase tracking-wider">Reduces Risk</span>
            </div>
          </div>
        </div>

        <!-- Recommended Action -->
        <div class="bg-primary text-on-primary rounded-2xl p-8 shadow-xl relative overflow-hidden group">
          <div class="relative z-10">
            <h4 class="text-lg font-bold mb-3 flex items-center gap-2">
              <Sparkles class="w-5 h-5 text-secondary-container" />
              Recommended Action
            </h4>
            <p class="text-sm opacity-90 leading-relaxed mb-8">
              {{ predictionResult.risk_level === 'High' ? 'Generate a personalized retention offer including a 15% discount for the next 3 months.' : 
                 (predictionResult.risk_level === 'Medium' ? 'Send a simple check-in email and highlight recent feature updates or minor perks.' : 
                 'No immediate action required. Continue providing excellent service.') }}
            </p>
            <button class="w-full bg-white text-primary px-6 py-3 rounded-xl font-bold text-xs uppercase tracking-widest hover:bg-surface-container transition-all flex items-center justify-center gap-2">
              {{ predictionResult.risk_level === 'High' ? 'Draft Retention Email' : 'View Action Items' }}
              <ChevronRight class="w-4 h-4" />
            </button>
          </div>
          <Sparkles class="absolute -right-8 -bottom-8 w-40 h-40 text-white/10 rotate-12 transition-transform group-hover:scale-110 duration-500" />
        </div>
      </template>

      <!-- Empty State -->
      <div v-else class="bg-surface-container border border-outline-variant border-dashed rounded-2xl p-8 h-full flex flex-col items-center justify-center text-center">
        <LineChart class="w-12 h-12 text-outline mb-4 opacity-50" />
        <h3 class="text-lg font-bold text-on-surface mb-2">No Prediction Yet</h3>
        <p class="text-sm text-outline max-w-[250px]">
          Fill out the form and run a prediction to see the churn probability and AI analysis here.
        </p>
      </div>

    </section>
  </div>
</template>
