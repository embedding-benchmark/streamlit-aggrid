# Streamlit Aggrid SDK with Custom Link Header Component

[English](#overview) | [中文](./README_ZH.md)

---

## Overview

This SDK extends the `st-aggrid` library with a custom link header component that allows you to add clickable link icons to column headers. The component preserves all default `ag-grid` functionality including sorting, filtering, and resizing.

## Features

- 🔗 **Custom Link Headers**: Add clickable link icons to column headers
- 📊 **Full Grid Functionality**: Maintains sorting, filtering, and resizing capabilities
- 🎯 **Event Isolation**: Clicking the link icon doesn't interfere with sorting/filtering
- 📏 **Auto-Width Adjustment**: Automatically adjusts column width to fit header text
- 🛠️ **Easy Integration**: Simple API for creating link-enabled columns
- 🔧 **Enhanced Error Handling**: Robust error handling with multiple fallback strategies
- 📦 **Cross-Platform**: Supports Windows, Linux, and macOS environments
- ⚡ **Fast Build System**: Simplified, single-command build process

## Building the SDK

### Prerequisites

- **Python 3.8+** (required)
- **Node.js 14+** (optional, for frontend building)
- **npm** or **yarn** (auto-detected if available)

### Quick Build

```bash
# Complete build (frontend + Python package)
python build_sdk.py

# Python package only (skip frontend)
python build_sdk.py --skip-frontend

# View all options
python build_sdk.py --help
```

### Build Options

| Option            | Description                    | Example                               |
| ----------------- | ------------------------------ | ------------------------------------- |
| `--skip-frontend` | Skip frontend build            | `python build_sdk.py --skip-frontend` |
| `--skip-python`   | Skip Python package build      | `python build_sdk.py --skip-python`   |
| `--strict`        | Stop on frontend build failure | `python build_sdk.py --strict`        |
| `--help`, `-h`    | Show help message              | `python build_sdk.py --help`          |

### What the Script Does

1. **Environment Check**: Detects Python version and Node.js availability
2. **Frontend Build**: If Node.js is available, automatically runs:
   - `npm install` or `yarn install` (auto-detects based on lock files)
   - `npm run build` or `yarn build`
3. **Python Package Build**: Creates wheel and source distribution using:
   - PEP 517 build system (preferred)
   - Falls back to `setup.py` if needed

### Build Output

After successful build, you'll find in `dist/`:

- `streamlit_aggrid-<version>-py3-none-any.whl`
- `streamlit_aggrid-<version>.tar.gz`

### Build Examples

```bash
# Standard build (recommended)
python build_sdk.py
# Output:
# 🚀 Streamlit AgGrid SDK 快速构建
# ✅ Python: 3.9.7
# 📦 Node.js: v18.17.0
# 🔧 使用 npm 构建前端...
# ✅ 前端构建完成
# ✅ Python包构建完成 (PEP 517)
# 🎉 构建完成! 生成了 1 个文件:
#   📦 streamlit_aggrid-1.1.7-py3-none-any.whl

# If Node.js is not available
python build_sdk.py
# Output:
# ✅ Python: 3.9.7
# ⚠️ Node.js不可用，跳过前端构建
# ✅ Python包构建完成 (PEP 517)

# Python package only
python build_sdk.py --skip-frontend
# Output:
# ✅ Python: 3.9.7
# ⏭️ 跳过前端构建
# ✅ Python包构建完成 (PEP 517)
```

## Installation

```bash
# Install from local wheel file
pip install dist/*.whl
```

## Quick Start

```python
import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.link_header_builder import create_link_column

# Sample data
data = {
    'name': ['Alice', 'Bob', 'Charlie'],
    'email': ['alice@example.com', 'bob@example.com', 'charlie@example.com'],
    'github': ['alice-github', 'bob-github', 'charlie-github'],
    'age': [25, 30, 35]
}
df = pd.DataFrame(data)

# Create link columns
email_column = create_link_column(
    field='email',
    header_name='Email',
    url='mailto:{email}',
    sortable=True,
    filter=True
)

github_column = create_link_column(
    field='github',
    header_name='GitHub',
    url='https://github.com/{github}',
    sortable=True,
    filter=True
)

# Build grid options
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column('name', sortable=True, filter=True)
gb.configure_column('age', sortable=True, filter=True)

# Add link columns to grid options
grid_options = gb.build()
grid_options['columnDefs'].append(email_column)
grid_options['columnDefs'].append(github_column)

# Display the grid
grid_response = AgGrid(
    df,
    gridOptions=grid_options,
    data_return_mode='AS_INPUT',
    update_mode='MODEL_CHANGED',
    fit_columns_on_grid_load=True,
    theme='streamlit'
)
```

## API Reference

### `create_link_column(field, header_name, url, **kwargs)`

Creates a column definition with a custom link header.

**Parameters:**

- `field` (str): Data field name
- `header_name` (str): Column header name
- `url` (str): URL template for the link (supports {field} placeholder)
- `**kwargs`: Additional column configuration options

**Returns:**

- `dict`: Column definition dictionary

### `create_link_columns(link_config, **default_kwargs)`

Creates multiple link columns from a configuration dictionary.

**Parameters:**

- `link_config` (dict): Dictionary mapping field names to URLs
- `**default_kwargs`: Default configuration for all columns

**Returns:**

- `dict`: Dictionary of column definitions

### `add_link_headers_to_grid_options(grid_options, link_config, **default_kwargs)`

Adds link column configurations to existing grid options.

**Parameters:**

- `grid_options` (dict): Existing grid options
- `link_config` (dict): Dictionary mapping field names to URLs
- `**default_kwargs`: Default configuration for all columns

**Returns:**

- `dict`: Updated grid options

## Advanced Usage

### Batch Column Creation

```python
# Define link configurations
link_config = {
    'email': 'mailto:{email}',
    'website': 'https://{website}',
    'github': 'https://github.com/{github}'
}

# Create all link columns at once
link_columns = create_link_columns(link_config, sortable=True, filter=True)

# Add to grid options
for column_def in link_columns.values():
    grid_options['columnDefs'].append(column_def)
```

### Dynamic URL Generation

```python
# URL with dynamic field substitution
email_column = create_link_column(
    field='email',
    header_name='Contact',
    url='mailto:{email}?subject=Hello from {name}',
    sortable=True,
    filter=True
)
```

## Configuration Options

All standard `ag-grid` column options are supported:

- `sortable`: Enable/disable sorting
- `filter`: Enable/disable filtering
- `resizable`: Enable/disable column resizing
- `suppressHeaderContextMenu`: Show/hide header context menu
- `width`: Set column width
- `minWidth`: Set minimum column width
- `maxWidth`: Set maximum column width

## Examples

See `test_streamlit_app.py` for a complete working example.

## Troubleshooting

### Build Issues

**Issue**: Frontend build fails

- Try building Python package only: `python build_sdk.py --skip-frontend`
- Check if Node.js is properly installed: `node --version`
- Verify npm/yarn is available: `npm --version` or `yarn --version`

**Issue**: "Package not found" errors

- Ensure you're in the correct project directory
- Check if `pyproject.toml` or `setup.py` exists

### Component Issues

**Issue**: Link icons not showing

- Check if `create_link_column` function is imported correctly
- Verify column definitions are properly added to `grid_options['columnDefs']`
- Ensure the frontend build was successful and includes the latest components

**Issue**: Sorting/filtering functionality lost

- Ensure `sortable=True` and `filter=True` are set in `create_link_column`
- Check if `headerComponentParams` structure is used correctly

**Issue**: Column width too narrow, text wrapping

- The component now automatically adjusts column width to fit text
- If issues persist, manually set `minWidth` in column configuration:
  ```python
  column = create_link_column(
      field='email',
      header_name='Email Address',
      url='mailto:{email}',
      minWidth=150  # Set minimum width
  )
  ```

**Issue**: Clicking links not responding

- Verify URL format is correct
- Check browser console for JavaScript errors
- Ensure URLs use proper format with field placeholders: `https://example.com/{field}`

## Notes

1. **URL Templates**: URLs support `{field}` placeholders that get replaced with actual data
2. **Event Handling**: Clicking the 🔗 icon prevents event bubbling and won't trigger sorting
3. **Auto-Width**: Component automatically adjusts column width to prevent text wrapping
4. **Styling**: Link icons use default colors and maintain consistency with header text
5. **Build System**: Fast, single-command build with automatic Node.js detection
6. **Error Recovery**: Multiple fallback strategies ensure reliable package generation
7. **Compatibility**: Fully compatible with all `ag-grid` functionality and modern browsers

## Recent Updates (v1.1.7)

- ✅ **Fixed LinkHeaderComponent Implementation**: Resolved text wrapping issues in column headers
- ✅ **Enhanced Auto-Width Logic**: Improved column width calculation and adjustment
- ✅ **Simplified Build System**: Streamlined build process with better error handling
- ✅ **Cross-Platform Support**: Improved Windows compatibility for build scripts
- ✅ **Better Error Recovery**: Multiple fallback strategies for package building
