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


def generatePrompt(mailSummary: str):
    return f"""メールの件名と、本文の文頭を渡すので、そのメールを読む必要があるかと、その理由を出力してください。下記のポイントに沿って、メールを読む必要があるかを判断してください。
    - ただの報告、勧誘やキャンペーンなどの、メールの本文を読む必要がないものは、通知不要です。
    - 知り合いや契約先、関係者からの依頼など、何かしらの対応が必要なものは、通知してください。

    Mail: 開発全体方針すり合わせ でんでんのSpeeeのZoomhttps://speee.zoom.us/j/hogefuga#successアジェンダ方向性（fromはしたつ）開発手段のログの確認※録音したい この予定は更新されました 変更あり: 説明 説明 変更されました でんでんのSpeeeのZoom https://speee.zoom.us/j/hogefuga#success アジェンダ
    Responce: 必要, すり合わせのための会議という要件があり、zoomリンクが含まれているので、必要
    Mail: HOTPEPPER Beauty はしもとさん ※このメールは、HOT PEPPER Beautyにてヘアサロン・リラク＆ビューティーサロンをご予約された方全員へお送りしております。 サロンへ直接キャンセルのご連絡をいただいた方にも、このメールが届く可能性がございます。その際にはご了承ください。 この度はHOT PEPPER Beautyをご利用いただき、ありがとうございました。 ご来店されたサロン
    Responce: 不要, Webサービスから来た、ただの予約の通知なので通知不要
    Mail: 過日登録されたhogehoge.netについて、 Whois情報公開代行の転送設定が無効です。 設定を有効にすると、Whois情報公開代行利用時の Whois情報掲載メールアドレス宛にきたメールをお客様指定のメールアドレスで転送受信できるようになります。 ▼さっそく設定する https://www.onamae.com/domain/navi/quick_option?lang=
    Responce: 不要, 対応が必要に見せかけた、ただの宣伝メール、ゴミ
    Mail: {mailSummary}
    Responce: """


def check_importance(prompt: str) -> Judgement:
    print("prompt:", prompt)
    response = openai.Completion.create(
        model="curie:ft-personal-2023-03-05-08-17-43",
        prompt=prompt,
        temperature=0,
        max_tokens=100,
    )
    response_text = response["choices"][0]["text"]
    # ジャッジ結果をパース
    judge_result = "必要"
    judge_reason = "不明"
    if len(response_text.split(",")) > 1:
        judge_result = response_text.split(",")[0].replace(" ", "")
        judge_reason = response_text.split(",")[1].replace(" ", "")
        return Judgement(judge_result == "必要", judge_reason, response_text)
    else:
        return Judgement(False, judge_reason, response_text)
