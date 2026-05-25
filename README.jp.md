<div align="center">

# 豆包.skill

> *「すべてのAIエージェントが豆包を呼び出せるように——毎回ドキュメントを探す必要はない」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Hermes Agent](https://img.shields.io/badge/Hermes%20Agent-Skill-orange)](https://github.com/mattpocock/hermes)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-ff69b4)](https://openclaw.ai)
[![Skills](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)

<br>

**豆包大模型の能力をプラグ＆プレイのAIエージェントスキルに——会話、画像認識、ドキュメント理解、画像生成、動画生成。**

<br>

[例](#例) · [インストール](#インストール) · [サブスキル](#サブスキル) · [仕組み](#仕組み)

<br>

**他の言語:**

[中文](README.md) · [English](README.en.md) · [한국어](README.ko.md) · [Русский](README.ru.md)

</div>

---

## 例

**会話 & マルチモーダル（doubao-general）**

```
ユーザー  ❯ この決算報告書のスクリーンショットを分析して、Q3の前年比
            収益変化を教えて

豆包      ❯ スクリーンショットによると、Q3の収益は48.7億元で、
            前年同期の38.2億元から27.5%増加しました。
            成長の主な要因は広告事業（+35%）とクラウドサービス（+22%）です。
            粗利益率も58%から62%に改善しています。
```

```
ユーザー  ❯ このPDF契約書の主要条項を表形式で教えて

豆包      ❯ | 条項 | 内容 | リスク |
            |------|------|--------|
            | 違約責任 | 1日あたり万分の五の違約金 | 中 |
            | 知的財産権 | 委託者が全成果物の権利を保有 | 低 |
            | 秘密保持 | 双方に永久秘密保持義務 | 低 |
            | 排他条項 | 3年間競合他社へのサービス禁止 | ⚠️ 高 |
            排他条項は将来のビジネスを制限するため、1年に短縮するか
            補償条項を追加することを推奨します。
```

**画像生成（doubao-generate-image）**

```
ユーザー  ❯ ポスターを作成：秋のイチョウ並木、ベージュのトレンチコートを
            着た女性の後ろ姿、映画のような光、縦長

豆包      ❯ [9:16の縦長画像を生成]
            4K解像度で生成しました：https://ark-cn-beijing.volces.com/...
            ⚠️ URLの有効期限は24時間です。早めにダウンロードしてください。
```

**動画生成（doubao-generate-video）**

```
ユーザー  ❯ 5秒の動画を生成：草原を走るゴールデンレトリバー、
            スローモーション、午後の日差し

豆包      ❯ タスク作成: cgt-s6xcyoSh4BRx
            状態: 待機中 → 実行中 → 成功 (47秒)
            ダウンロード完了: output.mp4 (1080p, 5秒)
```

---

## インストール

```bash
npx skills add Trainerchan/doubao-skill
```

インストール後、会話で直接トリガー：

```
> この画像を豆包で分析して
> 販促用ポスターを生成して
> このPDFを豆包で要約して
```

### 手動インストール

```bash
git clone https://github.com/Trainerchan/doubao-skill.git
cd doubao-skill
cp .env.example .env
# .envを編集して ARK_API_KEY を設定
pip install volcengine-python-sdk python-dotenv
```

---

## サブスキル

| スキル | 能力 | モデル |
|--------|------|--------|
| 🔥 **doubao-general** | 会話、画像認識、ドキュメント/動画/音声理解、Web検索、関数呼び出し | doubao-seed-2.0-lite/pro/mini |
| 🔥 **doubao-generate-image** | テキスト→画像、画像→画像、グループ画像、複数画像融合 | doubao-seedream-5.0/4.5/4.0 |
| **doubao-generate-video** | テキスト→動画、画像→動画、マルチモーダル参照、音声同期 | doubao-seedance-2.0/1.5/1.0 |

> 動画生成にはアカウント残高200元以上またはリソースパックが必要です。

---

## 環境変数

| 変数 | 必須 | デフォルト | 説明 |
|------|:---:|--------|------|
| `ARK_API_KEY` | ✅ | — | 火山方舟 APIキー（[取得先](https://console.volcengine.com/ark/region:ark+cn-beijing/apiKey)） |
| `DOUBAO_CHAT_MODEL` | ❌ | `doubao-seed-2-0-lite-260428` | 会話モデルの上書き |
| `DOUBAO_IMAGE_MODEL` | ❌ | `doubao-seedream-5-0-260128` | 画像生成モデルの上書き |
| `DOUBAO_VIDEO_MODEL` | ❌ | `doubao-seedance-2-0-260128` | 動画生成モデルの上書き |

---

## 仕組み

**1. ルートマッチング** — 親スキルがユーザーの意図に応じて適切なサブスキルにルーティング。

**2. 自己実行サブスキル** — 各サブスキルは自己完結型：前提チェック、パラメータ参照表、コード例（cURL + Python）、エラー解決策を含む。

**3. エラー時のフォールバック** — APIがエラーを返した場合、エージェントは自動的にドキュメントクエリツールまたはWeb取得ツールを使用して最新パラメータを取得し、修正後に再試行。

---

## リポジトリ構造

```
doubao-skill/
├── SKILL.md                      # 親スキル：共通設定、サブスキルルーティング
├── REFERENCE.md                  # 親スキル参照：インストール、エージェント統合、リトライ
├── .env.example                  # 環境変数テンプレート
├── general/
│   ├── SKILL.md                  # 会話 & マルチモーダル（コア）
│   └── REFERENCE.md              # 拡張シナリオ、パラメータ表、エラー
├── generate-image/
│   ├── SKILL.md                  # 画像生成 Seedream（コア）
│   └── REFERENCE.md              # ストリーミング、パラメータ表、サイズ表
├── generate-video/
│   ├── SKILL.md                  # 動画生成 Seedance（コア）
│   ├── REFERENCE.md              # 拡張シナリオ、パラメータ表、解像度表
│   └── scripts/
│       └── poll_video.py         # 再利用可能なポーリング＆ダウンロード
├── docs/
│   └── agents/
└── CLAUDE.md                     # プロジェクト開発ガイド
```

コア機能とクイック例は SKILL.md（≤100行）に、完全なパラメータ表やエラーリファレンスは REFERENCE.md に分割——エージェントは必要なものを必要なときに読み込む。

---

## ライセンス

MIT

---

<div align="center">

すべての豆包呼び出しを、呼吸のように自然に。<br>
*ドキュメント不要。パラメータ探し不要。必要なことを言うだけ。*

<br>

MIT License © [Trainerchan](https://github.com/Trainerchan)

</div>
