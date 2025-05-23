import logging
import json

from textpy import code, text

CACHE_DIR = "./cache"

logger = logging.getLogger("StoryGen")

story_metadata = {
    "time":"1890s summer",
    "address":"Russian provincial town",
    "role":{
        "Belikov": "a Greek teacher afraid of life",
        "Burkin": "a schoolteacher telling the story",
        "Ivan Ivanovich": "a veterinarian listening",
        "Varinka": "a cheerful Ukrainian woman",
        "Kovalenko": "Varinka's rebellious brother"
    },
    "background":"A stagnant provincial society governed by fear and conformity",
    "outline":[
        "Two hunters shelter in a village shed and discuss local people",
        "Burkin recounts the story of Belikov, the 'man in a case'",
        "Belikov's extreme aversion to any change or unpredictability",
        "Attempts to marry Belikov to Varinka disrupt his routine",
        "Public humiliation over a cartoon and bicycle incident",
        "Belikov dies from the shock of nonconformity",
        "Reflection on how many 'case people' still exist in society"
    ]
}

class StoryNode:
    is_critical_plot_point: bool
    should_switch_to_next_plot_point: bool
    story_passage: str
    context: list[str]
    next_task: str

    def __init__(self, *, is_critical_plot_point: bool, story_passage: str, context: list[str], next_task: str, should_switch_to_next_plot_point: bool) -> None:
        self.is_critical_plot_point = is_critical_plot_point
        self.story_passage = story_passage
        self.context = context
        self.next_task = next_task
        self.should_switch_to_next_plot_point = should_switch_to_next_plot_point

    @staticmethod
    def from_dict(data: dict) -> "StoryNode":
        return StoryNode(
            is_critical_plot_point=data.get("is_critical_plot_point", False),
            story_passage=data.get("story_passage", ""),
            context=data.get("context", []),
            next_task=data.get("next_task", ""),
            should_switch_to_next_plot_point=data.get("should_switch_to_next_plot_point", False)
        )

    def to_dict(self) -> dict:
        return {
            "is_critical_plot_point": self.is_critical_plot_point,
            "story_passage": self.story_passage,
            "context": self.context,
            "next_task": self.next_task,
            "should_switch_to_next_plot_point": self.should_switch_to_next_plot_point
        }

class StoryStack:
    def __init__(self) -> None:
        self.story_nodes: list[StoryNode] = []

    def push(self, node: StoryNode) -> None:
        self.story_nodes.append(node)

    def pop(self) -> StoryNode | None:
        if self.story_nodes:
            return self.story_nodes.pop()
        return None

    def top(self) -> StoryNode | None:
        if self.story_nodes:
            return self.story_nodes[-1]
        return None

    def is_empty(self) -> bool:
        return not self.story_nodes

    def size(self) -> int:
        return len(self.story_nodes)


@text(cache=CACHE_DIR)
# Refer to the context of the node and generate a single possible continuation paragraph according to the story_metadata and task
# check_failed_reasons stores the reasons why previously generated paragraphs failed, in order to avoid making the same mistakes again.
# A paragraph contains 100 to 200 words.
# If current_critical_plot is already the last element in context['outline'], the story must end in this paragraph, and paragraphs longer than 200 words are allowed.
# Write in English.
def generate_paragraph(*, story_metadata: str, context:list[str], task:str, check_failed_reasons: list[str], current_critical_plot:str)->str:...

@text(cache=CACHE_DIR)
# Refer to the context of the node and generate the next task according to the current paragraph and story_metadata, like "Develop the conflict between the protagonist and the corrupt judge."
# if the story is end, set task to "end"
# If current_critical_plot is already the last element in context['outline'], you must return "end".
def generate_next_task(*, story_metadata: str, context:list[str], paragraph:str ,current_critical_plot:str)->str:...

@text(cache=CACHE_DIR)
# Determine whether the paragraph matches a key plot point in the outline.
def judge_paragraph_is_critical_plot_point(*, outline:str,paragraph:str)->bool:...

