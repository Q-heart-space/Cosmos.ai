# DSH 宿主适配包

本包按 manifest.json 安装到可覆盖的 DSH 配置根，安装器只使用 Python 标准库。MCP 薄代理与 common/ 下共享实现一同安装；运行代理前须由使用者配置 QDR_ROOT，指向其可用的 Q博士 服务或工作空间。

`hooks.json` 只是可选模板：所需治理脚本和兼容的 DSH hook 桥不随本包交付，安装文件不代表事件已通电。`qdr_wrapper.py` 也需另行提供 QDR_ROOT 下的命令脚本。专家预设模板的 persona 由用户自己的技能源提供。

`agents-anywhere/bridge/endpoint.json` 是运行期端点，包含会话令牌与进程信息，不随源码或公开包交付。安装后仍需分别验证真实 DSH 会话、MCP 调用及业务系统授权。
