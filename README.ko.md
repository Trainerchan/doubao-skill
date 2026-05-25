<div align="center">

# 豆包.skill

> *"모든 AI 에이전트가 더우바오를 호출할 수 있도록 — 매번 문서를 뒤질 필요 없이"*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Hermes Agent](https://img.shields.io/badge/Hermes%20Agent-Skill-orange)](https://github.com/mattpocock/hermes)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-ff69b4)](https://openclaw.ai)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>

**더우바오 대형 모델의 기능을 플러그 앤 플레이 AI 에이전트 스킬로 — 대화, 이미지 인식, 문서 이해, 이미지 생성, 비디오 생성.**

<br>

[예시](#예시) · [설치](#설치) · [서브스킬](#서브스킬) · [작동 방식](#작동-방식)

<br>

**다른 언어:**

[中文](README.md) · [English](README.en.md) · [日本語](README.jp.md) · [Русский](README.ru.md)

</div>

---

## 예시

**대화 & 멀티모달 (doubao-general)**

```
사용자    ❯ 이 실적 보고서 스크린샷을 분석해줘, Q3 전년 대비 매출 변화는?

더우바오  ❯ 스크린샷 기준 Q3 매출은 48.7억 위안, 작년 동기 38.2억 위안 대비
            27.5% 증가했습니다. 주요 성장 동력은 광고(+35%)와 클라우드(+22%)입니다.
            매출총이익률도 58%에서 62%로 개선되었습니다.
```

```
사용자    ❯ 이 PDF 계약서의 핵심 조항을 표로 정리해줘

더우바오  ❯ | 조항 | 내용 | 위험도 |
            |------|------|--------|
            | 위약 책임 | 매일万分의五 위약금 | 중 |
            | 지식재산권 | 의뢰자가 모든 결과물 권리 보유 | 저 |
            | 비밀유지 | 쌍방 영구 비밀유지 의무 | 저 |
            | 배타 조항 | 3년간 경쟁사 서비스 금지 | ⚠️ 고 |
            배타 조항이 향후 비즈니스를 제한하므로 1년 단축 또는 보상 조항 추가 권장.
```

**이미지 생성 (doubao-generate-image)**

```
사용자    ❯ 포스터 생성: 가을 은행나무 길, 베이지 트렌치코트 입은 소녀의 뒷모습,
            시네마틱 라이팅, 세로형

더우바오  ❯ [9:16 세로 이미지 생성]
            4K 해상도 이미지: https://ark-cn-beijing.volces.com/...
            ⚠️ URL 유효기간 24시간, 즉시 다운로드하세요.
```

**비디오 생성 (doubao-generate-video)**

```
사용자    ❯ 5초 비디오: 초원을 달리는 골든 리트리버, 슬로우 모션, 오후 햇살

더우바오  ❯ 작업 생성됨: cgt-s6xcyoSh4BRx
            상태: 대기 → 실행 → 완료 (47초)
            다운로드 완료: output.mp4 (1080p, 5초)
```

---

## 설치

```bash
npx skills add Trainerchan/doubao-skill
```

설치 후 대화에서 직접 트리거:

```
> 이 이미지를 더우바오로 분석해줘
> 홍보 포스터 생성해줘
> 이 PDF를 더우바오로 요약해줘
```

### 수동 설치

```bash
git clone https://github.com/Trainerchan/doubao-skill.git
cd doubao-skill
cp .env.example .env
# .env 편집하여 ARK_API_KEY 설정
pip install volcengine-python-sdk python-dotenv
```

---

## 서브스킬

| 스킬 | 기능 | 모델 |
|------|------|------|
| 🔥 **doubao-general** | 대화, 이미지 인식, 문서/비디오/오디오 이해, 웹 검색, 함수 호출 | doubao-seed-2.0-lite/pro/mini |
| 🔥 **doubao-generate-image** | 텍스트→이미지, 이미지→이미지, 그룹 이미지, 다중 이미지 융합 | doubao-seedream-5.0/4.5/4.0 |
| **doubao-generate-video** | 텍스트→비디오, 이미지→비디오, 멀티모달 참조, 오디오 동기화 | doubao-seedance-2.0/1.5/1.0 |

> 비디오 생성은 계정 잔액 200위안 이상 또는 리소스 팩 필요.

---

## 환경 변수

| 변수 | 필수 | 기본값 | 설명 |
|------|:---:|--------|------|
| `ARK_API_KEY` | ✅ | — | 화산방주 API 키 ([발급처](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)) |
| `DOUBAO_CHAT_MODEL` | ❌ | `doubao-seed-2-0-lite-260428` | 대화 모델 재정의 |
| `DOUBAO_IMAGE_MODEL` | ❌ | `doubao-seedream-5-0-260128` | 이미지 생성 모델 재정의 |
| `DOUBAO_VIDEO_MODEL` | ❌ | `doubao-seedance-2-0-260128` | 비디오 생성 모델 재정의 |

---

## 작동 방식

**1. 라우트 매칭** — 부모 스킬이 사용자 의도에 따라 적절한 서브스킬로 라우팅.

**2. 자체 실행 서브스킬** — 각 서브스킬은 독립적: 전제 조건 확인, 매개변수 참조표, 코드 예제(cURL + Python), 오류 해결책 포함.

**3. 오류 시 폴백** — API 오류 발생 시 에이전트가 자동으로 문서 쿼리 도구 또는 웹 가져오기 도구로 최신 매개변수 조회 후 수정 재시도.

---

## 저장소 구조

```
doubao-skill/
├── SKILL.md                      # 부모 스킬: 공통 설정, 서브스킬 라우팅
├── REFERENCE.md                  # 부모 스킬 참조: 설치, 에이전트 통합, 재시도
├── .env.example                  # 환경 변수 템플릿
├── general/
│   ├── SKILL.md                  # 대화 & 멀티모달 (코어)
│   └── REFERENCE.md              # 확장 시나리오, 파라미터표, 오류
├── generate-image/
│   ├── SKILL.md                  # 이미지 생성 Seedream (코어)
│   └── REFERENCE.md              # 스트리밍, 파라미터표, 크기표
├── generate-video/
│   ├── SKILL.md                  # 비디오 생성 Seedance (코어)
│   ├── REFERENCE.md              # 확장 시나리오, 파라미터표, 해상도표
│   └── scripts/
│       └── poll_video.py         # 재사용 가능한 폴링 & 다운로드
├── docs/
│   └── agents/
└── CLAUDE.md                     # 프로젝트 개발 가이드
```

핵심 사용법과 빠른 예제는 SKILL.md(≤100줄)에, 전체 파라미터표와 오류 참조는 REFERENCE.md로 분리——에이전트가 필요한 만큼 로드, 효율성과 완전성의 균형.

---

## 라이선스

MIT

---

<div align="center">

모든 더우바오 호출을 숨쉬듯 자연스럽게.<br>
*문서 불필요. 매개변수 검색 불필요. 필요한 것만 말하면 됩니다.*

<br>

MIT License © [Trainerchan](https://github.com/Trainerchan)

</div>
