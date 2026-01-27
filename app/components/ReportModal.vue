<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content report-size">
      <header class="modal-header">
        <div class="header-left">
          <span class="report-icon">📊</span>
          <h2>기업 상세 분석 리포트</h2>
        </div>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </header>

      <div class="modal-body report-body">
        <div v-if="reportHtml" v-html="reportHtml"></div>
        
        <div v-else class="dummy-report">
          <section class="report-section">
            <h3>🏢 기업 개요</h3>
            <p>본 기업은 생성형 AI 및 데이터 플랫폼 분야의 선두주자로...</p>
          </section>
          <section class="report-section">
            <h3>🎯 핵심 가치 (Core Value)</h3>
            <div class="keyword-group">
              <span class="keyword">혁신</span>
              <span class="keyword">도전</span>
              <span class="keyword">고객 중심</span>
            </div>
          </section>
          <section class="report-section">
            <h3>🔍 JD 핵심 분석 (Job Description)</h3>
            <p>해당 직무는 Python 기반의 대규모 데이터 처리 역량과 LLM 파인튜닝 경험을 최우선으로 요구함.</p>
          </section>
        </div>
      </div>

      <footer class="modal-footer">
        <button class="confirm-btn" @click="$emit('close')">확인</button>
      </footer>
    </div>
  </div>
</template>

<script setup>
defineProps(['reportHtml'])
defineEmits(['close'])
</script>

<style scoped>
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100%; height: 100%;
  background: rgba(0, 0, 0, 0.6); display: flex; align-items: center; justify-content: center; z-index: 9999;
}
.modal-content.report-size {
  width: 800px; max-width: 90%; max-height: 85vh; background: #fff; border-radius: 20px; display: flex; flex-direction: column; overflow: hidden;
}
.modal-header { padding: 20px 30px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
.header-left { display: flex; align-items: center; gap: 10px; }
.report-icon { font-size: 24px; }
.close-btn { background: none; border: none; font-size: 30px; cursor: pointer; color: #999; }

.modal-body { padding: 30px; overflow-y: auto; flex: 1; line-height: 1.7; }
.report-section { margin-bottom: 30px; }
.report-section h3 { color: #1d4ed8; font-size: 18px; margin-bottom: 10px; border-left: 4px solid #1d4ed8; padding-left: 10px; }
.keyword-group { display: flex; gap: 10px; margin-top: 10px; }
.keyword { background: #eff6ff; color: #1d4ed8; padding: 5px 12px; border-radius: 20px; font-size: 13px; font-weight: 600; }

.modal-footer { padding: 20px 30px; border-top: 1px solid #eee; text-align: right; }
.confirm-btn { background: #3b82f6; color: #fff; border: none; padding: 10px 24px; border-radius: 8px; font-weight: 700; cursor: pointer; }
</style>