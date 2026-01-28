import pdfplumber
import io
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# PDF 파일에서 텍스트 추출 함수
def extract_text_from_pdf(file_content: bytes) -> str:
    text = ""
    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()

import openai
import json

def process_experience(data, is_json=False):
    client = openai.OpenAI(api_key="YOUR_KEY")
    
    if is_json:
        # 1. 이미 분리된 경우: 키워드와 타이틀만 추출
        prompt = f"""
        다음은 사용자가 STAR 기법으로 직접 작성한 경험 데이터입니다.
        이 내용을 바탕으로 1) 전문적인 제목을 짓고, 2) 핵심 역량 키워드 3개를 추출해줘.
        
        데이터: {json.dumps(data, ensure_ascii=False)}
        """
    else:
        # 2. 통짜 PDF 텍스트인 경우: STAR 분류 + 키워드 + 타이틀 전체 추출
        prompt = f"""
        다음은 사용자의 경험 원문입니다.
        이 내용을 1) STAR 기법으로 분류하고, 2) 전문적인 제목을 짓고, 3) 핵심 키워드 3개를 추출해줘.
        
        원문: {data}
        """

    # 공통 JSON 출력 가이드
    prompt += """
    반드시 다음 JSON 형식으로만 출력해:
    {
      "title": "...",
      "classifyStart": {"S": "...", "T": "...", "A": "...", "R": "..."},
      "keywords": ["...", "...", "..."]
    }
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    
    result = json.loads(response.choices[0].message.content)

    # 만약 이미 JSON이었다면, 전달받은 S, T, A, R을 그대로 유지하거나 
    # AI가 다듬은 버전으로 덮어씌울 수 있습니다.
    if is_json:
        result['classifyStart'] = data # 원본 데이터 유지할 경우
        
    return result