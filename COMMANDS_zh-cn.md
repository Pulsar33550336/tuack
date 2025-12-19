# tuack 命令文档

本文档详细介绍了 `tuack` 工具的所有可用命令和特性，旨在为项目重构提供清晰的参考。

## `gen` 命令

`gen` 命令用于生成新的项目结构（如比赛、比赛日、题目）以及管理和更新配置文件。

### 用法

```bash
python -m tuack.gen <subcommand> [args...]
```

### 子命令

#### 项目生成

- **`contest` (或 `n`)**
  - **功能**: 在当前目录下生成一个新的比赛（contest）工程。
  - **用法**: `python -m tuack.gen contest`

- **`day` (或 `d`)**
  - **功能**: 在比赛工程目录下生成一个新的比赛日（day）工程。可以一次生成多个。
  - **用法**: `python -m tuack.gen day day1 day2`

- **`problem` (或 `p`)**
  - **功能**: 在比赛日工程目录下生成一个新的题目（problem）工程。可以一次生成多个。
  - **用法**: `python -m tuack.gen problem problem-a problem-b`

- **`empty` (或 `e`)**
  - **功能**: 生成一个不包含示例文件的空题目工程，适用于题目结构简单或自定义需求较高的场景。
  - **用法**: `python -m tuack.gen empty my-empty-problem`

#### 配置文件更新

- **`data` (或 `t`)**
  - **功能**: 自动搜索题目工程下 `data/` 目录中的 `.in` 和 `.ans` 文件，并将它们作为测试数据更新到配置文件中。
  - **用法**: `python -m tuack.gen data`

- **`samples` (或 `s`)**
  - **功能**: 自动搜索题目工程下 `down/` 目录中的 `.in` 和 `.ans` 文件，并将它们作为样例数据更新到配置文件中。
  - **用法**: `python -m tuack.gen samples`

- **`pre`**
  - **功能**: 自动搜索题目工程下 `pre/` 目录中的 `.in` 和 `.ans` 文件，并将它们作为预测试数据更新到配置文件中。
  - **用法**: `python -m tuack.gen pre`

- **`code` (或 `c`)**
  - **功能**: 自动搜索题目工程下的源代码文件（如 `.cpp`, `.c`, `.py`），并将它们更新到配置文件的 `users` 字段中。
  - **用法**: `python -m tuack.gen code`

- **`auto` (或 `a`)**
  - **功能**: 自动执行 `data`, `samples`, `pre`, `code` 四个子命令，一次性更新所有相关配置。
  - **用法**: `python -m tuack.gen auto`

#### 工程配置与工具

- **`lfs`**
  - **功能**: 为题目工程添加 `git-lfs` 支持，用于管理大型数据文件。
  - **用法**: `python -m tuack.gen lfs`

- **`chk`**
  - **功能**: 在题目工程的 `data/chk/` 目录下添加一个答案校验器（special judge）的模板文件 `chk.cpp`。
  - **用法**: `python -m tuack.gen chk`

- **`prec`**
  - **功能**: 为比赛工程添加考生须知文件。
  - **用法**: `python -m tuack.gen prec`

- **`upgrade` (或 `u`)**
  - **功能**: 将旧版 `tuack` 工程的配置文件和目录结构升级到当前版本。
  - **用法**: `python -m tuack.gen upgrade`

#### 批量修改配置

- **`title` (或 `l`)**
  - **功能**: 批量设置比赛日或题目的标题。
  - **用法**: `python -m tuack.gen title "第一天" "第二天"`

- **`time` (或 `i`)**
  - **功能**: 批量设置题目的时间限制（单位：秒）。
  - **用法**: `python -m tuack.gen time 1.0 2.0`

- **`memory` (或 `m`)**
  - **功能**: 批量设置题目的内存限制（单位：MB）。
  - **用法**: `python -m tuack.gen memory 256 512`

- **`length` (或 `g`)**
  - **功能**: 批量设置比赛日的时长（单位：小时）。
  - **用法**: `python -m tuack.gen length 5.0 4.5`

- **`conf` (或 `f`)**
  - **功能**: 批量设置任意配置字段。第一个参数为字段名（支持 JSON 格式表示层级），后续参数为对应的值（也为 JSON 格式）。
  - **用法**:
    ```bash
    # 设置 file io 为 true
    python -m tuack.gen conf '"file io"' true true
    # 设置 C++ 编译选项
    python -m tuack.gen conf '["compile","cpp"]' '"-O2 -std=c++14"'
    ```

## `test` 命令

`test` 命令用于对题目进行评测。它会编译指定的用户代码，并使用配置文件中定义的测试数据（`data`）、样例数据（`samples`）和预测试数据（`pre`）来运行和验证代码的正确性。

### 用法

```bash
python -m tuack.test [options] [problem_path...]
```

### 功能特性

