"""
SNS分析チーム - CrewAI マルチエージェント
==========================================
10人のAIエージェントがSNSアカウントのBAN対策・運用改善を分析するチーム。
model: anthropic/claude-sonnet-4
"""

import os
from crewai import Agent, Task, Crew, Process

# --- 環境変数 ---
# 事前に設定すること: export ANTHROPIC_API_KEY="sk-ant-api03-xxxxx"
assert os.getenv("ANTHROPIC_API_KEY"), "ANTHROPIC_API_KEY 環境変数を設定してください"

MODEL = "anthropic/claude-sonnet-4"

# ============================================================
# エージェント定義（10名）
# ============================================================

sns_researcher = Agent(
    role="SNSリサーチャー",
    goal="対象アカウントの投稿内容・頻度・使用ハッシュタグ・エンゲージメントパターンを網羅的に調査する",
    backstory=(
        "あなたはSNSマーケティングリサーチの第一人者です。"
        "TikTok、Instagram、Facebook、X(Twitter)、YouTube等あらゆるプラットフォームの"
        "投稿データを分析し、アカウントの現状を把握するスペシャリストです。"
    ),
    verbose=True,
    llm=MODEL,
)

ban_risk_analyst = Agent(
    role="BANリスク分析官",
    goal="アカウントがBAN・制限を受けるリスクを評価し、具体的なリスク要因を特定する",
    backstory=(
        "あなたはSNSプラットフォームのモデレーション基準に精通した分析官です。"
        "過去数千件のBAN事例を調査し、パターンを見抜く能力を持っています。"
        "シャドウバン・一時制限・永久BANの違いも正確に判別できます。"
    ),
    verbose=True,
    llm=MODEL,
)

platform_rules_expert = Agent(
    role="プラットフォーム規約専門家",
    goal="各SNSプラットフォームの最新利用規約・コミュニティガイドラインを正確に把握し、違反リスクを指摘する",
    backstory=(
        "あなたは各SNSの利用規約・コミュニティガイドラインを熟知した法務寄りの専門家です。"
        "TikTok、Instagram、Facebook、X、YouTubeそれぞれの規約の違いを理解し、"
        "グレーゾーンの判断も的確に行えます。"
    ),
    verbose=True,
    llm=MODEL,
)

content_strategist = Agent(
    role="コンテンツ戦略家",
    goal="BANリスクを回避しつつ、エンゲージメントを最大化するコンテンツ改善提案を行う",
    backstory=(
        "あなたはSNSコンテンツ戦略のプロフェッショナルです。"
        "規約を守りながらもバズるコンテンツを企画し、"
        "アルゴリズムに好まれる投稿スタイルを熟知しています。"
    ),
    verbose=True,
    llm=MODEL,
)

competitor_analyst = Agent(
    role="競合分析官",
    goal="同業種・競合アカウントの成功事例と失敗事例を分析し、ベンチマークを提供する",
    backstory=(
        "あなたは競合分析のスペシャリストです。"
        "業界内の成功アカウントがなぜ成長したか、"
        "BANされたアカウントがどのような投稿でペナルティを受けたかを調査します。"
    ),
    verbose=True,
    llm=MODEL,
)

data_analyst = Agent(
    role="データアナリスト",
    goal="エンゲージメント率・リーチ・インプレッション等の定量データを分析し、傾向を可視化する",
    backstory=(
        "あなたはSNSデータ分析の専門家です。"
        "投稿ごとのエンゲージメント率、フォロワー増減、"
        "最適投稿時間帯などを統計的に分析する能力を持っています。"
    ),
    verbose=True,
    llm=MODEL,
)

multilingual_expert = Agent(
    role="多言語コンテンツ専門家",
    goal="日本語・ベトナム語・ネパール語でのコンテンツ最適化と多言語SNS運用の改善を提案する",
    backstory=(
        "あなたは多言語SNSマーケティングの専門家です。"
        "日本語圏・ベトナム語圏・ネパール語圏それぞれのSNS文化や"
        "好まれるコンテンツスタイルに精通しています。"
        "特に外国人材採用に関するSNS発信に詳しいです。"
    ),
    verbose=True,
    llm=MODEL,
)

device_network_expert = Agent(
    role="デバイス・ネットワーク専門家",
    goal="アカウントの安全管理（デバイス、IPアドレス、VPN使用等）を分析し、技術的リスクを軽減する",
    backstory=(
        "あなたはSNSアカウントの技術的安全管理の専門家です。"
        "複数デバイスからのログイン、IP変動、VPN使用、"
        "ブラウザフィンガープリント等がアカウントBANに与える影響を熟知しています。"
    ),
    verbose=True,
    llm=MODEL,
)

recovery_expert = Agent(
    role="復旧・異議申立専門家",
    goal="BAN後のアカウント復旧手順・異議申立方法を策定し、成功率を最大化する",
    backstory=(
        "あなたはSNSアカウントの復旧・異議申立のエキスパートです。"
        "各プラットフォームの異議申立フォーム、連絡先、"
        "成功率の高いメッセージテンプレートを持っています。"
    ),
    verbose=True,
    llm=MODEL,
)

general_manager = Agent(
    role="総合マネージャー",
    goal="全エージェントの分析結果を統合し、経営者向けの包括的なレポートを作成する",
    backstory=(
        "あなたはSNSマーケティングチームの統括マネージャーです。"
        "各専門家の分析結果をまとめ、経営者が意思決定しやすい"
        "優先順位付きのアクションプランを作成します。"
    ),
    verbose=True,
    llm=MODEL,
)

# ============================================================
# タスク定義
# ============================================================

