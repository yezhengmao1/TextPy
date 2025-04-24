from textpy.jit import text

@text(cache=None)
def translate_text_to_Chinese(*, src: str,tgt:str) -> str: ...

@text(cache=None)
def summary_text(*, text:str) -> str: ...

def get_long_text():
    text = (
        "As mentioned before, researchers have introduced several properties to help describe and define agents in the field of AI. Here, we will delve into some key properties, elucidate their relevance to LLMs, and thereby expound on why LLMs are highly suited to serve as the main part of brains of AI agents."

        "Autonomy. Autonomy means that an agent operates without direct intervention from humans or others and possesses a degree of control over its actions and internal states. This implies that an agent should not only possess the capability to follow explicit human instructions for task completion but also exhibit the capacity to initiate and execute actions independently. LLMs can demonstrate a form of autonomy through their ability to generate human-like text, engage in conversations, and perform various tasks without detailed step-by-step instructions. Moreover, they can dynamically adjust their outputs based on environmental input, reflecting a degree of adaptive autonomy. Furthermore, they can showcase autonomy through exhibiting creativity like coming up with novel ideas, stories, or solutions that haven’t been explicitly programmed into them. This implies a certain level of self-directed exploration and decision-making. Applications like Auto-GPT exemplify the significant potential of LLMs in constructing autonomous agents. Simply by providing them with a task and a set of available tools, they can autonomously formulate plans and execute them to achieve the ultimate goal."

        "Reactivity. Reactivity in an agent refers to its ability to respond rapidly to immediate changes and stimuli in its environment. This implies that the agent can perceive alterations in its surroundings and promptly take appropriate actions. Traditionally, the perceptual space of language models has been confined to textual inputs, while the action space has been limited to textual outputs. However, researchers have demonstrated the potential to expand the perceptual space of LLMs using multimodal fusion techniques, enabling them to rapidly process visual and auditory information from the environment. Similarly, it’s also feasible to expand the action space of LLMs through embodiment techniques and tool usage. These advancements enable LLMs to effectively interact with the real-world physical environment and carry out tasks within it. One major challenge is that LLM-based agents, when performing non-textual actions, require an intermediate step of generating thoughts or formulating tool usage in textual form before eventually translating them into concrete actions. This intermediary process consumes time and reduces the response speed. However, this aligns closely with human behavioral patterns, where the principle of “think before you act” is observed."

        "Pro-activeness. Pro-activeness denotes that agents don’t merely react to their environments; they possess the capacity to display goal-oriented actions by proactively taking the initiative. This property emphasizes that agents can reason, make plans, and take proactive measures in their actions to achieve specific goals or adapt to environmental changes. Although intuitively the paradigm of next token prediction in LLMs may not possess intention or desire, research has shown that they can implicitly generate representations of these states and guide the model’s inference process. LLMs have demonstrated a strong capacity for generalized reasoning and planning. By prompting large language models with instructions like “let’s think step by step”, we can elicit their reasoning abilities, such as logical and mathematical reasoning. Similarly, large language models have shown the emergent ability of planning in forms of goal reformulation, task decomposition, and adjusting plans in response to environmental changes."

        "Social ability. Social ability refers to an agent’s capacity to interact with other agents, including humans, through some kind of agent-communication language. Large language models exhibit strong natural language interaction abilities like understanding and generation. Compared to structured languages or other communication protocols, such capability enables them to interact with other models or humans in an interpretable manner. This forms the cornerstone of social ability for LLM-based agents. Many researchers have demonstrated that LLM-based agents can enhance task performance through social behaviors such as collaboration and competition. By inputting specific prompts, LLMs can also play different roles, thereby simulating the social division of labor in the real world. Furthermore, when we place multiple agents with distinct identities into a society, emergent social phenomena can be observed."
    )
    return text

if __name__ == "__main__":
    long_text = get_long_text()
    sumarized_text = summary_text(text = long_text)
    translated_info = translate_text_to_Chinese(src = sumarized_text, tgt = "Chinese", return_content = "只保留翻译")
    print(translated_info)
