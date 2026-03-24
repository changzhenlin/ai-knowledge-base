# Java RAG / Agent 面试题 - 2026-03-23

## 题目
如果让你用 Java 从零搭一个 RAG 系统，核心技术栈会怎么选？

## 详解答案
我会优先选择 Spring Boot 作为服务框架，LangChain4j 或 Spring AI 作为模型编排层，MySQL/PG 存业务数据，Redis 做缓存，向量库根据规模选 Elasticsearch、Milvus、Qdrant 或 PGVector。文档解析会接 PDF/Word/HTML 解析组件，异步任务用 MQ 或定时任务体系处理 embedding 和索引更新。监控方面要把检索耗时、命中率、上下文 token、LLM 耗时拆开看，不然线上出问题只会看到一片“慢”，像在医院看体检单只知道自己不太行。

## 面试官真正想听什么
- 服务层、编排层、存储层要分清职责
- 向量库选型看规模和检索需求
- 监控必须拆指标，不然无法定位问题

---
*生成时间：2026-03-24 10:47:54*