def create_tasks(target_account: str, platform: str = "TikTok"):
    """指定されたアカウント・プラットフォームに対するタスクを生成"""

    task_research = Task(
        description=f"""
        {platform}アカウント「{target_account}」の投稿内容を調査してください。
        - 直近の投稿の傾向（テーマ、頻度、時間帯）
        - 使用しているハッシュタグ
        - エンゲージメントの特徴
        - フォロワー層の推定
        """,
        expected_output="アカウントの投稿パターンと現状の詳細レポート",
        agent=sns_researcher,
    )

    task_ban_risk = Task(
        description=f"""
        {platform}アカウント「{target_account}」のBANリスクを評価してください。
        - 規約違反の可能性がある投稿パターン
        - シャドウバンの兆候
        - リスクレベル（高・中・低）の判定
        - 過去のペナルティ履歴の推定
        """,
        expected_output="BANリスク評価レポート（リスクレベル付き）",
        agent=ban_risk_analyst,
    )

    task_rules = Task(
        description=f"""
        {platform}の最新の利用規約・コミュニティガイドラインを確認し、
        「{target_account}」が注意すべきポイントをまとめてください。
        - 禁止コンテンツ一覧
        - グレーゾーンの判断基準
        - 最近の規約変更点
        """,
        expected_output="プラットフォーム規約に基づくリスクポイントまとめ",
        agent=platform_rules_expert,
    )

    task_strategy = Task(
        description=f"""
        BANリスクを避けながらエンゲージメントを向上させる
        コンテンツ戦略を提案してください。
        - 安全なコンテンツカテゴリ
        - 推奨投稿頻度・時間帯
        - ハッシュタグ戦略
        - アルゴリズム対策
        """,
        expected_output="具体的なコンテンツ改善提案（5つ以上のアクションアイテム）",
        agent=content_strategist,
    )

    task_competitor = Task(
        description=f"""
        {platform}上の競合・同業種アカウントを分析してください。
        - 成功しているアカウントの共通パターン
        - BANされたアカウントの失敗パターン
        - ベンチマーク数値
        """,
        expected_output="競合分析レポート（成功・失敗パターン付き）",
        agent=competitor_analyst,
    )

    task_data = Task(
        description=f"""
        「{target_account}」のエンゲージメントデータを分析してください。
        - エンゲージメント率の推定
        - 最適投稿時間帯
        - フォロワー成長トレンド
        - コンテンツ種別ごとのパフォーマンス比較
        """,
        expected_output="定量データ分析レポート",
        agent=data_analyst,
    )

    task_multilingual = Task(
        description=f"""
        「{target_account}」の多言語展開の可能性を分析してください。
        - 日本語コンテンツの最適化ポイント
        - ベトナム語・ネパール語圏向けコンテンツの提案
        - 外国人材採用に効果的なSNS発信方法
        - 多言語ハッシュタグ戦略
        """,
        expected_output="多言語コンテンツ戦略レポート",
        agent=multilingual_expert,
    )

    task_device = Task(
        description=f"""
        「{target_account}」のアカウント安全管理について分析してください。
        - 複数デバイスログインのリスク
        - IP・VPN関連のリスク
        - 推奨セキュリティ設定
        - アカウント連携の安全性
        """,
        expected_output="デバイス・ネットワーク安全管理レポート",
        agent=device_network_expert,
    )

    task_recovery = Task(
        description=f"""
        万が一「{target_account}」がBANされた場合の復旧戦略を策定してください。
        - 異議申立の手順（{platform}固有）
        - 成功率の高い申立文テンプレート
        - 代替アカウント運用のリスクと対策
        - BAN後のフォロワー維持策
        """,
        expected_output="BAN復旧マニュアル（テンプレート付き）",
        agent=recovery_expert,
    )

    task_final_report = Task(
        description=f"""
        全チームメンバーの分析結果を統合し、経営者向けの最終レポートを作成してください。

        レポートに含める内容：
        1. エグゼクティブサマリー（3行）
        2. 現状評価（BANリスクレベル含む）
        3. 優先対応事項TOP5
        4. 具体的アクションプラン（担当・期限付き）
        5. 多言語展開の推奨事項
        6. 緊急時（BAN発生時）の対応フロー

        対象: {platform}アカウント「{target_account}」
        """,
        expected_output="経営者向け包括レポート（日本語・A4で3-5ページ相当）",
        agent=general_manager,
    )

    return [
        task_research, task_ban_risk, task_rules,
        task_strategy, task_competitor, task_data,
        task_multilingual, task_device, task_recovery,
        task_final_report,
    ]


def run_crew(target_account: str, platform: str = "TikTok"):
    """Crewを実行してSNS分析を行う"""
    tasks = create_tasks(target_account, platform)

    crew = Crew(
        agents=[
            sns_researcher, ban_risk_analyst, platform_rules_expert,
            content_strategist, competitor_analyst, data_analyst,
            multilingual_expert, device_network_expert, recovery_expert,
            general_manager,
        ],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()
    return result


# ============================================================
# メイン実行
# ============================================================
if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "テストアカウント"
    platform = sys.argv[2] if len(sys.argv) > 2 else "TikTok"

    print(f"\n{'='*60}")
    print(f"  SNS分析チーム起動")
    print(f"  対象: {target} ({platform})")
    print(f"  エージェント数: 10名")
    print(f"  モデル: {MODEL}")
    print(f"{'='*60}\n")

    result = run_crew(target, platform)

    print(f"\n{'='*60}")
    print("  最終レポート")
    print(f"{'='*60}")
    print(result)
