<template>
  <div class="upload-page-wrapper">
    <Sidebar />
    
    <main class="main-content">
      <header class="page-header">
        <h1 class="page-title">경험 업로드</h1>
        <p class="page-subtitle">자기소개서 파일을 첨부하거나 경험을 직접 입력하여 AI 분석을 시작하세요.</p>
      </header>

      <section class="upload-section">
        <div v-if="isLoading" class="loading-state">
          <div class="spinner"></div>
          <p>데이터를 분석하고 저장하는 중입니다...</p>
        </div>

        <div v-else class="action-group">
          <div class="upload-item" @click="triggerFileInput">
            <div class="icon-box">
              <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="12" y1="18" x2="12" y2="12"></line>
                <polyline points="9 15 12 12 15 15"></polyline>
              </svg>
            </div>
            <div class="item-text">
              <h3>PDF 파일 첨부</h3>
              <p>작성해둔 자기소개서에서 경험을 추출합니다.</p>
              <span v-if="fileName" class="file-status">선택됨: {{ fileName }}</span>
            </div>
            <button class="btn-primary">파일 선택</button>
            <input type="file" ref="fileInput" @change="handleFileChange" accept=".pdf" style="display: none;" />
          </div>

          <div class="upload-item" @click="isModalOpen = true">
            <div class="icon-box">
              <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
              </svg>
            </div>
            <div class="item-text">
              <h3>직접 입력하기</h3>
              <p>STARI 기법에 맞춰 경험을 새로 작성합니다.</p>
            </div>
            <button class="btn-secondary">입력창 열기</button>
          </div>

          <div class="upload-item" @click="router.push('/editor')">
            <div class="icon-box highlight">
              <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M12 19l7-7 3 3-7 7-3-3z"></path>
                <path d="M18 13l-1.5-7.5L2 2l3.5 14.5L13 18l5-5z"></path>
                <path d="M2 2l7.5 1.5"></path>
                <path d="M7.5 24l-3-3"></path>
              </svg>
            </div>
            <div class="item-text">
              <h3>바로 초안 작성</h3>
              <p>경험 정리 없이 AI와 함께 자소서를 씁니다.</p>
            </div>
            <button class="btn-outline">작성 시작</button>
          </div>
        </div>
      </section>

      <ExperienceModal
        v-if="isModalOpen" 
        @close="isModalOpen = false" 
        @submit="handleExperienceSubmit"
      />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';
import ExperienceModal from '../components/ExpModal.vue'; 
import Sidebar from '../components/Sidebar.vue';

const router = useRouter();
const fileInput = ref(null);
const fileName = ref('');
const isModalOpen = ref(false);
const isLoading = ref(false);

const triggerFileInput = () => {
  fileInput.value.click();
};

// 성공 알림 함수
const handleSuccess = () => {
  alert("경험 저장소에 저장되었습니다! 🚀");
};

// PDF 업로드 및 분석
const handleFileChange = async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  const userInfo = JSON.parse(localStorage.getItem("userInfo"));
  const email = userInfo?.email || "";
  fileName.value = file.name;
  isLoading.value = true;

  const formData = new FormData();
  formData.append('file', file);
  formData.append('userEmail', email);

  try {
    const response = await axios.post('http://localhost:8000/analyze/pdf', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
    
    // 분석 결과가 있으면 DB 저장
    if (response.data) {
      await axios.post("/api/insertExp", { email: email, data: response.data });
      handleSuccess(); // 성공 메시지 표시
    }
  } catch (error) {
    console.error("PDF 분석 실패:", error);
    alert("파일 분석 중 오류가 발생했습니다.");
  } finally {
    isLoading.value = false;
    fileName.value = ''; // 파일명 초기화
  }
};

// 직접 입력 데이터 전송
const handleExperienceSubmit = async (experienceList) => {
  isModalOpen.value = false;
  isLoading.value = true;

  try {
    const userInfo = JSON.parse(localStorage.getItem("userInfo"));
    const email = userInfo?.email || "";
    const response = await axios.post('http://localhost:8000/analyze/json', { 
      userEmail: email, 
      data: experienceList 
    });
    
    if (response.data) {
      await axios.post("/api/insertExp", { email: email, data: response.data });
      handleSuccess(); // 성공 메시지 표시
    }
  } catch (error) {
    console.error("복수 데이터 전송 실패:", error);
    alert("데이터 분석 중 오류가 발생했습니다.");
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
/* (이전 스타일과 동일, .result-section 관련 스타일은 제거됨) */
.upload-page-wrapper { display: flex; min-height: 100vh; background-color: #f9f9fb; }
.main-content { flex: 1; padding: 60px 50px; max-width: 1400px; margin: 0 auto; }
.page-header { margin-bottom: 50px; text-align: left; }
.page-title { font-size: 2.2rem; font-weight: 800; color: #111; margin-bottom: 12px; }
.page-subtitle { color: #666; font-size: 1.1rem; }
.action-group { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }
.upload-item {
  display: flex; flex-direction: column; align-items: center; justify-content: space-between;
  padding: 50px 30px; background: white; border: 1px solid #eee; border-radius: 24px;
  cursor: pointer; transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  min-height: 400px; text-align: center;
}
.upload-item:hover { border-color: #0000FF; transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,255,0.08); }
.icon-box { width: 80px; height: 80px; background: #f0f3ff; border-radius: 20px; display: flex; align-items: center; justify-content: center; margin-bottom: 25px; }
.icon-box.highlight { background: #EBF5FF; }
.icon { width: 36px; height: 36px; color: #0000FF; }
.item-text { flex: 1; display: flex; flex-direction: column; justify-content: center; }
.item-text h3 { font-size: 1.4rem; font-weight: 700; margin-bottom: 12px; color: #111; }
.item-text p { font-size: 1rem; color: #888; line-height: 1.6; word-break: keep-all; }
.file-status { display: block; margin-top: 12px; color: #0000FF; font-weight: bold; font-size: 0.9rem; }
.btn-primary, .btn-secondary, .btn-outline {
  width: 100%; margin-top: 30px; padding: 14px 0; border-radius: 12px; font-weight: 700; font-size: 1rem;
  cursor: pointer; transition: all 0.2s ease; background-color: white !important;
  color: #0000FF !important; border: 2px solid #0000FF !important;
}
.btn-primary:hover, .btn-secondary:hover, .btn-outline:hover { background-color: #f0f3ff !important; box-shadow: 0 4px 12px rgba(0, 0, 255, 0.1); }
.loading-state { text-align: center; padding: 100px 0; }
.spinner { width: 60px; height: 60px; border: 6px solid #f3f3f3; border-top: 6px solid #0000FF; border-radius: 50%; animation: spin 1s linear infinite; margin: 0 auto 25px; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
@media (max-width: 1024px) { .action-group { grid-template-columns: 1fr; max-width: 500px; margin: 0 auto; } .upload-item { min-height: auto; } }
</style>