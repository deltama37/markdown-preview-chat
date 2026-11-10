# markdown-preview-chat

Markdown を Claude のアーティファクトでプレビューし、Notion のようにコメントでフィードバック →
Claude が `.md` を修正して再公開する、というループを回す Claude Code スキル。

## 構成

```
.claude/skills/md-review/
  SKILL.md       # Claude 向けの手順（公開 → コメント読む → 修正 → 再公開 → 返信・解決）
  render.py      # .md → アーティファクト用 HTML
  template.html  # プレビューページ（ライト/ダーク対応、Rev 表示）
examples/sample.md
```

## 使い方

1. このリポジトリで Claude Code を開き、`/md-review examples/sample.md` のように頼む。
2. 返ってきたアーティファクトのリンクを開く。
3. 直したい箇所のテキストを選択してコメント → **Send to Claude**。
4. Claude が `.md` を直し、同じ URL に Rev+1 で再公開して、スレッドに返信・解決する。

Send to Claude していない普通のコメントは自動では届かないので、チャットで「コメント反映して」と頼む。

## 手動レンダー

```bash
python3 .claude/skills/md-review/render.py examples/sample.md out/sample.html --rev 1
```
