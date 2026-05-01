"""
CrewAI動作確認テスト（最小構成: 2エージェント・1タスク）
"""
import os
from crewai import Agent, Task, Crew, Process

# 環境変数から読み込み（事前に設定すること）
# export ANTHROPIC_API_KEY="sk-ant-api03-xxxxx"

researcher = Agent(
    role="リサーチャー",
    goal="与えられたトピックについて要点を3つにまとめる",
    backstory="あなたは優秀なリサーチャーです。",
    verbose=True,
    llm="anthropic/claude-sonnet-4",
)

writer = Agent(
    role="ライター",
    goal="リサーチ結果を読みやすい文章にまとめる",
    backstory="あなたは文章作成のプロです。",
    verbose=True,
    llm="anthropic/claude-sonnet-4",
)

task = Task(
    description="「CrewAIとは何か」について100文字以内で日本語で説明してください。",
    expected_output="CrewAIの概要説明（日本語・100文字以内）",
    agent=writer,
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[task],
    process=Process.sequential,
    verbose=True,
)

if __name__ == "__main__":
    print("=== CrewAI テスト開始 ===")
    result = crew.kickoff()
    print("\n=== 結果 ===")
    print(result)
    print("\n=== テスト完了 ===")
