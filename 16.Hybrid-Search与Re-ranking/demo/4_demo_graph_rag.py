"""
============================================================
Demo 4: 知识图谱增强（Graph RAG）
============================================================

本 Demo 展示 Graph RAG 的核心概念和实现：
1. 从文本中抽取实体和关系（模拟 LLM 抽取）
2. 用 NetworkX 构建知识图谱
3. 多跳查询：沿着关系链走多步找到答案
4. 向量检索 + 图检索的融合思路

不需要 API Key，所有 LLM 调用都用模拟函数替代。
需要安装 networkx：pip install networkx
"""

import networkx as nx
from typing import List, Dict, Tuple, Optional


# ============================================================
# 第一部分：模拟 LLM 的实体关系抽取
# ============================================================

def mock_extract_entities_and_relations(text: str) -> Dict:
    """
    模拟 LLM 从文本中抽取实体和关系。
    实际项目中，这里会调用 LLM（如 GPT-4）来抽取。

    Args:
        text: 原始文本

    Returns:
        包含实体和关系的字典
    """
    # 模拟抽取结果
    # 实际项目中，Prompt 大致如下：
    # "请从以下文本中抽取实体和关系，输出 JSON 格式..."
    return {
        "entities": [],   # 由具体文本决定
        "relations": []   # 由具体文本决定
    }


# ============================================================
# 第二部分：知识图谱构建器
# ============================================================

class KnowledgeGraphBuilder:
    """
    知识图谱构建器

    功能：
    - 从三元组构建知识图谱
    - 添加实体和关系
    - 支持多跳查询

    使用 NetworkX 的有向图（DiGraph）来表示知识图谱：
    - 节点 = 实体
    - 边 = 关系（边的属性存储关系类型）
    """

    def __init__(self):
        # 创建有向图
        self.graph = nx.DiGraph()
        # 存储所有关系类型（用于查询时匹配）
        self.relation_types = set()

    def add_triple(self, head: str, relation: str, tail: str):
        """
        添加一个三元组（头实体, 关系, 尾实体）

        例如：("张三", "直属上司", "李四") 表示"张三的直属上司是李四"

        Args:
            head: 头实体
            relation: 关系类型
            tail: 尾实体
        """
        # 添加节点（如果不存在）
        if not self.graph.has_node(head):
            self.graph.add_node(head, type="entity")
        if not self.graph.has_node(tail):
            self.graph.add_node(tail, type="entity")

        # 添加边（带关系属性）
        self.graph.add_edge(head, tail, relation=relation)
        self.relation_types.add(relation)

    def add_triples(self, triples: List[Tuple[str, str, str]]):
        """
        批量添加三元组

        Args:
            triples: 三元组列表 [(头实体, 关系, 尾实体), ...]
        """
        for head, relation, tail in triples:
            self.add_triple(head, relation, tail)

    def get_neighbors(self, entity: str, relation: Optional[str] = None) -> List[Dict]:
        """
        获取实体的邻居节点（沿指定关系）

        Args:
            entity: 实体名称
            relation: 关系类型（可选，不指定则返回所有邻居）

        Returns:
            邻居列表 [{"entity": "李四", "relation": "直属上司"}, ...]
        """
        if entity not in self.graph:
            return []

        neighbors = []
        # 遍历出边
        for _, target, data in self.graph.out_edges(entity, data=True):
            if relation is None or data.get("relation") == relation:
                neighbors.append({
                    "entity": target,
                    "relation": data.get("relation", "未知")
                })
        return neighbors

    def multi_hop_query(self, start_entity: str, relation_chain: List[str]) -> List[str]:
        """
        多跳查询：沿着关系链走多步

        例如：multi_hop_query("张三", ["直属上司", "手机号"])
        表示：找到张三的直属上司的手机号

        实现思路：
        从起始实体出发，沿着关系链一步一步走，
        每一步找到满足关系的邻居，作为下一步的起点。

        Args:
            start_entity: 起始实体
            relation_chain: 关系链 ["关系1", "关系2", ...]

        Returns:
            最终找到的实体列表
        """
        current_entities = [start_entity]

        for relation in relation_chain:
            next_entities = []
            for entity in current_entities:
                neighbors = self.get_neighbors(entity, relation)
                next_entities.extend([n["entity"] for n in neighbors])

            if not next_entities:
                # 某一步找不到匹配的邻居，查询失败
                return []

            current_entities = next_entities

        return current_entities

    def find_path(self, source: str, target: str) -> Optional[List[str]]:
        """
        查找两个实体之间的最短路径

        Args:
            source: 起始实体
            target: 目标实体

        Returns:
            路径列表，如果不存在则返回 None
        """
        try:
            path = nx.shortest_path(self.graph, source, target)
            return path
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None

    def find_path_with_relations(self, source: str, target: str) -> Optional[List[Dict]]:
        """
        查找两个实体之间的路径（包含关系信息）

        Args:
            source: 起始实体
            target: 目标实体

        Returns:
            路径详情 [{"from": "张三", "relation": "上司", "to": "李四"}, ...]
        """
        path = self.find_path(source, target)
        if path is None:
            return None

        path_details = []
        for i in range(len(path) - 1):
            edge_data = self.graph.get_edge_data(path[i], path[i + 1])
            path_details.append({
                "from": path[i],
                "relation": edge_data.get("relation", "未知"),
                "to": path[i + 1]
            })
        return path_details

    def get_all_triples(self) -> List[Tuple[str, str, str]]:
        """获取图中所有三元组"""
        triples = []
        for head, tail, data in self.graph.edges(data=True):
            triples.append((head, data.get("relation", "未知"), tail))
        return triples

    def get_entity_info(self, entity: str) -> Dict:
        """
        获取实体的所有信息（所有入边和出边）

        Args:
            entity: 实体名称

        Returns:
            实体信息字典
        """
        if entity not in self.graph:
            return {"exists": False}

        info = {
            "exists": True,
            "name": entity,
            "outgoing": [],  # 出边：该实体作为头实体
            "incoming": []   # 入边：该实体作为尾实体
        }

        # 出边
        for _, target, data in self.graph.out_edges(entity, data=True):
            info["outgoing"].append({
                "relation": data.get("relation", "未知"),
                "target": target
            })

        # 入边
        for source, _, data in self.graph.in_edges(entity, data=True):
            info["incoming"].append({
                "relation": data.get("relation", "未知"),
                "source": source
            })

        return info


