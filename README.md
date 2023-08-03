# pypi-template

> pypi 开发模板

------

## 运行环境

![](https://img.shields.io/badge/Python-3.8%2B-brightgreen.svg)


## 使用说明

1. 创建 Github Repository 时选择这个仓库做模板
2. 在 [PyPI](https://pypi.org/) 上注册一个帐号，然后生成 API Token 后，把 Token 设置到 Github Repository -> Settings -> Secrets，即为配置文件 [`auto_depoly.yml`](./.github/workflows/auto_depoly.yml) 的环境变量 `pypi_password`，用于 Github Workflows 自动发版
3. 在 [src](./src) 目录中创建代码，源码各级目录必须要有 `__init__.py` 文件，不然发布时不会被打包
4. 修改 [setup.py](./setup.py) 中的 `FIXME` ，按实际修改发版信息


## 开发指引

> 详见 [SOP](DevSOP.md) 文档

------
