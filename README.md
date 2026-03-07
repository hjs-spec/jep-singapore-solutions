# 🇸🇬 JEP Singapore Solutions

**将新加坡AI治理框架转化为可验证的代码**

## 📋 概述

本仓库提供判断事件协议（JEP）与新加坡三大AI治理框架的完整对照解决方案，帮助企业用最低的技术成本满足最高的监管标准。

### 🎯 覆盖的新加坡框架

| 框架 | 发布机构 | JEP解决方案 |
|------|----------|-------------|
| **Model AI Governance Framework for Agentic AI (2026)** | IMDA | [智能体AI问责实现 →](/framework-agentic) |
| **AI Verify Testing Framework** | IMDA | [AI Verify问责插件 →](/framework-ai-verify) |
| **AIM Toolkit (Competition & Consumer Protection)** | CCS + IMDA | [AIM Toolkit证据导出 →](/framework-aim-toolkit) |

## 🔍 为什么选择JEP？

✅ **新加坡本土**：由新加坡注册的非营利基金会（HJS Foundation LTD）管理  
✅ **密码学保障**：Ed25519签名确保证据不可抵赖、不可篡改  
✅ **轻量集成**：3行代码，<1ms性能影响  
✅ **开源免费**：Apache 2.0许可证，社区驱动  

## 🏢 新加坡行业用例

| 行业 | 监管机构 | 示例场景 | 解决方案 |
|------|----------|----------|----------|
| 金融 | MAS | DBS银行贷款审批AI | [查看 →](/framework-agentic/examples/financial-services.py) |
| 医疗 | MOH | 新加坡中央医院诊断AI | [查看 →](/framework-agentic/examples/healthcare.py) |
| 公共部门 | GovTech | CPF智能咨询助手 | [查看 →](/framework-agentic/examples/public-sector.py) |

## 🚀 快速开始

```bash
# 克隆仓库
git clone https://github.com/hjs-spec/jep-singapore-solutions
cd jep-singapore-solutions

# 安装JEP核心库
pip install jep-protocol

# 运行新加坡框架验证
python tests/verify-singapore-compliance.py
