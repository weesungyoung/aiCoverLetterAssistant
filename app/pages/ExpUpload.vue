<template>
  <div class="upload-page">
    <div class="content-body">
      <h1 class="page-title">경험 업로드</h1>
      
      <div class="upload-card">
        <div class="upload-icon-wrapper">
          <svg class="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
            <polyline points="14 2 14 8 20 8"></polyline>
            <line x1="12" y1="18" x2="12" y2="12"></line>
            <polyline points="9 15 12 12 15 15"></polyline>
          </svg>
        </div>
        
        <div class="text-group">
          <p class="main-text">경험 추출을 위해 기존에 작성한 자기소개서를 첨부해주세요.</p>
          <p class="sub-text">저장된 경험이 없을 경우 진행이 불가능합니다.</p>
        </div>

        <input 
          type="file" 
          ref="fileInput" 
          @change="handleFileChange" 
          accept=".pdf,.doc,.docx,.txt"
          style="display: none;" 
        />

        <button class="attach-btn" @click="triggerFileInput">
          첨부하기
        </button>

        <p class="direct-input-btn" @click="isModalOpen = true">직접 입력하기</p>
        
        <p v-if="fileName" class="selected-file-name">선택된 파일: {{ fileName }}</p>
      </div>
    </div>

    <ExperienceModal
      v-if="isModalOpen" 
      @close="isModalOpen = false" 
      @submit="handleExperienceSubmit"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ExperienceModal from '../components/ExpModal.vue'; 

const fileInput = ref(null); // input 태그에 접근하기 위한 변수
const fileName = ref('');    // 화면에 파일명을 표시하기 위한 변수
const isModalOpen = ref(false); // 모달 열림 상태 관리 변수

// 업로드 버튼 누르면 숨겨진 input 클릭
const triggerFileInput = () => {
  fileInput.value.click();
};

// 파일이 실제로 선택되었을 때 실행되는 함수
const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    fileName.value = file.name;
    console.log("업로드 준비 완료:", file);
    // 여기서 서버로 파일을 보내거나 다음 페이지로 넘기는 로직을 짭니다.
  }
};


// 모달에서 소재 만들기를 눌렀을 때 실행될 함수
const handleExperienceSubmit = (data) => {
  console.log("입력된 데이터:", data);
  isModalOpen.value = false;
  // 다음 페이지 이동 로직 (예: router.push('/loading'))
};
</script>

<style scoped>
.upload-page {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
}

.content-body {
  text-align: center;
  width: 100%;
  max-width: 800px;
}

.page-title {
  font-size: 1.8rem;
  font-weight: 800;
  margin-bottom: 60px;
}

/* 중앙 카드 스타일 */
.upload-card {
  border: 1px solid #e9ecef;
  border-radius: 20px;
  padding: 60px 40px;
  background-color: #ffffff;
  /* 살짝 그림자를 주어 입체감을 냅니다 */
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
}

.upload-icon-wrapper {
  margin-bottom: 25px;
}

.upload-icon {
  width: 80px;
  height: 80px;
  color: #000;
}

.text-group {
  margin-bottom: 30px;
}

.main-text {
  font-size: 1.1rem;
  font-weight: 600;
  margin-bottom: 10px;
}

.sub-text {
  font-size: 0.95rem;
  color: #000; /* 이미지에선 검은색 계열로 보이네요 */
  font-weight: 500;
}

/* 파란색 첨부하기 버튼 */
.attach-btn {
  background-color: #0000FF; /* 선명한 파란색 */
  color: white;
  border: none;
  padding: 12px 35px;
  border-radius: 10px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: opacity 0.2s;
}

.attach-btn:hover {
  opacity: 0.8;
}

.selected-file-name {
  margin-top: 15px;
  font-size: 0.9rem;
  color: #339af0;
  font-weight: bold;
}

.direct-input-btn {
  margin-top: 20px;
  color: #868e96; /* 이미지와 같은 회색 */
  text-decoration: underline; /* 밑줄 추가 */
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 500;
}

.direct-input-btn:hover {
  color: #495057; /* 호버 시 약간 진하게 */
}

</style>