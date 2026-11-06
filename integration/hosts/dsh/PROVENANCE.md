# DSH 公开适配包来源与边界

- 权威源：`host-adapters` 分支 `2cea924aa` 的 `dsh/bootstrap/manifest.json`。
- 源清单 SHA-256：`a26fd98fce778d6f26cc7342801c39d8f7474b5a7d84740b4ad0a9418dd54e7c`；公开包列 10 件，逐项记录源与公开载荷摘要。
- 公开派生：README、hooks 说明、wrapper 历史机器路径注释、专家元数据说明、desktop 模板注释做语义脱敏；其它载荷按源字节复制。
- 运行态 `agents-anywhere/bridge/endpoint.json` 不在源清单和公开包内。
- 安装器仅负责清单核验与落位；MCP 实际调用依赖用户配置的 `QDR_ROOT`，hooks 还依赖兼容的 DSH 桥；本包不声称真实会话或业务系统已通电。

| 路径 | 源 SHA-256 | 公开 SHA-256 |
|:--|:--|:--|
| `hooks.json` | `66d47272de7077987787f8df911c10e42410b3c3b822ca76e8dec18dfb27b58c` | `8d41de8113671d60d702236d74e4df525d8fe034f15b507b75f9bfa2fd5c7827` |
| `qdr_mcp_proxy.py` | `b09fe116309416aca0d75db94de9b40ee4a3fd2c1836c1a8a3342578d4187951` | `b09fe116309416aca0d75db94de9b40ee4a3fd2c1836c1a8a3342578d4187951` |
| `qdr_wrapper.py` | `8650395a0a8de738caf9d62cedfaed264c9b13f27f8ad4a9bd879dfd9c66e920` | `0715aee8dd177ca6724c6480886e76f4f18d6ae1e10df6e96c32f40251991bec` |
| `README.md` | `6af944c13e8965a122951dc1bf0239fccc5bf99a51c34ac82876adcb69dcf282` | `90a343ed4b909f2ba1834a8a56e62fc1b8af6dedb25fbd74a939e93c99e6d53f` |
| `experts/_template/agent_dir/agent.cordis.yml` | `f256221acb7495bdcdfca1389374a92a9207b19cf535174e72a9a43ed5b8bab4` | `f256221acb7495bdcdfca1389374a92a9207b19cf535174e72a9a43ed5b8bab4` |
| `experts/_template/agent_preset_row.yml` | `4b17de2fef03cc00b6593365eee18ae2cb8a2cf6b2485529d188855af166a627` | `4b17de2fef03cc00b6593365eee18ae2cb8a2cf6b2485529d188855af166a627` |
| `experts/_template/README.md` | `bb2a5f814e4c99d859aa036770464d8b78e4fb07a4eb2956c07e52df7e26c98e` | `bb2a5f814e4c99d859aa036770464d8b78e4fb07a4eb2956c07e52df7e26c98e` |
| `experts/expert_lib.meta.json` | `5cb3e03c6a680e93fbb970636ca5fe7303c62e9078bca323bb259276358e3759` | `2172db5bed30aacae8abb67ade8f767aaadabc7ad99810ef6751aeab96bf85a2` |
| `profiles/desktop/cordis.patch.yml` | `54526a4f4b40444c1da63fef3ae1d356d0562ad0c2f13ee62be1373d74a26376` | `ca95692cc2db1b4c2bf60fddd09193c512bd0d28f46bb6fcf193448bcd888467` |
| `common/qdr_mcp_host_proxy.py` | `c6bcb989782dc15ee84a8264c5807b44af5e899e689670e9f91f9547dcf9b8e8` | `c6bcb989782dc15ee84a8264c5807b44af5e899e689670e9f91f9547dcf9b8e8` |