- **代码编译**:
  - 自动根据配置文件中的 `compile` 字段找到对应的编译器（如 `g++`, `gcc`, `fpc`）和编译选项来编译源代码。
  - 如果编译失败，会在 `compile.log` 文件中记录详细的错误信息。

- **多平台支持**:
  - 支持在 `Linux`, `Windows`, `macOS` 等不同操作系统上运行。
  - 会根据当前系统选择合适的沙箱和计时方式来限制程序运行。

- **资源限制**:
  - **时间限制**: 严格限制程序的运行时间，超时则会被终止。
  - **内存限制**: 在 `Linux` 和 `macOS` 上，会限制程序使用的最大内存，超限会导致运行时错误（Runtime Error）。Windows 平台暂不支持内存限制。

- **评测流程**:
  - 依次运行所有测试点（包括测试数据、样例数据和预测试数据）。
  - 对于每个测试点，将程序的输出与标准答案文件（`.ans`）进行比对。
  - 支持使用自定义校验器（`chk.cpp`）进行评测。

- **结果报告**:
  - 评测结果会以 `.csv` 格式保存在 `result/` 目录下。
  - 报告中包含每个程序在每个测试点上的得分、运行时间、评测状态（如 `ok`, `wa`, `tle`, `re`）等详细信息。
  - 如果配置了期望得分（`expected`），当实际得分与期望不符时，会在日志中给出错误提示。

- **打包评测（Packed Scoring）**:
  - 支持子任务（subtask）模式。配置文件中的 `data` 字段可以定义数据包，每个包可以包含多个测试点并被赋予一个总分。
  - 只有当一个包内的所有测试点都通过时，才能获得该包的分数。

## `ren` 命令

`ren` 命令（render）用于将题目或整场比赛的题面渲染成不同格式的文档。它使用 `Jinja2` 模板引擎，支持高度定制化的输出。

### 用法

```bash
python -m tuack.ren <format> [options]
```

### 支持的格式

- **`tex`**: 渲染成 LaTeX 格式，最终编译为 PDF 文档。支持多种竞赛风格：
  - `noi`: NOI 系列竞赛风格。
  - `ccpc`: CCPC 系列竞赛风格。
  - `tupc`: THU Programming Contest 风格。
  - `tuoi`: THU OI Contest 风格。
  - `hand`: 手写作业风格。

- **`md`**: 渲染成 Markdown 格式。支持多种 OJ 平台：
  - `uoj`: Universal Online Judge 风格。
  - `tuoj`: THU Online Judge 风格。
  - `loj`: LibreOJ 风格。
  - `ipuoj`: IPU Online Judge 风格。

- **`html`**: 渲染成 HTML 格式。
  - `tsinsen-oj`: 清橙 OJ 风格。

- **`doku`**: 渲染成 DokuWiki 格式。
  - `thuoj`: THU Online Judge (DokuWiki) 风格。

- **复合格式**:
  - `ccc-tex` / `ccc-md`: 加拿大计算机竞赛（CCC）的 LaTeX 和 Markdown 风格。
  - `tuoj-pc` / `tuoj-oi`: 结合了 `tupc` / `tuoi` 与 `tuoj` 的风格。

### 功能特性

- **模板驱动**:
  - 所有输出格式都由 `templates/` 目录下的 `Jinja2` 模板定义。
  - 支持通过修改模板或添加新模板来扩展和定制输出样式。

- **多语言支持**:
  - 支持国际化（i18n），可以根据需要生成不同语言的题面（如中文 `zh-cn`、英文 `en`）。

- **动态内容生成**:
  - **表格**: 支持从 `.py`, `.json`, `.yaml` 文件中读取数据并动态渲染成表格。
  - **图片和资源**: 自动处理 `resources/` 目录下的图片等资源文件，并将其嵌入到输出文档中。
  - **代码片段**: 可以将 `down/` 目录下的文件内容直接渲染到题面中，方便展示样例代码或数据。

- **依赖工具**:
  - 渲染 `tex` 格式需要安装 `xelatex` 和 `pandoc`。
  - 渲染 `html` 和 `doku` 格式需要安装 `pandoc`。
  - 所有模板渲染都需要安装 `jinja2`。

## `dump` 命令

`dump` 命令用于将 `tuack` 工程导出为其他评测系统或 OJ 平台支持的格式。

### 用法

```bash
python -m tuack.dump <format>
```

### 支持的格式

