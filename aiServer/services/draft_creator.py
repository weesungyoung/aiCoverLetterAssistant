from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# 자소서 초안 생성 함수
# 문항 유형 / 나의 경험 / 지원직무 / 지원산업군 / 기업 핵심역량 / 기업개요 / 기업뉴스 / 합격자 사례

def search_resume_from_db(query_text="직무: 백엔드 개발자 | 항목: 지원동기 | 키워드: 홈페이지, 물류", db_path="../my_coverletter_db"):
    embedding = OpenAIEmbeddings(model="text-embedding-3-large")

    vectorstore = Chroma(
        persist_directory=db_path,  
        embedding_function=embedding,   
        collection_name="coverletter_collection"
    )
    
    docs = vectorstore.similarity_search(
        query=query_text,
        k=3,
    )
    
    return docs


def create_draft(question_type, user_exp, user_job, user_industry, core_competencies, company_info, company_news):
    
   search_results = search_resume_from_db()
   references = ""

   for i, doc in enumerate(search_results):
      rank_info = f"\n[Rank {i+1}]"
    
      question_info = f"### 사례{i+1}\n질문: {doc.metadata.get('question', '질문 없음')}"
      answer_info = f"답변: {doc.metadata.get('answer', '답변 없음')}"
      
      # 출력
      print(rank_info)
      print(question_info)
      print(answer_info)
      
      # 변수 누적
      references += question_info + "\n" + answer_info + "\n\n"

   system_prompt = """
너는 국내 기업의 채용 트렌드를 꿰뚫고 있는 **자소서 전문 전략 컨설턴트**이다. 파편화된 사용자의 경험 데이터 및 기업 데이터(JSON 또는 텍스트 등)를 분석하여, 인사 담당자의 시선을 사로잡는 특별한 자기소개서 초안을 구성하는 것이 너의 핵심 임무이다.

--------------
참고자료
<문항 유형>
{question_type}

<사용자 경험>
{user_exp}

<지원직무>
{user_job}

<지원산업군>
{user_industry}

<핵심역량> (인재상, 직무 역량)
{core_competencies}

<기업개요> (사업내용, 브랜드)
{company_info}

<기업뉴스>
{company_news}

<합격자 사례> (참조용)
{references}

### 작성 가이드라인 (중요):
1. **기본 규칙**
   - 답변은 한국어로 작성하고 시작은 []에 들어간 소제목(본문을 창의적으로 요약) 형태로 시작해줘. 소제목 이후 **엔터**치고 본문을 작성해줘.
   - 본문은 문단구분 없이 하나의 텍스트로 작성해줘.
   - 자소서 작성 시 반드시 {question_type}에 대한 답변이 명확히 드러나야 해.
   - {user_exp}에 기반하여 작성해야 하며, 경험을 왜곡하거나 과장하지 마. 사용자가 제공한 데이터 속의 구체적인 수치(%, 명, 시간, 금액 등)와 고유 명사(프로젝트명, 툴 이름 등)를 절대 누락하지 않고 핵심 성과로 강조해줘.
   - 답변 분량은 500자~1000자 내외로 작성해줘.

2. **{question_type}에 따른 작성 가이드라인**
   - {question_type}이 지원동기, 포부/비전, 산업이해일 경우: {user_exp}보다는 {company_info}와 {company_news}를 반드시 참고하여 작성해줘.
   - {question_type}이 직무역량, 경험/성과, 문제해결, 성격/인성, 성장과정, 협업경험일 경우: {user_exp}을 중심으로, 해당 경험이 {user_industry} 산업의 {user_job} 직무에 잘 부합한다는 점을 명확히 연결지어 작성해줘. 사용자의 경험 {user_exp}에서 단순히 '무엇을 했다'를 넘어, 그 과정에서 발휘된 {core_competencies}가 돋보이게 작성해줘. 경험을 제시할 때 **상황-행동-성과-성찰의 흐름**이 명확해야 해.

3. **합격자 사례 벤치마킹 지침**
   - {references}의 구체적인 '경험 내용'이나 '수치'를 그대로 복제하지 마. 
   - 대신 그들이 사용한 **어휘**, **언어표현**, **문장의 흐름과 접속사**만 철저히 벤치마킹해.

""" 

   prompt = ChatPromptTemplate.from_template(system_prompt)

    # 모델 정의 (gpt-4o-mini, temperature=0.3)
   llm = ChatOpenAI(model="gpt-5-nano-2025-08-07", temperature=0.3)

    # chain생성
   chain = prompt | llm | StrOutputParser() 

    # 응답 출력 
   response = chain.invoke({
        "question_type": question_type,
        "user_exp": user_exp,
        "user_job": user_job,
        "user_industry": user_industry,
        "core_competencies": core_competencies,
        "company_info": company_info,
        "company_news": company_news,
        "references": references
    })

   return response
