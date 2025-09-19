import os
import time
import requests
from playwright.sync_api import sync_playwright, Cookie, TimeoutError as PlaywrightTimeoutError

def send_telegram_message(message, screenshot_path=None):
    """
    发送 Telegram 消息，可附带截图。
    需要设置环境变量 TELEGRAM_BOT_TOKEN 和 TELEGRAM_CHAT_ID
    """
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("未设置 TELEGRAM_BOT_TOKEN 或 TELEGRAM_CHAT_ID，跳过 Telegram 通知。")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}

    try:
        requests.post(url, data=data, timeout=20)
    except Exception as e:
        print(f"发送文字消息失败: {e}")

    if screenshot_path and os.path.exists(screenshot_path):
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        files = {"photo": open(screenshot_path, "rb")}
        data = {"chat_id": chat_id, "caption": f"📷 {message}"}
        try:
            requests.post(url, data=data, files=files, timeout=30)
        except Exception as e:
            print(f"发送截图失败: {e}")

def add_server_time(server_url="https://hub.weirdhost.xyz/server/1d308dcb"):
    """
    尝试登录 hub.weirdhost.xyz 并点击 "시간 추가" 按钮。
    """
    remember_web_cookie = os.environ.get('REMEMBER_WEB_COOKIE')
    pterodactyl_email = os.environ.get('PTERODACTYL_EMAIL')
    pterodactyl_password = os.environ.get('PTERODACTYL_PASSWORD')

    if not (remember_web_cookie or (pterodactyl_email and pterodactyl_password)):
        msg = "❌ 错误: 缺少登录凭据，请设置 REMEMBER_WEB_COOKIE 或 PTERODACTYL_EMAIL + PTERODACTYL_PASSWORD"
        print(msg)
        send_telegram_message(msg)
        return False

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_default_timeout(90000)

        try:
            # --- 尝试 Cookie 登录 ---
            if remember_web_cookie:
                session_cookie = {
                    'name': 'remember_web_59ba36addc2b2f9401580f014c7f58ea4e30989d',
                    'value': remember_web_cookie,
                    'domain': 'hub.weirdhost.xyz',
                    'path': '/',
                    'expires': int(time.time()) + 3600 * 24 * 365,
                    'httpOnly': True,
                    'secure': True,
                    'sameSite': 'Lax'
                }
                page.context.add_cookies([session_cookie])
                page.goto(server_url, wait_until="domcontentloaded", timeout=90000)
                page.screenshot(path="cookie_login.png")

                if "login" in page.url or "auth" in page.url:
                    print("Cookie 登录失败，改用邮箱密码。")
                    page.context.clear_cookies()
                    remember_web_cookie = None
                else:
                    print("Cookie 登录成功。")

            # --- 邮箱密码登录 ---
            if not remember_web_cookie:
                login_url = "https://hub.weirdhost.xyz/auth/login"
                page.goto(login_url, wait_until="domcontentloaded", timeout=90000)
                page.fill('input[name="username"]', pterodactyl_email)
                page.fill('input[name="password"]', pterodactyl_password)

                with page.expect_navigation(wait_until="domcontentloaded", timeout=60000):
                    page.click('button[type="submit"]')

                page.screenshot(path="login_result.png")

                if "login" in page.url or "auth" in page.url:
                    error_text = "登录失败"
                    if page.locator('.alert.alert-danger').count() > 0:
                        error_text = page.locator('.alert.alert-danger').inner_text().strip()
                    msg = f"❌ 邮箱密码登录失败: {error_text}"
                    print(msg)
                    send_telegram_message(msg, "login_result.png")
                    browser.close()
                    return False
                else:
                    print("邮箱密码登录成功。")

            # --- 确保进入服务器页面 ---
            if page.url != server_url:
                page.goto(server_url, wait_until="domcontentloaded", timeout=90000)

            # --- 点击按钮 ---
            add_button_selector = 'button:has-text("시간 추가")'
            add_button = page.locator(add_button_selector)
            add_button.wait_for(state='visible', timeout=30000)
            add_button.click()
            time.sleep(5)
            page.screenshot(path="add_button_clicked.png")

            msg = "✅ 成功点击 '시간 추가' 按钮"
            print(msg)
            send_telegram_message(msg, "add_button_clicked.png")
            browser.close()
            return True

        except Exception as e:
            page.screenshot(path="general_error.png")
            msg = f"⚠️ 发生异常: {e}"
            print(msg)
            send_telegram_message(msg, "general_error.png")
            browser.close()
            return False

if __name__ == "__main__":
    print("开始执行添加服务器时间任务...")
    success = add_server_time()
    if success:
        print("任务执行成功。")
        exit(0)
    else:
        print("任务执行失败。")
        exit(1)
