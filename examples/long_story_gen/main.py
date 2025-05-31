import logging
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger("LongStoryGen")

# 小说元数据和大纲模板
metadata = {
    "main_character": "张三",
    "main_character_description": "出身贫寒，但是修炼天赋极高，性格坚毅不拔，渴望通过修炼改变命运。",
    "main_setting": "一个充满修仙者的世界，修炼者通过吸收天地灵气来提升自己的修为，争夺资源和地位。",
    "characters": {},
    "settings":{}
}

outline_template = {
    "第1卷": {
        "description": "大大宗",
        "contents": {
            "第1部": {
                "description": "张三加入大大宗",
                "contents": {}
            },
            "第2部": {
                "description": "张三被强迫接收危险的任务，离开大大宗完成任务",
                "contents": {}
            },
            "第3部": {
                "description": "张三在外界偶遇机缘，疯狂修炼，实力大涨",
                "contents": {}
            },
            "第4部": {
                "description": "张三回到大大宗，打败了原先打压他的人，受到尊敬",
                "contents": {}
            },
            "第5部": {
                "description": "张三决定离开宗门，寻找更大的机缘",
                "contents": {}
            }
        }
    },
}

def gen_outline():
    """
    生成长篇小说大纲，并将每个部的内容、上下文、元数据分别写入对应文件夹。
    """
    from plan import plot, character, setting
    global metadata
    global outline_template

    part_context = []
    chapter_context = []
    section_context = []
    max_context_length = 50  # 上下文最大长度
    initial_part_dir = None # 初始部目录，如果有则从该目录开始生成，便于从先前中断的地方继续

    # 切换到脚本所在目录，保证相对路径正确
    os.chdir(os.path.dirname(__file__))
    logger.info(f"当前工作目录: {os.getcwd()}")

    # 如果 initial_part_dir 存在，则从文件初始化上下文和大纲
    if initial_part_dir and os.path.exists(initial_part_dir):
        part_context_path = os.path.join(initial_part_dir, "part_context.txt")
        chapter_context_path = os.path.join(initial_part_dir, "chapter_context.txt")
        section_context_path = os.path.join(initial_part_dir, "section_context.txt")
        metadata_path = os.path.join(initial_part_dir, "metadata.json")
        outline_template_path = os.path.join(initial_part_dir, "outline_template.json")

        if os.path.exists(part_context_path):
            with open(part_context_path, "r", encoding="utf-8") as f:
                part_context = [line.strip() for line in f if line.strip()]
        if os.path.exists(chapter_context_path):
            with open(chapter_context_path, "r", encoding="utf-8") as f:
                chapter_context = [line.strip() for line in f if line.strip()]
        if os.path.exists(section_context_path):
            with open(section_context_path, "r", encoding="utf-8") as f:
                section_context = [line.strip() for line in f if line.strip()]
        if os.path.exists(metadata_path):
            with open(metadata_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        if os.path.exists(outline_template_path):
            with open(outline_template_path, "r", encoding="utf-8") as f:
                outline_template = json.load(f)

    # 遍历大纲结构，逐层生成内容
    for volume, volume_content in outline_template.items():
        # 只保留 initial_part_dir 及其之后的部
        part_names = list(volume_content["contents"].keys())
        idx = 0
        if initial_part_dir and os.path.basename(initial_part_dir) in part_names:
            idx = part_names.index(os.path.basename(initial_part_dir))
        for part in part_names[idx+1:]:
            part_content = volume_content["contents"][part]
            logger.info(f"  {part}: {part_content['description']}")

            # 生成章节概要
            chapter_descriptions = plot(
                metadata="",
                parent_desc=part_content["description"],
                characters="",
                settings="",
                outline=json.dumps(volume),
                context=json.dumps(part_context)
            )
            if len(part_context) >= max_context_length:
                part_context.pop(0)
            part_context.append(part_content["description"])
            chapters = {}
            for idx, desc in enumerate(chapter_descriptions, 1):
                chapter_name = f"第{idx}章"
                chapters[chapter_name] = {
                    "description": desc,
                    "caracters": {},
                    "settings": {},
                    "contents": {}
                }
            part_content["contents"] = chapters

            # 生成每章内容
            for chapter, chapter_content in part_content.get("contents", {}).items():
                logger.info(f"    {chapter}: {chapter_content['description']}")
                chapter_setting_cache = {}
                characters = character(
                    metadata=json.dumps(metadata["characters"]),
                    context=chapter_content["description"]
                )
                settings = setting(
                    metadata=json.dumps(chapter_setting_cache),
                    context=chapter_content["description"]
                )
                metadata["characters"].update(characters)
                metadata["settings"].update(settings)
                chapter_setting_cache.update(settings)
                chapter_content["caracters"] = characters
                chapter_content["settings"] = settings

                # 生成节概要
                section_descriptions = plot(
                    metadata="",
                    parent_desc=chapter_content["description"],
                    characters=json.dumps(characters),
                    settings=json.dumps(settings),
                    outline=json.dumps(part_content["contents"]),
                    context=json.dumps(chapter_context)
                )
                if len(chapter_context) >= max_context_length:
                    chapter_context.pop(0)
                chapter_context.append(chapter_content["description"])
                sections = {}
                for idx, desc in enumerate(section_descriptions, 1):
                    section_name = f"第{idx}节"
                    sections[section_name] = {
                        "description": desc,
                        "caracters": {},
                        "settings": {},
                        "contents": {}
                    }
                chapter_content["contents"] = sections

                # 生成每节内容
                for section, section_content in chapter_content.get("contents", {}).items():
                    logger.info(f"      {section}: {section_content['description']}")
                    characters = character(
                        metadata=json.dumps(metadata["characters"]),
                        context=section_content["description"]
                    )
                    settings = setting(
                        metadata=json.dumps(chapter_setting_cache),
                        context=section_content["description"]
                    )
                    section_content["caracters"] = characters
                    section_content["settings"] = settings
                    metadata["characters"].update(characters)
                    metadata["settings"].update(settings)
                    paragraphs = plot(
                        metadata="",
                        parent_desc=section_content["description"],
                        characters=json.dumps(characters),
                        settings=json.dumps(settings),
                        outline=json.dumps(chapter_content["contents"]),
                        context=json.dumps(section_context)
                    )
                    if len(section_context) >= max_context_length:
                        section_context.pop(0)
                    section_context.append(section_content["description"])
                    section_content["contents"] = {f"第{idx}段": para for idx, para in enumerate(paragraphs, 1)}
                    for para_idx, para in enumerate(paragraphs, 1):
                        logger.info(f"        第{para_idx}段: {para}")

            # 保存当前部的内容到对应文件夹
            part_dir = part
            if not os.path.exists(part_dir):
                os.makedirs(part_dir)
            with open(os.path.join(part_dir, "outline_template.json"), "w", encoding="utf-8") as f:
                json.dump(outline_template, f, ensure_ascii=False, indent=2)
            with open(os.path.join(part_dir, "metadata.json"), "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            with open(os.path.join(part_dir, "part_context.txt"), "w", encoding="utf-8") as f:
                for item in part_context:
                    f.write(item + "\n")
            with open(os.path.join(part_dir, "chapter_context.txt"), "w", encoding="utf-8") as f:
                for item in chapter_context:
                    f.write(item + "\n")
            with open(os.path.join(part_dir, "section_context.txt"), "w", encoding="utf-8") as f:
                for item in section_context:
                    f.write(item + "\n")


def gen_text(outline_path: str):
    """
    并发生成每个章节的文本内容，并写入 output 目录下的文本文件。
    """
    from text import writer, critical
    global outline_template

    def write_chapter(volume, part, chapter, chapter_content, output_dir):
        logger.info(f"开始写入章节: {volume} {part} {chapter}")
        paragraph_list = []
        context = ""
        for section, section_content in chapter_content.get("contents", {}).items():
            paragraphs = section_content["contents"]
            for paragraph_name, paragraph_text in paragraphs.items():
                generated_text = writer(
                    paragraph=paragraph_text,
                    caracters=json.dumps(section_content["caracters"]),
                    settings=json.dumps(section_content["settings"]),
                    context=context
                )
                context = generated_text
                paragraph_list.append(generated_text)
            logger.info(f"完成{volume}{part}{chapter} {section} 章节的段落生成")
        chapter_title = f"{volume} {part} {chapter} " + chapter_content["description"]
        chapter_filename = f"{volume}{part}{chapter}.txt"
        chapter_path = os.path.join(output_dir, chapter_filename)
        with open(chapter_path, "w", encoding="utf-8") as chapter_file:
            chapter_file.write(f"{chapter_title}\n\n")
            for para in paragraph_list:
                chapter_file.write(para + "\n\n")
        return chapter

    output_dir = "output"
    if not os.path.exists(outline_path):
        raise FileNotFoundError(f"Outline file {outline_path} does not exist.")

    with open(outline_path, "r", encoding="utf-8") as f:
        outline_template = json.load(f)

    os.chdir(os.path.dirname(__file__))

    tasks = []
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    with ThreadPoolExecutor(max_workers=30) as executor:
        for volume, volume_content in outline_template.items():
            for part, part_content in volume_content["contents"].items():
                for chapter, chapter_content in part_content.get("contents", {}).items():
                    tasks.append(executor.submit(write_chapter, volume, part, chapter, chapter_content, output_dir))
        for future in as_completed(tasks):
            logger.info(f"章节写入完成: {future.result()}")

if __name__ == "__main__":
    # 日志配置
    logger = logging.getLogger("LongStoryGen")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("[%(asctime)s][%(levelname)s][%(name)s]: %(message)s")
    )
    logger.addHandler(handler)

    # 选择要执行的任务
    # gen_outline()  # 生成大纲
    # gen_text("第5部/outline_template.json")  # 生成文本内容，参数为大纲的路径