# weirdhost-4--login
老王韩国游戏机自动续期
使用 Cookie 登录
在 Run Time Adder Script 步骤中，已经定义了一个环境变量 REMEMBER_WEB_COOKIE，它可能是用来进行登录的 cookie。通常，这种方式适用于：
保持会话：你不需要每次登录，只需提供有效的 cookie，就可以直接访问需要的资源。
避免频繁登录：适用于需要长期保持登录状态的任务。
如何获取和使用 Cookie：
登录目标网站（如 Pterodactyl）。
使用 浏览器开发者工具（按 F12 或右键点击页面选择“检查”）：
找到 Application 标签，左侧有一个 Cookies 部分。
在 Cookies 部分找到与登录相关的 cookie（如 session, auth_token 等）。
复制这些值。
在 GitHub 项目的 Secrets 中添加一个新的 secret，名称为 REMEMBER_WEB_COOKIE，然后将复制的 cookie 值粘贴进去。
使用 Cookie 的好处：
每次工作流运行时会自动使用该 cookie 进行登录，无需再次输入账号密码。
使用 邮箱和密码 登录
如果没有有效的 cookie 或希望使用邮箱和密码进行登录，你已经在 Run Time Adder Script 步骤中定义了环境变量：
PTERODACTYL_EMAIL
PTERODACTYL_PASSWORD
如何在 GitHub Secrets 中设置：
在 GitHub 仓库页面中，进入 Settings > Secrets and variables > Actions。
点击 New repository secret。
添加以下两个 Secrets：
PTERODACTYL_EMAIL：你的 Pterodactyl 账户邮箱。
PTERODACTYL_PASSWORD：你的 Pterodactyl 账户密码。
通过这两个变量，工作流会在执行时用这些信息进行登录。
