from typing import Dict, List


def build_rag_prompt(question: str, sources: List[Dict]) -> str:
    context = "\n\n".join(
        f"[Source {idx + 1} | {item.get('source')}]\n{item.get('content')}"
        for idx, item in enumerate(sources)
    )
    return f"""你是一个企业私有知识库 AI 助手。请优先根据给定资料回答问题。
如果资料不足，请明确说明“知识库中没有足够信息”，不要编造。

【知识库资料】
{context}

【用户问题】
{question}

【回答要求】
1. 回答简洁、准确。
2. 能引用知识库内容时，尽量结合资料回答。
3. 如果资料不足，说明缺少哪些信息。
"""
