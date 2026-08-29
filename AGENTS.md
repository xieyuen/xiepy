# AGENTS.md

## 目的

本文档为 Copilot CLI、会话代理及其他自动化助手提供本仓库的快速入门指南，涵盖构建、测试、打包、高层架构及特有约定。

---

## 构建 / 测试 / 代码检查

### 开发环境准备（与 CI 保持一致）

```bash
python -m pip install -U pip
pip install uv
uv sync
```

### 构建

```bash
uv build   # 生成 dist/ 下的分发包
```

### 测试

测试需要安装 `test` 可选依赖包, 请运行 `uv sync --extra test` 安装,
并请使用 ``uv run pytest`` 运行测试。

> **注意：** 如果已经 `uv tool install pytest`, 可以直接运行 `pytest`

- 运行全部测试：  
  `uv run pytest tests/`
- 运行单个测试文件：  
  `uv run pytest tests/test_file.py`
- 运行单个测试用例：  
  `uv run pytest tests/test_file.py::test_name`

### 代码检查

仓库使用 black 作为格式化工具.

---

## 高层架构

- **包路径：** `src/xiepy`
- **关键模块：**
  - `xiepy.common` – 共享工具（`constants.py`、`logger.py`、`exceptions.py`）
  - `xiepy.utils` – 工具集（其中 `mcversion.py` 实现复杂的版本解析与比较）
  - `xiepy.scripts` / `xiepy._scripts` – 独立脚本（如 `music_crawler.py`）
- **打包配置：** `pyproject.toml` 使用 `setuptools` 后端，通过 `setuptools.find` 指向 `src/`。
- **版本来源：** 打包时从 `src/xiepy/common/constants.py` 中读取 `VERSION_PYPI`。

---

## 仓库约定

- **版本管理：** 每次发布或打包前，需同步更新 `xiepy.common.constants` 中的 `VERSION` 与 `VERSION_PYPI`。
- **日志：** 使用 `get_logger(...)` 获取 logger。日志写入 `logs/xiepy.log`，旧日志会被归档（压缩并删除旧文件）。创建 logger 时会清理已有 handlers 以避免重复。
- **脚本依赖检查：** 脚本中通过 `try/except ModuleNotFoundError` 保护导入，并在缺少依赖时抛出 `xiepy.common.exceptions.DependencyNotInstalled`，错误信息中需包含 `pip` 安装提示。新增脚本请沿用此模式。
- **工作目录：** 脚本默认使用 `xiepy.common.constants.WORKING_DIRECTORY`（即 `Path.cwd()`）。
- **提交信息规范：** 本仓库要求采用**约定式提交（Conventional Commits）** 格式，例如：
  ```
  feat(scripts): 添加音乐爬虫新功能
  fix(logger): 修复日志轮转时的句柄泄漏
  ci(testpypi): 删除 testpypi.yml 中的 release 触发器
  docs: 更新 AGENTS.md 中文版本
  ```
  类型包括但不限于 `feat`、`fix`、`docs`、`style`、`refactor`、`perf`、`test`、`chore` 等，作用域（括号内）为可选的模块名，请尽量明确。

---

## CI 与发布流程

- **关键工作流：** `.github/workflows/build.yml`、`test.yml`、`pypi_publish.yml` 及 `testpypi.yml`。
- **CI 步骤概要：** CI 安装 `uv` → 执行 `uv sync` → 执行 `uv build`，构建产物上传为 `release-dists`，后续发布任务将使用这些产物。

---

## 给 AI / 自动化代理的建议

- 更改版本或打包相关代码时：**务必同步更新** `src/xiepy/common/constants.py` 中的 `VERSION_PYPI` 和 `VERSION`，然后执行 `uv build` 验证构建产物。
- 新增运行时依赖：需在 `pyproject.toml` 中添加依赖（或可选依赖），并确保对应的脚本包含依赖检查及友好的错误提示。
- 新增测试：请将测试步骤接入现有的 `test.yml`（该文件为 `workflow_call`），或在 `build.yml` 中增加测试步骤以便在 CI 中验证。
- 提交代码时：请严格遵循上述“提交信息规范”，使用约定式提交格式。
- 回复或询问用户时: 尽可能使用中文, 但注意保留英文术语

---

## 已检查的 AI 辅助配置文件

仓库中未发现 `CLAUDE.md`、`.cursorrules`、`.windsurfrules`、`CONVENTIONS.md` 等常见 AI 助手规则文件。
