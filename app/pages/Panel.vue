<template>
  <aside class="editor-right">
    <nav class="right-tabs">
      <button 
        v-for="tab in tabList" 
        :key="tab.id"
        :class="['tab-pill', { active: currentTab === tab.id }]" 
        @click="currentTab = tab.id"
      >
        {{ tab.label }}
      </button>
    </nav>

    <div class="right-content-scroll">
      <keep-alive>
        <component 
          :is="tabComponents[currentTab]" 
          :active-question="activeQuestion"
          :materials="materials"
          :selected-materials="selectedMaterials"
          @update:selected-materials="$emit('update:selectedMaterials', $event)"
          @open-modal="$emit('open-modal')"
        />
      </keep-alive>
    </div>
  </aside>
</template>

<script setup>
import { ref } from 'vue'
import StepDraft from '../components/panel/StepDraft.vue'

// 나중에 만들 컴포넌트들 (현재는 비워둬도 됨)
const StepFeedback = { template: '<div class="empty-state">피드백 기능 준비 중...</div>' }
const StepSubhead = { template: '<div class="empty-state">소제목 추천 기능 준비 중...</div>' }

const props = defineProps(['activeQuestion', 'materials', 'selectedMaterials'])
const emit = defineEmits(['open-modal', 'update:selectedMaterials'])

const currentTab = ref('draft')

const tabList = [
  { id: 'draft', label: '초안 생성' },
  { id: 'feedback', label: '피드백 받기' },
  { id: 'subhead', label: '소제목 추천' }
]

const tabComponents = {
  draft: StepDraft,
  feedback: StepFeedback,
  subhead: StepSubhead
}
</script>

<style scoped>
/* Panel 전체 레이아웃만 남김 */
.editor-right { flex: 0 0 40%; background-color: #f8fafc; display: flex; flex-direction: column; padding: 40px 30px; box-sizing: border-box; }
.right-tabs { display: flex; gap: 15px; border-bottom: 1px solid #e2e8f0; margin-bottom: 20px; }
.tab-pill { background: none; border: none; padding: 10px 0; color: #94a3b8; cursor: pointer; font-size: 14px; }
.tab-pill.active { color: #1d4ed8; font-weight: 700; border-bottom: 2px solid #1d4ed8; }
.right-content-scroll { flex: 1; overflow-y: auto; }
.empty-state { padding: 40px; text-align: center; color: #94a3b8; }
</style>