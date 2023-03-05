from dataclasses import dataclass
import os
import openai

gpt_auth_token = os.environ.get("GPT_AUTH_TOKEN")
openai.api_key = gpt_auth_token


@dataclass
class Judgement:
    is_important: bool
    reason: str
    all_statements: str


def check_importance(prompt: str) -> Judgement:
    response = openai.Completion.create(
        model="curie:ft-personal-2023-03-05-09-16-06",
        prompt=prompt,
        temperature=0,
        max_tokens=100,
    )
    response_text = response["choices"][0]["text"]
    # ジャッジ結果をパース
    judge = response_text.split("\n")[0]
    if judge.find("必要") != -1 or judge.find("不要") != -1:
        # 2行目が理由
        judge_reason = (
            response_text.split("\n")[1].split("理由: ")[1]
            if len(response_text.split("\n")[1].split("理由: ")) > 1
            else "不明"
        )

        return Judgement(
            # 1行目がジャッジ結果
            response_text.split("\n")[0].find("必要") != -1,
            judge_reason,
            response_text,
        )
    else:
        return Judgement(False, "不明", response_text)