@text(cache=CACHE_DIR)
# Determine whether the current paragraph is at the end of the current critical plot point and needs to switch to the next plot point.
def judge_should_switch_to_next_plot_point(*, outline:str,paragraph:str,current_critical_plot:str)->bool:...

@text(cache=CACHE_DIR)
# Check whether the characters in story_passage of the node does NOT CONFLICT with the description of roles in story_metadata['role'].
# Output a dict containing match: bool ，reason: str ，adding_roles: dict[str:str]
# If new characters appear, add them to adding_roles in the format name:description,and set match=True; otherwise, set adding_roles to None
# If the description of characters match story_metadata['role'], then match = True and reason = ""
# If the description of characters do not match story_metadata['role'], then match = False and reason contains the reason for the mismatch
def check_role(*, paragraph:str, roles: dict[str,str]) -> dict: ...

@text(cache=CACHE_DIR)
# Check whether the story_passage of the node does NOT conflict with the background in story_metadata['background'].
# Output a dict containing match: bool and reason: str
# If the background does not conflict with story_metadata['background'], then match = True and reason = ""
# If the background conflicts with story_metadata['background'], then match = False and reason contains the reason for the conflict
def check_background(*, paragraph: str, background: str) -> dict: ...

@text(cache=CACHE_DIR)
# Rewrite the paragraph based on the task, current_critical_plot, and check_failed_reasons
# Return the rewritten paragraph
def rewrite(*, paragraph: str, context:list[str], task:str, current_critical_plot:str,check_failed_reasons: list[str])->str: ...

@code(cache=CACHE_DIR)
# Starting from the top of the stack, count down until the first critical plot point or the bottom of the stack. 
# If the number of paragraphs exceeds max_paragraphs, return False.
# If the top paragraph is a critical plot point, return True.
def check_is_next_plot_point_within_paragraphs(*, stack, max_paragraphs:int) -> bool: ...

@code(cache=CACHE_DIR)
# Traverse all nodes in the StoryStack, combine their story_passage fields into a complete story,
# and save the result as a text file at the specified path.
def save_story_stack_to_file(*, stack, file_path: str) -> None: ...