# ============================================================
# 第三部分：Graph RAG 管道
# ============================================================

class GraphRAG:
    """
    Graph RAG 管道

    将知识图谱的图检索与传统向量检索结合：
    1. 向量检索：找语义相似的文档片段
    2. 图检索：沿关系链找结构化答案
    3. 融合：将两种结果合并，交给 LLM 生成最终答案
    """

    def __init__(self, kg: KnowledgeGraphBuilder):
        self.kg = kg
        # 模拟文档库（实际项目中是向量数据库）
        self.documents = {}

    def add_document(self, doc_id: str, content: str, entities: List[str]):
        """
        添加文档到模拟文档库

        Args:
            doc_id: 文档ID
            content: 文档内容
            entities: 文档中提到的实体
        """
        self.documents[doc_id] = {
            "content": content,
            "entities": entities
        }

    def vector_search(self, query: str) -> List[str]:
        """
        模拟向量检索（语义匹配）
        实际项目中会用 Embedding + 向量数据库

        Args:
            query: 用户查询

        Returns:
            相关文档内容列表
        """
        results = []
        query_lower = query.lower()

        # 简单的关键词匹配模拟
        for doc_id, doc in self.documents.items():
            for entity in doc["entities"]:
                if entity in query:
                    results.append(doc["content"])
                    break

        return results

    def graph_search(self, query: str) -> Optional[str]:
        """
        图检索：从查询中识别实体和关系，进行图遍历

        Args:
            query: 用户查询

        Returns:
            图检索结果（结构化答案）
        """
        # 简单的实体识别（实际项目中用 LLM）
        entities_in_query = []
        for node in self.kg.graph.nodes():
            if node in query:
                entities_in_query.append(node)

        if not entities_in_query:
            return None

        # 尝试多跳查询
        # 这里用简化的逻辑：查找实体的所有关系链
        results = []
        for entity in entities_in_query:
            entity_info = self.kg.get_entity_info(entity)
            if entity_info.get("exists"):
                # 输出该实体的所有关系
                for out in entity_info["outgoing"]:
                    results.append(f"{entity} 的 {out['relation']} 是 {out['target']}")
                for inc in entity_info["incoming"]:
                    results.append(f"{inc['source']} 的 {inc['relation']} 是 {entity}")

        return "\n".join(results) if results else None

    def query(self, question: str) -> Dict:
        """
        Graph RAG 查询入口

        融合向量检索和图检索的结果。

        Args:
            question: 用户问题

        Returns:
            包含向量检索结果和图检索结果的字典
        """
        # 向量检索
        vector_results = self.vector_search(question)

        # 图检索
        graph_results = self.graph_search(question)

        return {
            "question": question,
            "vector_results": vector_results,
            "graph_results": graph_results,
            "answer": self._generate_answer(question, vector_results, graph_results)
        }

    def _generate_answer(self, question: str, vector_results: List[str],
                         graph_results: Optional[str]) -> str:
        """
        模拟 LLM 生成最终答案
        实际项目中会将两种检索结果都传给 LLM
        """
        parts = []
        if graph_results:
            parts.append(f"[图检索结果] {graph_results}")
        if vector_results:
            parts.append(f"[向量检索结果] {'; '.join(vector_results)}")

        if not parts:
            return "抱歉，未找到相关信息。"
        return "\n".join(parts)


