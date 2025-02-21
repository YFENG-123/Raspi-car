from zhipuai import ZhipuAI

client = ZhipuAI(
    api_key="f8ab318eb41a4d34a2524ec4f8706157.s6SZey1ivTJkcrvJ"
) 
prompt = """你是一个智能语音助手，负责将用户的语音转换为对应的指令 ID。

下面是指令的映射表（id → description）：
- 1001 → 小爱同学
- 1002 → 瞄准
- 1003 → 开火
- 0 → 未知指令

你的任务是：
1. **尽可能匹配** 用户的输入到最接近的指令 ID，避免返回 0，除非完全无法推测意图。
3. **允许一定程度的错误匹配**，例如“灯光”可以匹配“打开灯”或“关闭灯”，“调高空调”可以匹配“提高温度”。
4. **仅返回整数 ID，不要包含任何其他文本**。
用户输入："[锁定目标]"

返回格式：仅返回对应的指令 **整数 ID**，如果无法匹配，则返回 0。"""

response = client.chat.completions.create(
    model="glm-4-plus",  # 请填写您要调用的模型名称
    messages=[
        {"role": "user", "content": prompt},
    ],
)
print(response.choices[0].message)
