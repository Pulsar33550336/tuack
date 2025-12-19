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
  - **功能**: 自动搜索题目工程下的源代码文件，并将它们更新到配置文件的 `users` 字段中。
  - **技术细节**: 该命令会递归地扫描题目目录下的所有子目录（除了 `data`, `down`, `pre` 等特殊目录），并识别扩展名为 `.cpp`, `.c`, `.pas`, `.java`, `.py` 的文件。
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
  - **临时目录**: 评测时，会在项目根目录下创建一个 `tmp/` 临时目录。
  - **文件复制**: 源代码、输入文件（重命名为 `in`）、答案文件（重命名为 `ans`）会被复制到 `tmp/` 目录中。
  - **执行**: 在 `tmp/` 目录中编译和执行代码，程序的输出会被重定向到 `out` 文件。
  - **比对**: `out` 文件会与 `ans` 文件进行比对。如果存在 `chk.cpp`，则会先编译它，然后用它来比对 `in`, `out`, `ans` 文件。
  - **清理**: 每个测试点评测完毕后，`tmp/` 目录会被清空。

- **结果报告**:
  - **路径**: 评测结果会以 `.csv` 格式保存在 `result/` 目录下，并以题目的完整路径命名（如 `result/day1/problem-a.csv`）。
  - **内容**: 报告中包含每个程序在每个测试点上的得分、运行时间、评测状态（如 `ok`, `wa`, `tle`, `re`）等详细信息。
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
  - **表格**: 通过 `{{ tbl('table_name') }}` 语法调用。脚本会在题目工程的 `tables/` 目录下查找 `table_name.pyinc`, `table_name.json`, 或 `table_name.yaml` 文件，并使用对应的模板（如 `table.tex.jinja`）进行渲染。
  - **图片和资源**: 通过 `{{ img('image.png') }}` 语法调用。脚本会自动处理 `resources/` 目录下的图片等资源文件，并将其嵌入到输出文档中。
  - **代码片段**: 通过 `{{ down_file('example.cpp') }}` 语法调用。脚本会将题目工程 `down/` 目录下的文件内容直接渲染到题面中。

- **依赖工具**:
  - **`jinja2`**: 所有模板渲染的核心依赖。
  - **`pandoc`**: 用于 Markdown 与 LaTeX/HTML/DokuWiki 等格式之间的转换。
  - **`xelatex`**: 用于将 `.tex` 文件编译成 PDF。
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
  - **技术细节**:
    - **数据打包**: 会将 `data/` 目录下的测试数据、`chk/chk.cpp`（如果存在）、`data.yml` 配置文件（自动生成）打包成 `data.zip`。
    - **资源打包**: 会将 `resources/` 目录下的所有文件打包成 `resources.zip`。
    - **API 调用**: 通过 POST 请求将题面、配置信息、`data.zip` 和 `resources.zip` 上传到目标 OJ。
  - **配置**: 需要在 `~/.tuack/conf.json` 中配置对应平台的 `cookies` 等认证信息。

- **`tuoj-down`**:
  - **功能**: 仅导出适用于 TUOJ 的下发数据（样例）。
  - **技术细节**: 将 `down/` 目录下的所有 `.in` 和 `.ans` 文件复制到 `tuoj/down/<problem_route>/` 目录下。

## `load` 命令

`load` 命令用于从其他格式的工程或数据源导入题目信息到当前的 `tuack` 题目工程中。

### 用法

```bash
python -m tuack.load <format> <source_path>
```

### 支持的格式

- **`tsinsen-oj`**:
  - **功能**: 从清橙 OJ 的 `.txt` 格式文件导入题目。
  - **技术细节**:
    - **题面**: `Description` 字段内容会被提取并保存到 `statement/zh-cn.md`。
    - **数据**: `InData` 和 `OutData` 字段内容会被提取并依次保存为 `data/1.in`, `data/1.ans`, `data/2.in`, `data/2.ans`, ...
    - **标程/校验器**: `Solution` 和 `Judger` 字段内容会分别保存到 `tsinsen-oj/std/std.cpp` 和 `data/chk/chk.cpp`。
    - **配置**: 时空限制、标题等信息会被更新到 `conf.yaml` 中。
  - **用法**: `python -m tuack.load tsinsen-oj problem.txt`

- **`loj` / `ipuoj`**:
  - **功能**: 从 LibreOJ 或 IPU Online Judge 的题目页面 URL 导入题目。
  - **技术细节**:
    - **API**: 访问题目 URL 的 `/export` 接口获取 JSON 数据，并访问 `/testdata/download` 接口下载数据包。
    - **文件**: 题面被保存到 `statement/zh-cn.md`，数据包解压到 `data/` 目录，附加文件解压到 `down/` 目录。
    - **配置**: `conf.yaml` 会根据下载的 JSON 数据进行更新。
  - **用法**: `python -m tuack.load loj https://loj.ac/problem/1`

- **`data`**:
  - **功能**: 从一个包含数据文件的文件夹或压缩包中导入测试数据。
  - **子命令**:
    - `data-folder`: 强制指定源为文件夹。
    - `data-zip`: 强制指定源为 `.zip` 文件。
    - `data-tar`: 强制指定源为 `.tar` 文件。
    - `data-rar`: 强制指定源为 `.rar` 文件。
  - **技术细节**:
    - **匹配规则**: 脚本会递归扫描源目录，并尝试根据文件名匹配输入/输出文件对。它主要识别 `*input*`/`*output*` 和 `*.in`/`*.out` 或 `*.ans` 这样的模式。例如，`problem1.in` 会和 `problem1.ans` 配对。
    - **导入**: 成功配对的文件会被重命名并复制到当前题目的 `data/` 目录下，命名规则为 `1.in`, `1.ans`, `2.in`, `2.ans`, ...
  - **用法**: `python -m tuack.load data /path/to/data_folder`

## `doc` 命令

`doc` 命令用于处理和规范化题面文档。

### 用法

```bash
python -m tuack.doc <subcommand> [args...]
```

### 子命令

- **`load`**:
  - **功能**: 从一个外部文件（如 `.md`, `.html`）导入题面。
  - **技术细节**: 使用 `pandoc` 将输入文件转换为 Markdown，并覆盖 `statement/zh-cn.md` 文件。
  - **用法**: `python -m tuack.doc load statement.html`

- **`format`**:
  - **功能**: 对当前 `tuack` 工程中的题面文件（`statement/zh-cn.md`）进行格式化。
  - **技术细节**:
    - **标题转换**: 自动识别 Markdown 标题（如 `## 题目描述`），并将其转换为 `{{ s('description') }}` 格式的模板调用。
    - **样例分离**: 识别 `## 样例` 部分的内容，将其中的输入和输出代码块分别提取出来，并保存为 `down/1.in`, `down/1.ans`, `down/2.in`, ...
    - **图片下载**: 自动识别 Markdown 或 HTML 格式的图片链接，下载图片并保存到 `resources/` 目录，然后将链接替换为 `{{ img(...) }}` 模板调用。
  - **注意**: 这是一个有风险的操作，建议在执行前备份题面文件。

- **`check`**:
  - **功能**: 检查题面中的格式问题，如中英文之间缺少空格、使用全角标点等。
  - **技术细节**: 调用 `~/.tuack/format-linux` (或对应系统的可执行文件) 来进行检查。该检查器本身是用 `flex` 和 `bison` 实现的。
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
