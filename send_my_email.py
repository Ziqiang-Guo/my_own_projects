import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import datetime
import os
from openai import OpenAI

print("程序开始运行...")

# 邮件配置
SENDER_EMAIL = "ziqiangguo000@gmail.com"  # 发送者邮箱
SENDER_PASSWORD = "czku akix qdsm ebmq"   # 邮箱应用专用密码
RECEIVER_EMAIL = "z9guo@uwaterloo.ca"  # 接收者邮箱
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

print(f"邮件配置已加载: 发件人 {SENDER_EMAIL} -> 收件人 {RECEIVER_EMAIL}")

# OpenAI配置
client = OpenAI(api_key='61c48aac-1117-49ff-a941-cdd390655c62', base_url="https://ark.cn-beijing.volces.com/api/v3/bots")
print("OpenAI客户端已初始化")

def generate_motivation():
    """使用OpenAI生成励志语句"""
    print("正在生成励志语句...")
    try:
        response = client.chat.completions.create(
            model="bot-20250225101537-b7ddt",
            messages=[
                {"role": "system", "content": "你是一个励志语句生成器。请只返回一句励志语句，用双引号包裹。不需要作者署名，不要添加任何其他解释或建议。"},
                {"role": "user", "content": "给我一句励志名言"}
            ]
        )
        # 获取内容并处理：只保留第一对引号之间的内容
        raw_content = response.choices[0].message.content.strip()
        motivation = raw_content
        if '“' in raw_content:
            # 找到第一个和第二个引号的位置
            first_quote = raw_content.find('“')
            second_quote = raw_content.find('”', first_quote + 1)
            if second_quote != -1:
                motivation = raw_content[first_quote + 1:second_quote]
            else:
                motivation = raw_content
        else:
            motivation = raw_content
            
        print(f"励志语句生成成功: {motivation}")
        return motivation
    except Exception as e:
        print(f"生成励志语句时出错: {str(e)}")
        return "生活总是充满希望，让我们继续前进！"

def send_email(subject, body):
    """发送邮件"""
    print("\n准备发送邮件...")
    print(f"邮件主题: {subject}")
    
    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))
    print("邮件内容已组装完成")

    try:
        print(f"正在连接到SMTP服务器 {SMTP_SERVER}:{SMTP_PORT}...")
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=50)
        print("连接成功，正在启动TLS...")
        print("正在登录邮箱...")
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("正在发送邮件...")
        server.send_message(msg)
        server.quit()
        print("邮件发送成功！")
    except Exception as e:
        print(f"发送邮件时出错: {str(e)}")

def main():
    print("\n=== 开始执行主程序 ===")
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    motivation = generate_motivation()
    
    # 检查是否是生日
    is_birthday = today == "2025-04-10"
    if is_birthday:
        print("今天是生日！")
        subject = f"生日快乐！今日励志语句 - {today}"
        body = f"""
亲爱的朋友：

🎂 生日快乐！愿你在新的一年里事事顺心！
愿你在生活的每一个阶段都能找到属于自己的快乐和满足。

希望这句话能给你力量：

{motivation}

祝你生日快乐，前程似锦！
"""
    else:
        print("今天是普通的一天")
        subject = f"今日励志语句 - {today}"
        body = f"""
亲爱的朋友：

希望这句话能给你力量：

{motivation}

祝你今天过得愉快！
"""
    
    send_email(subject, body)
    print("=== 程序执行完毕 ===")

if __name__ == "__main__":
    main()