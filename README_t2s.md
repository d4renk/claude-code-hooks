# 繁体转简体工具 (t2s.py)

Python 脚本用于将繁体中文转换为简体中文。

## 安装依赖

```bash
pip install opencc-python-reimplemented
```

## 使用方法

### 1. 从标准输入读取，输出到标准输出

```bash
echo "繁體中文測試" | python t2s.py
# 输出: 繁体中文测试
```

### 2. 转换单个文件

```bash
python t2s.py -i input.txt -o output.txt
```

### 3. 批量转换目录

```bash
# 转换所有 .txt 文件
python t2s.py --in-dir ./traditional --out-dir ./simplified

# 递归转换所有子目录
python t2s.py --in-dir ./traditional --out-dir ./simplified --recursive

# 转换指定扩展名的文件
python t2s.py --in-dir ./docs --out-dir ./docs_cn --ext .md --recursive
```

### 4. 指定编码

```bash
python t2s.py -i input.txt -o output.txt --encoding gbk
```

## 参数说明

- `-i, --input`: 输入文件路径（省略则从 stdin 读取）
- `-o, --output`: 输出文件路径（省略则输出到 stdout）
- `--in-dir`: 批量模式的输入目录
- `--out-dir`: 批量模式的输出目录
- `--encoding`: 文本编码（默认: utf-8）
- `--ext`: 批量模式的文件扩展名过滤（默认: .txt）
- `--recursive`: 递归处理子目录
- `--strict`: 批量模式遇到错误立即退出

## 注意事项

- 不支持原地转换（输入输出不能为同一文件）
- 批量模式使用 `--recursive` 时，输出目录不能在输入目录内
- 保持目录结构：批量转换会在输出目录中保持相同的相对路径结构
