# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此代码仓库中工作时提供指导。

## 技术栈

- Java 17+, Spring Boot 3.x
- 构建工具: Maven (pom.xml) 或 Gradle (build.gradle)
- 数据库: PostgreSQL/MySQL + Spring Data JPA + Hibernate 6
- API 设计: REST, OpenAPI 3.0 (springdoc-openapi)
- 测试: JUnit 5 + Mockito + Testcontainers

## 代码规范

- 所有 Service 类使用 `@Service`，事务通过 `@Transactional` 管理
- Controller 层仅处理请求解析和响应格式化；业务逻辑放在 Service 层
- Entity 类放在 `entity/` 包，DTO 放在 `dto/` 包；API 响应中绝不直接暴露 Entity
- 使用构造器注入（`@RequiredArgsConstructor` + `private final` 字段）；禁止使用 `@Autowired` 字段注入
- 通过 `@RestControllerAdvice` 统一异常处理，配合自定义异常类
- 测试与源码类同目录存放
- 遵循 RESTful API 设计原则

## 构建命令

每条命令单独执行，不要链式调用。

- 构建: `mvn clean package -DskipTests`
- 运行测试: `mvn test`
- 运行单个测试: `mvn test -Dtest=ClassName#methodName`
- 集成测试（需要 Docker）: `mvn verify`
- 运行应用: `mvn spring-boot:run`

## 安全规则

- 不要硬编码凭证或 API 密钥；使用环境变量或 Spring Cloud Config
- 不要将敏感端点（actuator、health、metrics）暴露给公网
- 使用参数化查询；禁止拼接 SQL 字符串

## 反模式

- 禁止在 Controller 中编写业务逻辑
- 禁止在 Entity 类上使用 `@Data`（会导致 equals/hashCode 问题）；使用 `@Getter` + `@Setter` 替代
- 禁止将 `Optional` 作为字段类型；仅作为方法返回值
- 禁止在 Repository 层编写复杂查询；使用 Specification 或 Querydsl
- 禁止在只读操作上使用 `@Transactional` 而不设置 `readOnly = true`
