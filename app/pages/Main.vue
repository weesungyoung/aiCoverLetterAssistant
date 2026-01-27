<template>
  <div class="container">
    <main :class="['main-content', { 'expanded': !isSidebarOpen }]">
      <header class="top-header">
        <button class="help-btn">?</button>
      </header>

      <div class="content-body">
        <h1 class="main-title">서비스이름</h1>
        
        <div class="input-container">
          <input 
            v-model="jobLink"
            type="text" 
            placeholder="채용 공고 링크를 입력해주세요." 
            class="url-input"
          />
          <button class="search-submit" @click="startAnalysis">↑</button>
        </div>
        <p class="notice">링크를 입력하면 기업 분석이 시작됩니다.</p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const jobLink = ref(''); 

const startAnalysis = () => {
  if (!jobLink.value) {
    alert('채용 공고 링크를 입력해주세요!');
    return;
  }
  router.push('/upload'); 
};
</script>

<style scoped>
/* 전체 레이아웃 */
.container {
  display: flex;
  height: 100vh;
  width: 100vw;
  font-family: 'Pretendard', sans-serif;
  background-color: #ffffff;
}

/* 메인 컨텐츠 영역 (가운데 정렬) */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background-color: #ffffff;
  transition: margin 0.3s ease;
}

.top-header {
  height: 80px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding-right: 40px;
}

.help-btn {
  width: 40px;
  height: 40px;
  background-color: #212529;
  color: white;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  font-size: 1.2rem;
}

.content-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* 가운데 정렬 */
  padding-bottom: 10vh; /* 하단 쏠림 방지 및 위치 조절 */
}

.main-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 60px;
  letter-spacing: -2px;
}

/* 입력창 스타일 */
.input-container {
  width: 100%;
  max-width: 700px;
  position: relative;
  display: flex;
  align-items: center;
}

.url-input {
  width: 100%;
  padding: 20px 30px;
  font-size: 1.1rem;
  border: 2px solid #f1f3f5;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.05);
  outline: none;
  transition: border-color 0.2s;
}

.url-input:focus {
  border-color: #339af0;
}

.search-submit {
  position: absolute;
  right: 15px;
  width: 45px;
  height: 45px;
  background-color: #339af0; /* 파란색 계열 */
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.5rem;
  cursor: pointer;
  transition: background 0.2s;
}

.search-submit:hover {
  background-color: #228be6;
}

.notice {
  margin-top: 20px;
  color: #adb5bd;
  font-size: 0.9rem;
}
</style>