- **`lemon`**:
  - **功能**: 导出为 [Lemon](https://github.com/SPOJ/lemon) 评测系统兼容的格式。
  - **输出**: 生成包含 `*.cdf` 配置文件和 `data/` 目录的文件夹结构。
  - **注意**: 需要 `PySide` 库（Python 2）或 `json` 库（Python 3）来生成 `.cdf` 文件。

- **`arbiter`**:
  - **功能**: 导出为 [Arbiter](https://github.com/MikeMirzayanov/Arbiter) 评测系统兼容的格式。
  - **子命令**:
    - `arbiter-main`: 仅导出评测所需的主数据和配置文件。
    - `arbiter-down`: 仅导出供选手下载的样例数据。
  - **输出**: 生成 `arbiter/` 目录，包含 `main/` 和 `down/` 子目录，符合 Arbiter 的工程结构。

- **`tsinsen-oj`**:
  - **功能**: 导出为清橙 OJ 的“我来出题”格式。
  - **输出**: 生成一个 `.txt` 文件，包含了题面、数据、标程等所有信息，可以直接上传到清橙 OJ。

- **`loj` / `ipuoj`**:
  - **功能**: 将题目直接上传或更新到 [LibreOJ](https://loj.ac) 或 IPU Online Judge 平台。
  - **实现**: 通过模拟浏览器请求，自动填充题面、配置时空限制、上传数据和资源文件。
  - **配置**: 需要在 `conf.json` 中配置对应平台的 `cookies` 等认证信息。

- **`tuoj-down`**:
  - **功能**: 仅导出适用于 TUOJ 的下发数据（样例）。
  - **输出**: 生成 `tuoj/down/` 目录，包含每个题目的样例输入和输出文件。

## `load` 命令

`load` 命令用于从其他格式的工程或数据源导入题目信息到当前的 `tuack` 题目工程中。

### 用法

```bash
python -m tuack.load <format> <source_path>
```

### 支持的格式

- **`tsinsen-oj`**:
  - **功能**: 从清橙 OJ 的 `.txt` 格式文件导入题目。
  - **实现**: 解析 `.txt` 文件中的各个字段（如题面、时空限制、数据、标程），并将其转换为 `tuack` 的配置和文件结构。
  - **用法**: `python -m tuack.load tsinsen-oj problem.txt`

- **`loj` / `ipuoj`**:
  - **功能**: 从 LibreOJ 或 IPU Online Judge 的题目页面 URL 导入题目。
  - **实现**: 访问题目 URL 的 `/export` 接口，下载 JSON 格式的题目数据，并自动导入题面、时空限制、数据等。
  - **用法**: `python -m tuack.load loj https://loj.ac/problem/1`

- **`data`**:
  - **功能**: 从一个包含数据文件的文件夹或压缩包中导入测试数据。
  - **子命令**:
    - `data-folder`: 强制指定源为文件夹。
    - `data-zip`: 强制指定源为 `.zip` 文件。
    - `data-tar`: 强制指定源为 `.tar` 文件。
    - `data-rar`: 强制指定源为 `.rar` 文件。
  - **实现**: 自动识别输入（`.in`, `input`）和输出（`.ans`, `.out`）文件对，并将其复制到当前题目的 `data/` 目录下，然后更新配置文件。
  - **用法**: `python -m tuack.load data /path/to/data_folder`

## `doc` 命令

`doc` 命令用于处理和规范化题面文档。

### 用法

```bash
python -m tuack.doc <subcommand> [args...]
```

### 子命令

- **`load`**:
  - **功能**: 从一个外部文件（如 `.md`, `.html`）导入题面。它会使用 `pandoc` 将输入文件转换为 `tuack` 标准的 Markdown 格式。
  - **用法**: `python -m tuack.doc load statement.html`

- **`format`**:
  - **功能**: 对当前 `tuack` 工程中的题面文件（`statement/zh-cn.md`）进行格式化。
  - **实现**: 自动识别题面中的标题（如“题目描述”、“输入格式”），并将其转换为 `{{ s('title') }}` 格式的模板调用。同时，它还能解析样例数据，并将其分离到 `down/` 目录下。
  - **注意**: 这是一个有风险的操作，建议在执行前备份题面文件。

- **`check`**:
  - **功能**: 检查题面中的格式问题，如中英文之间缺少空格、使用全角标点等。
  - **实现**: 依赖一个名为 `format` 的可执行文件（通过 `tuack.install format` 安装）来进行检查。
  - **输出**: 在控制台输出详细的格式问题报告，包括行号、列号和问题描述。

## `install` 命令

`install` 命令用于安装 `tuack` 的附加组件和依赖工具。

### 用法

```bash
python -m tuack.install <component>
```

### 支持的组件

- **`format`**:
  - **功能**: 安装题面格式检查器。这是一个使用 `flex` 和 `bison` 编译的 C++ 程序，用于 `doc check` 命令。
  - **实现**: 脚本会尝试从 `tuack/lex/` 目录中找到预编译好的可执行文件并复制到 `~/.tuack/` 目录下。如果失败，会提示用户手动编译。

- **`std`**:
  - **功能**: 标准安装，安装所有常用的小型工具（目前仅包含 `format`）。

- **`full`**:
  - **功能**: 完整安装，未来可能包含更多大型工具。