if __name__ == "__main__":
    for logger_name in ["CodeFunc", "TextFunc", "StoryGen"]:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("[%(asctime)s][%(levelname)s][%(name)s]: %(message)s")
        )
        logger.addHandler(handler)

    story_stack = StoryStack()
    story_stack.push(StoryNode(
        is_critical_plot_point=True,
        story_passage="Alice meets Bob in a dark alley.",
        context=["","","",""],
        next_task="The beginning of the article",
        should_switch_to_next_plot_point=False
    ))

    NUMBER_OF_NODES = 1
    MAX_PARAGRAPHS = 5
    try_gen_suitable_node_count = 3
    try_gen_suitable_plot_generation_count = 5
    check_failed_reasons = []
    current_critical_plot_index = 0

    while True:
        if story_stack.top().next_task == "end":
            break

        paragraph = generate_paragraph(
            story_metadata=json.dumps(story_metadata),
            context=json.dumps(story_stack.top().context),
            task=story_stack.top().next_task,
            check_failed_reasons=check_failed_reasons,
            current_critical_plot=story_metadata['outline'][current_critical_plot_index]
        )
        next_task = generate_next_task(
            story_metadata=json.dumps(story_metadata),
            context=json.dumps(story_stack.top().context),
            paragraph=paragraph,
            current_critical_plot=story_metadata['outline'][current_critical_plot_index]
        )
        context = story_stack.top().context[-3:] + [paragraph]
        is_critical_plot_point = judge_paragraph_is_critical_plot_point(
            outline=json.dumps(story_metadata['outline']),
            paragraph=paragraph
        )
        should_switch_to_next_plot_point = judge_should_switch_to_next_plot_point(
            outline=json.dumps(story_metadata['outline']),
            paragraph=paragraph,
            current_critical_plot=story_metadata['outline'][current_critical_plot_index]
        )

        logger.info(f"generate paragraph:{paragraph}")
        logger.info(f"generate next_task:{next_task}")
        logger.info(f"judge whether the paragraph is critical plot point:{is_critical_plot_point}")
        logger.info(f"judge whether the paragraph should switch to next plot point:{should_switch_to_next_plot_point}")

        # check the node
        check_role_result = check_role(paragraph=paragraph, roles=story_metadata['role'])
        check_background_result = check_background(paragraph=paragraph, background=story_metadata['background'])
        if not check_role_result['match']:
            logger.info("don't match the roles in story_metadata['role']")
            check_failed_reasons.append(check_role_result['reason'])
            rewrite_paragraph = paragraph
            for i in range(5):
                logger.info(f"reason:{check_role_result['reason']}")
                logger.info(f"The {i}-th attempt")
                rewrite_paragraph = rewrite(
                    paragraph=rewrite_paragraph,
                    context=story_stack.top().context,
                    task=story_stack.top().next_task,
                    current_critical_plot=story_metadata['outline'][current_critical_plot_index],
                    check_failed_reasons=check_failed_reasons
                )
                logger.info(f"rewrite paragraph:{i + 1}")
                check_role_result = check_role(paragraph=rewrite_paragraph, roles=story_metadata['role'])
                if check_role_result['match']:
                    paragraph = rewrite_paragraph
                    break
                else:
                    check_failed_reasons.append(check_role_result['reason'])
                if i == 4:
                    raise ValueError(f"Failed to generate a valid paragraph matching the roles after 5 rewrites. Reasons: {check_failed_reasons}")

        check_failed_reasons = []

        if check_role_result.get('adding_roles'):
            story_metadata['role'].update(check_role_result['adding_roles'])
            logger.info(f"add roles:{check_role_result['adding_roles']}")

        if not check_background_result['match']:
            logger.info("don't match the background in story_metadata['background']")
            check_failed_reasons.append(check_background_result['reason'])
            rewrite_paragraph = paragraph
            for i in range(5):
                logger.info(f"reason:{check_background_result['reason']}")
                logger.info(f"rewrite paragraph:{i+1}")
                rewrite_paragraph = rewrite(
                    paragraph=rewrite_paragraph,
                    context=story_stack.top().context,
                    task=story_stack.top().next_task,
                    current_critical_plot=story_metadata['outline'][current_critical_plot_index],
                    check_failed_reasons=check_failed_reasons
                )
                check_background_result = check_background(paragraph=rewrite_paragraph, background=story_metadata['background'])
                if check_background_result['match']:
                    paragraph = rewrite_paragraph
                    break
                else:
                    check_failed_reasons.append(check_background_result['reason'])
                if i == 4:
                    raise ValueError(f"Failed to generate a valid paragraph matching the background after 5 rewrites. Reasons: {check_failed_reasons}")

        check_failed_reasons = []

        node = StoryNode(
            is_critical_plot_point=is_critical_plot_point,
            story_passage=paragraph,
            context=context,
            next_task=next_task,
            should_switch_to_next_plot_point=should_switch_to_next_plot_point
        )

        if not check_is_next_plot_point_within_paragraphs(
            stack=story_stack,
            max_paragraphs=MAX_PARAGRAPHS
        ):
            try_gen_suitable_plot_generation_count -= 1
            logger.info("The next plot point is too far away")
            if try_gen_suitable_plot_generation_count <= 0:
                logger.warning("The next plot point is too far away, please check the story metadata.")
                break
            while not story_stack.top().is_critical_plot_point:
                story_stack.pop()
            continue

        if node:
            story_stack.push(node)
        if node.should_switch_to_next_plot_point:
            current_critical_plot_index += 1

        print(f"Current story passage: {story_stack.top().story_passage}")
        try_gen_suitable_node_count = 3
        try_gen_suitable_plot_generation_count = 5

    save_story_stack_to_file(
        stack=story_stack,
        file_path="story.txt"
    )