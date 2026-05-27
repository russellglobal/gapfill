# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码仓库中工作时提供指导。

## 技术栈

- React 19 + TypeScript（strict 模式）
- 构建工具: Vite
- 状态管理: 优先使用 React Server Components；客户端状态用 useState/useReducer
- 数据校验: Zod
- 测试: Vitest + React Testing Library
- 样式: Tailwind CSS（不使用 CSS Modules 或 styled-components）

## 组件规范

- 仅使用函数式组件；禁止使用类组件
- 默认为 Server Components；仅在需要交互时才使用 "use client"
- Props 使用 TypeScript interface 定义，不使用 type alias
- 命名: 文件名 PascalCase（UserProfile.tsx），导出名 camelCase
- 默认使用命名导出；保留文件（page.tsx、layout.tsx）使用默认导出
- 测试与组件同目录存放

## 数据获取

- 使用异步 Server Components 加载数据；禁止使用 useEffect 获取数据
- 使用 Next.js fetch() 并配合 cache/revalidation 选项
- 禁止使用 getServerSideProps 或 getStaticProps
- use() hook 需要稳定的 promise 引用；禁止内联创建（如 use(fetch('/api'))）

## 构建命令

每条命令单独执行，不要链式调用。

- 开发: `npm run dev`
- 构建: `npm run build`
- 类型检查: `npx tsc --noEmit`
- Lint: `npm run lint`
- 测试: `npm run test`
- 运行单个测试: `npx vitest run -t "test name"`

## 安全规则

- 禁止在客户端代码中存储密钥、API 密钥或 Token
- 禁止使用 dangerouslySetInnerHTML
- 渲染前对所有用户输入进行消毒

## 反模式

- 禁止在 Server Components 中使用 useState/useEffect/useRef
- 禁止使用内联样式；使用 Tailwind 类
- 禁止直接操作 DOM；使用 refs
- 禁止使用 `any` 类型；启用 strict 模式并修复类型错误
- 禁止向 use() 传入内联 promise
- 禁止在提交前跳过类型检查
