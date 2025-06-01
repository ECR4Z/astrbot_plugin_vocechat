# VoceChat Adapter Plugin for AstrBot

**版本:** 1.0.0
**作者:** HikariFroya
**描述:** 一款为 AstrBot 设计的平台适配器插件，用于连接和集成 VoceChat 聊天服务。VoceChat是一个支持多平台、搭建简单的快捷聊天平台。

---

## ⚠️ 重要前置条件

为了成功使用此插件，**您必须首先拥有一个正在运行的 VoceChat 服务器实例，并且您的服务器上需要安装 Docker 来部署 VoceChat。**

### 1. 关于 VoceChat

VoceChat 是一款支持独立部署的个人云社交媒体聊天服务。它具有以下特点：
*   **独立部署**: 可以在您自己的服务器上搭建，数据完全由用户自己掌握。
*   **轻量级**: 约 15MB 的大小可部署在任何的服务器上。
*   **部署简单**: 很少需要维护。
*   **可内嵌**: 前端可以内嵌到自己的网站下。
*   **安全**: 传输过程加密。
*   **多平台支持**: 包括常见的 Windows, macOS, Linux, Android, iOS，此外还可以直接从网页端进行访问。

**官方网站及更多信息:** [https://voce.chat/zh-CN](https://voce.chat/zh-CN)

### 2. 安装 Docker

VoceChat 的推荐部署方式是使用 Docker。如果您的服务器上尚未安装 Docker，请根据您的操作系统参考以下官方文档进行安装：

*   **Windows (Docker Desktop):** [https://docs.docker.com/desktop/setup/install/windows-install/](https://docs.docker.com/desktop/setup/install/windows-install/)
*   **Linux (获取 Docker 引擎):** [https://docs.docker.com/get-started/get-docker/](https://docs.docker.com/get-started/get-docker/) (此链接通常会引导你选择适合的Linux发行版安装指南)
    *   对于常见的 Linux 发行版，如 Ubuntu, Debian, CentOS 等，都有详细的安装步骤。

### 3. 部署 VoceChat 服务器

请参照 VoceChat 官方文档中关于 Docker 部署的指南来搭建和运行您的 VoceChat 服务器。
*   **VoceChat Docker 部署指南 (通常在其官方文档或GitHub仓库中可以找到):** 确保遵循官方最新的部署步骤。

**在继续安装和配置本插件之前，请确保您的 VoceChat 服务器已成功部署并可以正常访问。**

---

## ✨ 插件功能特性

*   **连接 VoceChat**: 允许 AstrBot 连接到一个或多个 VoceChat 机器人账号。
*   **接收消息**: 通过 Webhook 接收来自 VoceChat 的私聊和频道消息。
*   **发送消息**: 支持向 VoceChat 用户（私聊）和频道（群聊）发送文本、Markdown 和图片消息。
*   **用户昵称获取**: 可配置是否通过 VoceChat API 获取用户的昵称，以提供更友好的显示。
*   **图片处理**:
    *   接收 VoceChat 中的图片消息，并将其转换为 Base64 编码的图片数据，供其他插件（如 LLM 插件）使用。
    *   支持发送 Base64 编码的图片或通过 Markdown 格式发送图片URL。
*   **新用户事件处理**: 可接收 VoceChat `newuser` 事件，方便进行欢迎等自动化操作。
*   **灵活配置**: 支持通过 AstrBot WebUI 或配置文件进行详细设置。

---

## ⚙️ 安装与配置

### 1. 安装插件

*   将 `astrbot_plugin_vocechat` 文件夹放置到 AstrBot 的 `data/plugins/` 目录下。
*   重启 AstrBot。

### 2. 配置插件实例

您需要在 AstrBot 的 "平台设置" 界面为每一个您想连接的 VoceChat 机器人账号**创建一个新的平台实例**，并选择本 "VoceChat 适配器"。

对于每个 VoceChat 平台实例，需要配置以下主要参数：

*   **`机器人名称(id)` (必填)**: 为这个平台实例在 AstrBot 中起一个唯一的ID，例如 `MyVoceBot1`, `GoldshipVoce`。这个ID会被其他插件（如 `RelayChatPlugin`）用来引用这个特定的Bot连接。
*   **`vocechat_server_url` (必填)**: 您的 VoceChat 服务器的完整 URL 地址。例如: `http://localhost:3009` 或 `https://your.vocechat.domain`。请确保末尾没有 `/`。
*   **`api_key` (必填)**: 您在 VoceChat 后台为该机器人账号生成的 API Key。请参考上面 VoceChat 文档截图中的“初始化一个 API Key”部分。
*   **`webhook_path` (建议保留默认或自定义)**: AstrBot 用于接收 VoceChat 推送消息的 Webhook 路径。例如: `/vocechat_webhook`。您需要在 VoceChat 机器人设置中填写的 Webhook URL 将是 `http://<你的AstrBot可访问地址>:<webhook_port><webhook_path>`。
*   **`webhook_listen_host` (通常为 `0.0.0.0`)**: AstrBot Webhook 服务器监听的IP地址。`0.0.0.0` 表示监听所有可用的网络接口。
*   **`webhook_port` (必填)**: AstrBot Webhook 服务器监听的端口号。例如: `8080`。请确保此端口未被其他应用占用，并且如果您的 AstrBot 服务器在防火墙后，此端口需要被允许访问。
*   **`get_user_nickname_from_api` (布尔值, 默认: `true`)**: 是否尝试通过 VoceChat API 获取用户昵称。如果为 `false`，将使用 `VoceChatUser_UID` 作为默认昵称。
*   **`send_plain_as_markdown` (布尔值, 默认: `false`)**: 如果为 `true`，发送纯文本消息时会使用 Markdown 格式（可能会影响部分纯文本的显示，但能更好地支持一些特殊字符）。通常建议保持 `false`，除非有特定需求。
*   **`default_bot_self_uid` (必填)**: 您要连接的这个VoceChat机器人账号在VoceChat中的用户ID (UID)。

**配置示例 (通常在 `data/config/vocechat_adapter_你的实例名.json` 中生成):**
```json
{
  "id": "MyVoceBot1", // 与平台设置中的 "机器人名称(id)" 一致
  "vocechat_server_url": "http://192.168.1.100:3009",
  "api_key": "your_bot_api_key_here_for_MyVoceBot1",
  "webhook_path": "/myvocebot1_hook",
  "webhook_listen_host": "0.0.0.0",
  "webhook_port": 8081, // 如果有多个实例，端口不能冲突
  "get_user_nickname_from_api": true,
  "send_plain_as_markdown": false,
  "default_bot_self_uid": "15" // MyVoceBot1 在 VoceChat 中的 UID
}