# ============================================================
# 第四部分：演示运行
# ============================================================

def print_separator(title: str):
    """打印分隔线"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def demo_build_knowledge_graph():
    """
    演示1：构建知识图谱
    """
    print_separator("演示1：构建知识图谱")

    # 创建知识图谱构建器
    kg = KnowledgeGraphBuilder()

    # 模拟从文本中抽取的三元组
    # 实际项目中，这些三元组由 LLM 从文档中抽取
    triples = [
        # 人物关系
        ("张三", "直属上司", "李四"),
        ("张三", "所属部门", "技术部"),
        ("张三", "职位", "高级工程师"),
        ("李四", "职位", "技术总监"),
        ("李四", "所属部门", "技术部"),
        ("李四", "手机号", "13812345678"),
        ("李四", "邮箱", "lisi@company.com"),
        ("王五", "直属上司", "李四"),
        ("王五", "所属部门", "技术部"),
        ("王五", "职位", "工程师"),

        # 部门关系
        ("技术部", "上级部门", "公司"),
        ("技术部", "总监", "李四"),
        ("市场部", "总监", "赵六"),
        ("公司", "CEO", "钱七"),

        # 项目关系
        ("张三", "参与项目", "RAG系统"),
        ("王五", "参与项目", "RAG系统"),
        ("RAG系统", "使用技术", "LangChain"),
        ("RAG系统", "使用技术", "向量数据库"),
    ]

    # 批量添加三元组
    kg.add_triples(triples)

    print("知识图谱构建完成！")
    print(f"  实体数量（节点）：{kg.graph.number_of_nodes()}")
    print(f"  关系数量（边）：{kg.graph.number_of_edges()}")
    print(f"  关系类型：{kg.relation_types}")
    print()
    print("所有三元组：")
    for head, relation, tail in kg.get_all_triples():
        print(f"  ({head}, {relation}, {tail})")

    return kg


def demo_entity_query(kg: KnowledgeGraphBuilder):
    """
    演示2：实体信息查询
    """
    print_separator("演示2：实体信息查询")

    # 查询张三的所有信息
    entity = "张三"
    info = kg.get_entity_info(entity)

    print(f"查询实体：{entity}")
    print(f"  存在：{info['exists']}")
    print(f"  出边（张三 → ?）：")
    for out in info["outgoing"]:
        print(f"    {entity} --[{out['relation']}]--> {out['target']}")
    print(f"  入边（? → 张三）：")
    for inc in info["incoming"]:
        print(f"    {inc['source']} --[{inc['relation']}]--> {entity}")


def demo_multi_hop_query(kg: KnowledgeGraphBuilder):
    """
    演示3：多跳查询（Graph RAG 的核心能力）
    """
    print_separator("演示3：多跳查询")

    # 查询1：张三的直属上司是谁？（1跳）
    print("【查询1】张三的直属上司是谁？")
    result = kg.multi_hop_query("张三", ["直属上司"])
    print(f"  答案：{result}")
    print()

    # 查询2：张三的直属上司的手机号是多少？（2跳）
    print("【查询2】张三的直属上司的手机号是多少？")
    result = kg.multi_hop_query("张三", ["直属上司", "手机号"])
    print(f"  答案：{result}")
    print()

    # 查询3：张三的直属上司的邮箱是多少？（2跳）
    print("【查询3】张三的直属上司的邮箱是多少？")
    result = kg.multi_hop_query("张三", ["直属上司", "邮箱"])
    print(f"  答案：{result}")
    print()

    # 查询4：技术部的总监的手机号？（2跳）
    print("【查询4】技术部的总监的手机号是多少？")
    result = kg.multi_hop_query("技术部", ["总监", "手机号"])
    print(f"  答案：{result}")
    print()

    # 查询5：张三参与的项目使用了什么技术？（2跳）
    print("【查询5】张三参与的项目使用了什么技术？")
    result = kg.multi_hop_query("张三", ["参与项目", "使用技术"])
    print(f"  答案：{result}")


def demo_path_finding(kg: KnowledgeGraphBuilder):
    """
    演示4：路径查找（任意两实体之间的关系链）
    """
    print_separator("演示4：路径查找")

    # 查找张三到公司之间的路径
    source, target = "张三", "钱七"
    print(f"【路径查找】{source} → {target}")

    path = kg.find_path(source, target)
    if path:
        print(f"  最短路径：{' → '.join(path)}")

    path_details = kg.find_path_with_relations(source, target)
    if path_details:
        print(f"  详细路径：")
        for step in path_details:
            print(f"    {step['from']} --[{step['relation']}]--> {step['to']}")

    print()

    # 查找王五到 LangChain 之间的路径
    source, target = "王五", "LangChain"
    print(f"【路径查找】{source} → {target}")

    path = kg.find_path(source, target)
    if path:
        print(f"  最短路径：{' → '.join(path)}")

    path_details = kg.find_path_with_relations(source, target)
    if path_details:
        print(f"  详细路径：")
        for step in path_details:
            print(f"    {step['from']} --[{step['relation']}]--> {step['to']}")


def demo_graph_rag_pipeline():
    """
    演示5：完整的 Graph RAG 管道
    """
    print_separator("演示5：Graph RAG 管道（图检索 + 向量检索融合）")

    # 构建知识图谱
    kg = KnowledgeGraphBuilder()
    triples = [
        ("张三", "直属上司", "李四"),
        ("张三", "所属部门", "技术部"),
        ("李四", "手机号", "13812345678"),
        ("李四", "职位", "技术总监"),
        ("RAG系统", "使用技术", "LangChain"),
    ]
    kg.add_triples(triples)

    # 创建 Graph RAG 管道
    rag = GraphRAG(kg)

    # 添加模拟文档（向量检索的数据源）
    rag.add_document("doc1", "张三是技术部的高级工程师，他的直属上司是李四。", ["张三", "李四", "技术部"])
    rag.add_document("doc2", "李四是技术总监，手机号是13812345678。", ["李四"])
    rag.add_document("doc3", "RAG系统使用了 LangChain 和向量数据库技术。", ["RAG系统", "LangChain"])

    # 查询演示
    questions = [
        "张三的直属上司的手机号是多少？",
        "张三属于哪个部门？",
        "RAG系统使用了什么技术？",
    ]

    for question in questions:
        print(f"问题：{question}")
        result = rag.query(question)
        print(f"  {result['answer']}")
        print()


def demo_comparison():
    """
    演示6：传统 RAG vs Graph RAG 对比
    """
    print_separator("演示6：传统 RAG vs Graph RAG 对比")

    print("场景：用户问 '张三的直属上司的手机号是多少？'\n")

    print("【传统 RAG 的做法】")
    print("  1. 将问题转为向量")
    print("  2. 在文档库中找语义相似的片段")
    print("  3. 可能找到：'张三是技术部的高级工程师'")
    print("  4. 也可能找到：'李四是技术总监，手机号是13812345678'")
    print("  5. 但很难确定'张三的直属上司'就是'李四'")
    print("  → 需要 LLM 推理，可能出错\n")

    print("【Graph RAG 的做法】")
    print("  1. 识别实体：张三")
    print("  2. 图遍历：张三 →[直属上司]→ 李四 →[手机号]→ 13812345678")
    print("  3. 直接得到精确答案：13812345678")
    print("  → 精确、高效、不依赖 LLM 推理\n")

    print("【结论】")
    print("  - 向量检索擅长：语义匹配（'RAG是什么' → 找相关文档）")
    print("  - 图检索擅长：关系推理（'张三的上司的手机号' → 沿关系链走）")
    print("  - 两者结合 = 既理解语义，又理解关系")


# ============================================================
# 主程序入口
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  知识图谱增强（Graph RAG）Demo")
    print("  实体关系抽取 → 知识图谱构建 → 多跳查询")
    print("=" * 60)

    # 演示1：构建知识图谱
    kg = demo_build_knowledge_graph()

    # 演示2：实体信息查询
    demo_entity_query(kg)

    # 演示3：多跳查询（核心能力）
    demo_multi_hop_query(kg)

    # 演示4：路径查找
    demo_path_finding(kg)

    # 演示5：Graph RAG 管道
    demo_graph_rag_pipeline()

    # 演示6：传统 RAG vs Graph RAG 对比
    demo_comparison()

    print_separator("Demo 完成")
    print("关键要点：")
    print("1. 知识图谱 = 实体 + 关系，用有向图表示")
    print("2. Graph RAG = 向量检索 + 图检索的融合")
    print("3. 多跳查询：沿着关系链走多步，精确找到答案")
    print("4. 适合场景：关系推理、多跳查询、组织架构查询")
    print("5. 实现工具：NetworkX（轻量级）、Neo4j（生产级）")
